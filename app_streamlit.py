#!/usr/bin/env python3
"""
Frontend Streamlit para Chat Multi-Usuario
"""

import streamlit as st
import os
from typing import Dict, List
from chat_multi_usuario import ChatMultiUsuario
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="🎤 Chat Multi-Usuario",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .user-badge {
        background-color: #e1f5fe;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 2px solid #0277bd;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .stButton > button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Función para inicializar sistema de chat
@st.cache_resource
def inicializar_chat():
    """Inicializar el sistema de chat (cacheable)"""
    # Intentar cargar desde Streamlit secrets primero (para deploy)
    try:
        redis_url = st.secrets["REDIS_URL"]
        openai_api_key = st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        # Fallback a variables de entorno (para desarrollo local)
        redis_url = os.getenv("REDIS_URL")
        openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not redis_url or not openai_api_key:
        st.error("❌ Error: Variables de entorno/secretos no configuradas")
        st.error("💡 Para desarrollo local: configura .env")
        st.error("🌐 Para Streamlit Cloud: configura secrets en la interfaz web")
        st.stop()
    
    return ChatMultiUsuario(redis_url, openai_api_key)

def main():
    """Función principal de la aplicación"""
    
    # Inicializar estado de sesión
    if "chat_system" not in st.session_state:
        st.session_state.chat_system = inicializar_chat()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🎤 Chat Multi-Usuario tipo Alexa/Google Home</h1>
        <p>Sistema de chat inteligente con memoria persistente por usuario</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Panel de control
    with st.sidebar:
        st.header("🎛️ Panel de Control")
        
        # Mostrar usuario actual
        if st.session_state.current_user:
            st.markdown(f"""
            <div class="user-badge">
                👤 Usuario: <strong>{st.session_state.current_user}</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👤 Sin usuario identificado")
        
        st.markdown("---")
        
        # Identificación manual
        st.subheader("🔑 Identificación Manual")
        nuevo_usuario = st.text_input("Cambiar usuario:", placeholder="Ingresa tu nombre", key="cambiar_usuario_input")
        if st.button("🔄 Cambiar Usuario", key="cambiar_usuario_btn") and nuevo_usuario:
            st.session_state.chat_system.cambiar_usuario(nuevo_usuario)
            st.session_state.current_user = nuevo_usuario
            st.success(f"✅ Usuario cambiado a: {nuevo_usuario}")
            st.rerun()
        
        st.markdown("---")
        
        # Gestión de usuarios
        st.subheader("👥 Usuarios Registrados")
        if st.button("📝 Listar Usuarios", key="listar_usuarios_btn"):
            usuarios = st.session_state.chat_system.listar_usuarios_con_historial()
            if usuarios:
                st.write("**Usuarios con historial:**")
                for usuario in usuarios:
                    st.write(f"• {usuario}")
            else:
                st.info("No hay usuarios registrados")
        
        st.markdown("---")
        
        # Historial de usuario
        st.subheader("📋 Ver Historial")
        usuario_historial = st.selectbox(
            "Usuario:", 
            ["Selecciona..."] + st.session_state.chat_system.listar_usuarios_con_historial(),
            key="select_usuario_historial"
        )
        
        if st.button("📖 Ver Historial", key="ver_historial_btn") and usuario_historial != "Selecciona...":
            with st.expander(f"Historial de {usuario_historial}", expanded=True):
                historial = st.session_state.chat_system.obtener_historial(usuario_historial)
                if historial:
                    for msg in historial:
                        if hasattr(msg, 'content'):
                            tipo = "👤 Usuario" if msg.type == "human" else "🤖 Asistente"
                            st.text(f"{tipo}: {msg.content}")
                else:
                    st.info("No hay historial para este usuario")
        
        st.markdown("---")
        
        # Limpiar chat
        if st.button("🗑️ Limpiar Chat", key="limpiar_chat_btn"):
            st.session_state.messages = []
            st.rerun()
    
    # Área principal - Chat
    st.header("💬 Chat")
    
    # Mostrar mensajes del chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input("Escribe tu mensaje aquí...", key="main_chat_input"):
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar mensaje
        with st.chat_message("assistant"):
            with st.spinner("Procesando..."):
                try:
                    respuesta = st.session_state.chat_system.procesar_mensaje(prompt)
                    
                    # Actualizar usuario actual si cambió
                    if respuesta.usuario_actual != st.session_state.current_user:
                        st.session_state.current_user = respuesta.usuario_actual
                    
                    # Mostrar respuesta
                    st.markdown(respuesta.mensaje)
                    
                    # Agregar respuesta al historial
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": respuesta.mensaje
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
    
    # Información adicional
    with st.expander("ℹ️ Información y Ayuda"):
        st.markdown("""
        ### 🎯 Cómo usar el chat:
        
        1. **Identificación**: Di "Soy [tu nombre]" para que te reconozca
        2. **Conversación**: Habla normalmente, el sistema recordará tu contexto
        3. **Cambio de usuario**: Usa el panel lateral o di "Soy [otro nombre]"
        4. **Historial**: Revisa conversaciones previas en el panel lateral
        
        ### 🔧 Características:
        - ✅ Memoria persistente por usuario
        - ✅ Detección automática de usuarios
        - ✅ Historial de conversaciones
        - ✅ Interfaz intuitiva
        - ✅ Respuestas contextuales
        
        ### 🚀 Ejemplos de uso:
        - "Soy Pablo, ¿cómo estás?"
        - "Recuerda que mi color favorito es el azul"
        - "Soy Ana, ¿me recuerdas?"
        """) 