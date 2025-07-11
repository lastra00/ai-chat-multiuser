# 🚀 Deploy en Streamlit Cloud

## 📋 Pasos para desplegar tu aplicación

### **1. Preparar el repositorio**
✅ Ya tienes todo listo en la rama `deploy/streamlit-cloud`

### **2. Ir a Streamlit Cloud**
1. Ve a **[share.streamlit.io](https://share.streamlit.io)**
2. Haz clic en **"Sign up"** o **"Sign in"** con tu cuenta de GitHub
3. Autoriza a Streamlit Cloud acceder a tus repositorios

### **3. Crear nueva aplicación**
1. Haz clic en **"New app"**
2. Selecciona tu repositorio: `lastra00/ai-chat-multiuser`
3. Selecciona la rama: `deploy/streamlit-cloud`
4. Especifica el archivo principal: `chat_multi_usuario/streamlit_app.py`
5. Haz clic en **"Deploy!"**

### **4. Configurar secretos**
1. En la interfaz de Streamlit Cloud, ve a **"Settings"** > **"Secrets"**
2. Agrega tus secretos en formato TOML:

```toml
REDIS_URL = "redis://tu-usuario:tu-password@tu-host:tu-puerto"
OPENAI_API_KEY = "tu-api-key-de-openai"
```

3. Haz clic en **"Save"**

### **5. ¡Listo!**
Tu aplicación estará disponible en: `https://tu-app-name.streamlit.app`

## 🔧 Configuración incluida

### **Archivos para deploy:**
- ✅ `streamlit_app.py` - Archivo principal que Streamlit Cloud reconoce
- ✅ `requirements.txt` - Todas las dependencias necesarias
- ✅ `.streamlit/config.toml` - Configuración de tema y servidor

### **Características del deploy:**
- 🌐 **URL pública**: Tu aplicación será accesible desde internet
- 🔄 **Auto-deploy**: Se actualiza automáticamente cuando haces push
- 🔒 **Secretos seguros**: Redis y OpenAI API key protegidas
- 🎨 **Tema personalizado**: Colores y estilo configurados
- 📱 **Responsive**: Funciona en móviles y escritorio

## 🛠️ Troubleshooting

### **Error: "No module named..."**
- Verifica que todas las dependencias estén en `requirements.txt`
- Revisa que las versiones sean compatibles

### **Error: "Secrets not found"**
- Configura los secretos en la interfaz web de Streamlit Cloud
- Verifica que los nombres coincidan exactamente

### **Error de conexión Redis**
- Verifica que la URL de Redis sea correcta
- Asegúrate de que Redis esté accesible desde internet

## 🌟 Ventajas del deploy

### **✅ Beneficios:**
- **Acceso público**: Cualquiera puede usar tu aplicación
- **Sin configuración local**: No necesitas instalar nada
- **Escalable**: Maneja múltiples usuarios simultáneos
- **Mantenimiento automático**: Streamlit Cloud se encarga de todo
- **SSL incluido**: Conexión segura HTTPS automática

### **🔄 Actualizaciones:**
- Haz push a la rama `deploy/streamlit-cloud`
- Streamlit Cloud detectará los cambios automáticamente
- La aplicación se actualizará en 1-2 minutos

## 🔗 Enlaces útiles

- **Streamlit Cloud**: https://share.streamlit.io
- **Documentación**: https://docs.streamlit.io/streamlit-cloud
- **Tu repositorio**: https://github.com/lastra00/ai-chat-multiuser
- **Soporte**: https://docs.streamlit.io/streamlit-cloud/get-help 