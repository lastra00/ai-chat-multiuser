#!/usr/bin/env python3
"""
Chat Multi-Usuario tipo Alexa/Google Home
Ejercicio Grupal Offline - Diploma en Generative AI

Este sistema permite que múltiples usuarios conversen con un asistente AI
que recuerda las conversaciones individuales de cada usuario usando Redis.
"""

import os
import re
from typing import Optional, Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ========================================
# 1. MODELOS PYDANTIC PARA OUTPUT PARSING
# ========================================

class DeteccionUsuario(BaseModel):
    """Modelo para detectar si un usuario se está identificando"""
    usuario_identificado: bool = Field(
        description="True si el usuario está diciendo su nombre o identificándose"
    )
    nombre_usuario: Optional[str] = Field(
        description="Nombre del usuario extraído del mensaje, si está presente"
    )
    tipo_identificacion: Literal["presentacion", "referencia", "ninguna"] = Field(
        description="Tipo de identificación: 'presentacion' (soy X), 'referencia' (mi nombre es X), 'ninguna'"
    )

class RespuestaChat(BaseModel):
    """Modelo para estructurar las respuestas del chat"""
    mensaje: str = Field(description="Respuesta del asistente")
    usuario_actual: Optional[str] = Field(description="Usuario con el que se está conversando")
    requiere_identificacion: bool = Field(
        description="True si se necesita que el usuario se identifique"
    )

# ========================================
# 2. CONFIGURACIÓN DE MODELOS Y REDIS
# ========================================

# 🤖 CLASE PRINCIPAL DEL SISTEMA DE CHAT

class ChatMultiUsuario:
    def __init__(self, redis_url: str, openai_api_key: str):
        """Inicializa el sistema de chat multi-usuario"""
        self.redis_url = redis_url
        self.usuario_actual = None

        # Configurar OpenAI API
        os.environ["OPENAI_API_KEY"] = openai_api_key

        # Modelo para detección de usuarios
        self.llm_detector = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(DeteccionUsuario)

        # Modelo principal para el chat (usa output parser)
        self.llm_chat = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(RespuestaChat)

        # Prompt para detección de usuarios
        self.prompt_detector = ChatPromptTemplate.from_template(
            """
            Analiza este mensaje y determina si el usuario se está identificando con su nombre.

            Ejemplos de identificación:
            - "Soy Pablo" → usuario_identificado=True, nombre_usuario="Pablo", tipo="presentacion"
            - "Me llamo Ana" → usuario_identificado=True, nombre_usuario="Ana", tipo="presentacion"
            - "Soy María, quiero saber más" → usuario_identificado=True, nombre_usuario="María", tipo="presentacion"
            - "Hola, aquí Juan otra vez" → usuario_identificado=True, nombre_usuario="Juan", tipo="referencia"
            - "¿Cómo estás?" → usuario_identificado=False, nombre_usuario=None, tipo="ninguna"

            Mensaje: "{mensaje}"
            """
        )

        # Prompt principal del chat
        self.prompt_chat = ChatPromptTemplate.from_messages([
            ("system", """
            Eres un asistente de IA tipo Alexa o Google Home que recuerda conversaciones con diferentes usuarios.

            Comportamiento:
            - Si conoces al usuario, salúdalo por su nombre y referencia conversaciones anteriores si es relevante
            - Si no conoces al usuario, pídele que se identifique de manera amigable
            - Sé conversacional, útil y recuerda el contexto de conversaciones anteriores
            - Cuando un usuario se identifique, confirma que lo reconoces y estás listo para continuar

            Usuario actual: {usuario_actual}
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        # Cadenas de procesamiento
        self.cadena_detector = self.prompt_detector | self.llm_detector
        self.cadena_chat = self.prompt_chat | self.llm_chat

        print("✅ Sistema de chat inicializado")

    def detectar_usuario(self, mensaje: str) -> DeteccionUsuario:
        """Detecta si el usuario se está identificando en el mensaje"""
        return self.cadena_detector.invoke({"mensaje": mensaje})

    def obtener_historial(self, nombre_usuario: str) -> list:
        """Obtiene el historial de conversación de un usuario"""
        history = RedisChatMessageHistory(
            session_id=f"usuario_{nombre_usuario.lower()}",
            url=self.redis_url
        )
        return history.messages

    def procesar_mensaje(self, mensaje: str) -> RespuestaChat:
        """Procesa un mensaje del usuario, detecta identificación y genera respuesta"""
        # Detectar si hay identificación de usuario
        deteccion = self.detectar_usuario(mensaje)

        # Si se detecta un usuario, cambiar el usuario actual
        if deteccion.usuario_identificado and deteccion.nombre_usuario:
            self.usuario_actual = deteccion.nombre_usuario
            print(f"🔄 Usuario identificado: {self.usuario_actual}")

        # Si no hay usuario actual, pedir identificación
        if not self.usuario_actual:
            return RespuestaChat(
                mensaje=(
                    "¡Hola! Soy tu asistente personal. Para poder recordar nuestras conversaciones, "
                    "¿podrías decirme tu nombre? Por ejemplo: 'Soy María' o 'Me llamo Juan'"
                ),
                usuario_actual=None,
                requiere_identificacion=True
            )

        # Generar respuesta usando el historial del usuario actual
        session_id = f"usuario_{self.usuario_actual.lower()}"

        # Obtener historial y generar respuesta
        chat_history = self.obtener_historial(self.usuario_actual)
        respuesta_obj = self.cadena_chat.invoke({
            "input": mensaje,
            "usuario_actual": self.usuario_actual,
            "chat_history": chat_history
        })

        # Guardar manualmente los mensajes en Redis
        historial = RedisChatMessageHistory(session_id=session_id, url=self.redis_url)
        historial.add_user_message(mensaje)
        historial.add_ai_message(respuesta_obj.mensaje)

        return respuesta_obj

    def cambiar_usuario(self, nuevo_usuario: str):
        """Cambia manualmente el usuario actual"""
        self.usuario_actual = nuevo_usuario
        print(f"🔄 Usuario cambiado a: {self.usuario_actual}")

    def mostrar_historial(self, nombre_usuario: str):
        """Muestra el historial de conversación de un usuario"""
        historial = self.obtener_historial(nombre_usuario)
        print(f"\n📋 Historial de {nombre_usuario}:")
        print("-" * 50)

        if not historial:
            print("No hay conversaciones previas.")
            return

        for i, mensaje in enumerate(historial, 1):
            if isinstance(mensaje, HumanMessage):
                print(f"{i}. 👤 {nombre_usuario}: {mensaje.content}")
            elif isinstance(mensaje, AIMessage):
                print(f"{i}. 🤖 Asistente: {mensaje.content}")
        print("-" * 50)

    def listar_usuarios_con_historial(self) -> list:
        """Lista todos los usuarios con conversaciones previas"""
        import redis
        usuarios = []
        try:
            # Crear conexión Redis temporal
            redis_client = redis.from_url(self.redis_url)
            
            # Buscar claves de usuarios
            keys = redis_client.keys("message_store:usuario_*")
            
            for key in keys:
                # Extraer nombre de usuario de la key
                key_str = key.decode('utf-8') if isinstance(key, bytes) else key
                
                if key_str.startswith('message_store:usuario_'):
                    # Extraer el nombre después de 'message_store:usuario_'
                    usuario = key_str.replace('message_store:usuario_', '')
                    # Verificar que la clave tiene contenido
                    longitud = redis_client.llen(key_str)
                    
                    if longitud > 0:
                        usuarios.append(usuario)
                    
        except Exception as e:
            print(f"❌ Error al conectar con Redis: {e}")
        
        return usuarios

# ========================================
# 3. FUNCIÓN PRINCIPAL INTERACTIVA
# ========================================

def chat_interactivo():
    """
    Función principal para ejecutar el chat interactivo en Google Colab
    """
    print("🎤 CHAT MULTI-USUARIO TIPO ALEXA/GOOGLE HOME")
    print("=" * 60)
    print("Comandos especiales:")
    print("- 'salir' o 'quit': Terminar el chat")
    print("- 'cambiar usuario [nombre]': Cambiar de usuario manualmente")
    print("- 'historial [nombre]': Ver historial de un usuario")
    print("- 'usuarios': Listar usuarios conocidos")
    print("=" * 60)
    
    # Configuración desde variables de entorno
    REDIS_URL = os.getenv("REDIS_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Verificar que las variables existen
    if not REDIS_URL:
        print("❌ Error: REDIS_URL no encontrada en el archivo .env")
        return
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY no encontrada en el archivo .env")
        return
    
    print(f"✅ Credenciales cargadas desde .env")
    
    # Inicializar el sistema
    chat_system = ChatMultiUsuario(REDIS_URL, OPENAI_API_KEY)
    
    print("\n🚀 Sistema iniciado. ¡Comienza a conversar!")
    print("💡 Tip: Identifícate diciendo 'Soy [tu nombre]' para que te recuerde.\n")
    
    while True:
        try:
            # Mostrar usuario actual
            usuario_info = f"({chat_system.usuario_actual})" if chat_system.usuario_actual else "(Sin identificar)"
            mensaje = input(f"\n👤 {usuario_info} Tú: ").strip()
            
            # Comandos especiales
            if mensaje.lower() in ['salir', 'quit', 'exit']:
                print("👋 ¡Hasta luego!")
                break
            
            if mensaje.lower().startswith('cambiar usuario'):
                try:
                    nombre = mensaje.split('cambiar usuario')[1].strip()
                    chat_system.cambiar_usuario(nombre)
                    continue
                except IndexError:
                    print("❌ Uso: cambiar usuario [nombre]")
                    continue
            
            if mensaje.lower().startswith('historial'):
                try:
                    nombre = mensaje.split('historial')[1].strip()
                    chat_system.mostrar_historial(nombre)
                    continue
                except IndexError:
                    print("❌ Uso: historial [nombre]")
                    continue
            
            if mensaje.lower() == 'usuarios':
                usuarios = chat_system.listar_usuarios_con_historial()
                if usuarios:
                    print(f"👥 Usuarios conocidos: {', '.join(usuarios)}")
                else:
                    print("👥 No hay usuarios con historial registrados")
                continue
            
            # Procesar mensaje normal
            if not mensaje:
                continue
            
            print("🤖 Asistente: ", end="")
            respuesta = chat_system.procesar_mensaje(mensaje)
            print(respuesta.mensaje)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrumpido. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

# ========================================
# 4. FUNCIÓN DE TESTING
# ========================================

def test_multi_usuario():
    """
    Función de testing para validar el funcionamiento multi-usuario
    """
    print("🧪 TESTING MULTI-USUARIO")
    print("=" * 40)
    
    # Configuración desde variables de entorno
    REDIS_URL = os.getenv("REDIS_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Verificar que las variables existen
    if not REDIS_URL:
        print("❌ Error: REDIS_URL no encontrada en el archivo .env")
        return
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY no encontrada en el archivo .env")
        return
    
    print(f"✅ Credenciales cargadas desde .env")
    
    chat_system = ChatMultiUsuario(REDIS_URL, OPENAI_API_KEY)
    
    # Escenarios de testing
    escenarios = [
        ("Soy Pablo, ¿cómo estás?", "Pablo se identifica"),
        ("¿Cuál es mi color favorito?", "Pablo pregunta info personal"),
        ("Soy María, quiero saber el clima", "María se identifica"),
        ("Recuerda que mi comida favorita es pizza", "María da info personal"),
        ("Soy Pablo otra vez", "Pablo regresa"),
        ("¿Recuerdas mi color favorito?", "Pablo pregunta info previa"),
    ]
    
    for mensaje, descripcion in escenarios:
        print(f"\n🎯 {descripcion}")
        print(f"👤 Usuario: {mensaje}")
        respuesta = chat_system.procesar_mensaje(mensaje)
        print(f"🤖 Asistente: {respuesta.mensaje}")
        print(f"👥 Usuario actual: {respuesta.usuario_actual}")

if __name__ == "__main__":
    # Ejecutar en modo interactivo
    chat_interactivo() 