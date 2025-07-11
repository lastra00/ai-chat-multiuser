# 🎤 Chat Multi-Usuario tipo Alexa/Google Home

## 📋 Ejercicio Grupal Offline - Diploma en Generative AI

Este proyecto implementa un **chat multi-usuario** tipo Alexa/Google Home que recuerda conversaciones individuales de diferentes usuarios usando **Redis** como base de datos de memoria persistente.

## 🎯 Objetivo

Crear un sistema de chat que:
- Detecte automáticamente cuando un usuario se identifica
- Mantenga historiales separados por cada usuario en Redis
- Utilice Output Parsers y Prompt Templates de LangChain
- Funcione como un asistente conversacional inteligente

## ✨ Características Principales

### 🔍 Detección Inteligente de Usuarios
- Reconoce automáticamente frases como "Soy Pablo" o "Me llamo Ana"
- Utiliza **Output Parsers** de Pydantic para estructurar la detección
- Cambia automáticamente de contexto entre usuarios

### 💾 Memoria Persistente
- Historiales separados por usuario en **Redis**
- Recuerda conversaciones anteriores entre sesiones
- Gestión eficiente de múltiples usuarios simultáneos

### 🤖 Conversación Natural
- **Prompt Templates** optimizados para contexto conversacional
- Respuestas personalizadas basadas en historial previo
- Interfaz tipo asistente de voz (Alexa/Google Home)

### 🛠️ Funcionalidades Avanzadas
- Comandos especiales para gestión de usuarios
- Pruebas automáticas del sistema
- Funciones de utilidad para debugging
- Chat interactivo en Google Colab

## 🚀 Instalación y Uso

### 1. Clonar el Repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd chat-multi-usuario
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install langchain langchain-openai langchain-community redis pydantic python-dotenv
```

### 3. Configurar Credenciales
Crear archivo `.env` en la raíz del proyecto:
```bash
# Configuración de Redis
REDIS_URL=redis://localhost:6379

# Configuración de OpenAI
OPENAI_API_KEY=tu-api-key-aqui
```

**Nota**: El sistema ahora carga automáticamente las credenciales desde el archivo `.env`, por lo que ya no necesitas ingresarlas manualmente cada vez que ejecutes el programa.

### 4. Ejecutar el Sistema

#### Opción A: Archivo Python
```bash
python chat_multi_usuario.py
```

#### Opción B: Google Colab
1. Abrir `Chat_Multi_Usuario_Ejercicio.ipynb` en Google Colab
2. Configurar credenciales en la sección 2
3. Ejecutar todas las celdas secuencialmente
4. Usar `chat_interactivo_colab()` para iniciar el chat

## 📁 Estructura del Proyecto

```
chat-multi-usuario/
├── chat_multi_usuario.py          # Sistema principal
├── Chat_Multi_Usuario_Ejercicio.ipynb  # Notebook de Google Colab
├── README.md                      # Este archivo
└── requirements.txt               # Dependencias
```

## 🎮 Cómo Usar el Chat

### Identificación de Usuario
```
Usuario: Soy Pablo
🔄 Usuario identificado: Pablo
Asistente: ¡Hola Pablo! Me da mucho gusto conocerte...
```

### Cambio de Usuario
```
Usuario: Soy María, ¿me recuerdas?
🔄 Usuario identificado: María
Asistente: ¡Hola María! Por supuesto que te recuerdo...
```

### Comandos Especiales
- `salir` - Terminar el chat
- `estado` - Ver usuario actual
- `cambiar [nombre]` - Cambiar usuario manualmente
- `historial [nombre]` - Ver historial de un usuario

## 🧪 Pruebas y Validación

### Pruebas Automáticas
```python
# Ejecutar suite de pruebas
probar_escenarios()
```

### Verificar Historiales
```python
# Ver historiales guardados en Redis
verificar_historiales()
```

### Probar Detección
```python
# Probar detección de usuario
test_deteccion_usuario("Soy Carlos")
```

## 📊 Ejemplo de Funcionamiento

```
👤 Usuario: Hola
🤖 Asistente: ¡Hola! Para recordar nuestras conversaciones, ¿podrías decirme tu nombre?

👤 Usuario: Soy Ana
🔄 Usuario identificado: Ana
🤖 Asistente: ¡Hola Ana! Me da mucho gusto conocerte...

👤 Usuario: Recuerda que mi color favorito es el verde
🤖 Asistente: Perfecto Ana, recordaré que tu color favorito es el verde...

👤 Usuario: Soy Pablo, ¿cómo estás?
🔄 Usuario identificado: Pablo
🤖 Asistente: ¡Hola Pablo! ¿Cómo estás? Es un placer conocerte...

👤 Usuario: Soy Ana otra vez, ¿recuerdas mi color favorito?
🔄 Usuario identificado: Ana
🤖 Asistente: ¡Hola de nuevo Ana! Por supuesto, tu color favorito es el verde...
```

## 🔧 Configuración Técnica

### Modelos Utilizados
- **Detección de Usuario**: `gpt-4o-mini` (temperature=0)
- **Chat Principal**: `gpt-4o-mini` (temperature=0.7)

### Estructura de Datos
- **Session ID**: `usuario_{nombre_usuario.lower()}`
- **Redis Keys**: Gestionadas automáticamente por LangChain
- **Tipos de Mensaje**: `HumanMessage`, `AIMessage`

### Output Parsers
```python
class DeteccionUsuario(BaseModel):
    usuario_identificado: bool
    nombre_usuario: Optional[str]
    tipo_identificacion: Literal["presentacion", "referencia", "ninguna"]
```

## 🚀 Características Avanzadas

### Prompt Templates
- Sistema optimizado para contexto conversacional
- Placeholders para historial y usuario actual
- Instrucciones específicas para comportamiento tipo asistente

### Gestión de Memoria
- Historiales separados por usuario en Redis
- Persistencia automática de conversaciones
- Recuperación eficiente de contexto

### Manejo de Errores
- Validación de credenciales
- Manejo de excepciones de Redis
- Recuperación automática de errores

## 📝 Requisitos Técnicos

### Dependencias
- `langchain` >= 0.1.0
- `langchain-openai` >= 0.1.0
- `langchain-community` >= 0.1.0
- `redis` >= 4.0.0
- `pydantic` >= 2.0.0
- `python-dotenv` >= 1.0.0

### Credenciales Necesarias
- **OpenAI API Key**: Para acceso a GPT-4o-mini
- **Redis URL**: Para persistencia de datos

## 🎓 Cumplimiento del Ejercicio

### ✅ Requisitos Cumplidos
1. **Detección de usuarios**: Sistema automático con Output Parsers
2. **Memoria multi-usuario**: Historiales separados en Redis
3. **Output Parsers**: Modelos Pydantic para estructurar respuestas
4. **Prompt Templates**: Templates optimizados para contexto
5. **Funcionamiento tipo Alexa**: Interfaz conversacional natural

### 🧪 Validación
- Pruebas automáticas de múltiples escenarios
- Verificación de persistencia en Redis
- Validación de cambio de contexto entre usuarios
- Testing de comandos especiales

## 🛠️ Desarrollo y Contribución

### Estructura del Código
- **ChatMultiUsuario**: Clase principal del sistema
- **DeteccionUsuario**: Modelo para parsing de identificación
- **RespuestaChat**: Modelo para estructurar respuestas
- **Funciones utilitarias**: Testing y debugging

### Posibles Mejoras
- Autenticación por voz
- Integración con APIs externas
- Análisis de sentimientos
- Dashboard web de gestión
- Notificaciones push

## 📞 Soporte

Para preguntas o problemas:
1. Revisar la sección de pruebas automáticas
2. Verificar configuración de credenciales
3. Consultar logs de Redis
4. Validar conexión a OpenAI API

## 🏆 Conclusión

Este proyecto implementa exitosamente un **chat multi-usuario tipo Alexa/Google Home** con:
- Detección automática de usuarios
- Memoria persistente en Redis
- Conversaciones contextuales
- Interfaz natural y amigable

¡Disfruta experimentando con tu asistente multi-usuario! 🎉 