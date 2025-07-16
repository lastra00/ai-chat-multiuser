# 🚀 Guía de Deployment en Streamlit Cloud

## ⚠️ Problema: Aplicación en Blanco

Si tu app se ve en blanco en Streamlit Cloud, sigue estos pasos:

### 1. 📋 Configurar Secretos

**En Streamlit Cloud:**
1. Ve a tu dashboard de Streamlit Cloud
2. Selecciona tu app
3. Click en "Settings" → "Secrets"
4. Agrega lo siguiente:

```toml
REDIS_URL = "tu_redis_url_aqui"
OPENAI_API_KEY = "tu_openai_api_key_aqui"
```

### 2. 🔧 Verificar Archivos

Asegúrate de que estos archivos estén en la **raíz** del repositorio:
- ✅ `streamlit_app.py` (punto de entrada)
- ✅ `requirements.txt` (dependencias)

### 3. 🗂️ Estructura Correcta

```
DiploGenAI/
├── streamlit_app.py          ← Punto de entrada (RAÍZ)
├── requirements.txt          ← Dependencias (RAÍZ)
├── chat_multi_usuario/
│   ├── app_streamlit.py      ← Aplicación principal
│   ├── chat_multi_usuario.py ← Lógica del chat
│   └── .streamlit/
│       └── config.toml       ← Configuración UI
```

### 4. 🚨 Servicios Externos Necesarios

**Redis Database:**
- Opción 1: [Redis Cloud](https://redis.com/try-free/) (gratis)
- Opción 2: [Upstash Redis](https://upstash.com/) (gratis)

**OpenAI API:**
- [OpenAI Platform](https://platform.openai.com/api-keys)
- Necesitas crear una API key

### 5. 🔄 Reintentar Deployment

Después de configurar los secretos:
1. Ve a tu dashboard de Streamlit Cloud
2. Click en "Reboot app"
3. Espera 2-3 minutos para que cargue

### 6. 🐛 Debug

Si sigue fallando, revisa los logs:
1. En Streamlit Cloud → "Settings" → "Logs"
2. Busca errores de importación o conexión

## 📞 Casos Comunes

**Error: "No module named 'chat_multi_usuario'"**
→ Verifica que el directorio `chat_multi_usuario/` esté en tu repo

**Error: "REDIS_URL not found"**
→ Configura los secretos en Streamlit Cloud

**Pantalla en blanco**
→ Revisa que `streamlit_app.py` esté en la raíz

## ✅ Test Local

Para probar localmente:
```bash
cd DiploGenAI
pip install -r requirements.txt
streamlit run streamlit_app.py
``` 