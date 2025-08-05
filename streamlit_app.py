#!/usr/bin/env python3
"""
Archivo principal para Streamlit Cloud
Este archivo debe llamarse 'streamlit_app.py' para que Streamlit Cloud lo reconozca automáticamente
"""

import streamlit as st
import sys
import os
import traceback

# Mostrar información de debug inicial
st.write("🔄 **Iniciando Chat Multi-Usuario...**")

try:
    # Mostrar información del entorno
    st.write("📍 **Información del sistema:**")
    st.write(f"- Directorio actual: `{os.getcwd()}`")
    st.write(f"- Archivos en directorio: `{os.listdir('.')}`")
    st.write(f"- Python version: `{sys.version}`")
    
    # Verificar dependencias críticas
    st.write("📦 **Verificando dependencias...**")
    
    dependencies = ['streamlit', 'redis', 'langchain', 'openai', 'dotenv']
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            st.write(f"✅ {dep}")
        except ImportError:
            st.write(f"❌ {dep} - NO ENCONTRADO")
    
    # Verificar variables de entorno/secretos
    st.write("🔐 **Verificando configuración...**")
    
    redis_url = None
    openai_key = None
    
    # Intentar cargar desde Streamlit secrets
    try:
        redis_url = st.secrets.get("REDIS_URL")
        openai_key = st.secrets.get("OPENAI_API_KEY")
        if redis_url and openai_key:
            st.write("✅ Secretos de Streamlit Cloud configurados")
        else:
            st.write("⚠️ Secretos de Streamlit Cloud incompletos")
    except Exception as e:
        st.write(f"❌ Error cargando secretos: {e}")
    
    # Fallback a variables de entorno
    if not redis_url:
        redis_url = os.getenv("REDIS_URL")
    if not openai_key:
        openai_key = os.getenv("OPENAI_API_KEY")
    
    if not redis_url or not openai_key:
        st.error("🚨 **ERROR: Configuración faltante**")
        st.markdown("""
        **Para Streamlit Cloud:**
        1. Ve a tu app dashboard
        2. Click en "Settings" → "Secrets"
        3. Agrega:
        ```toml
        REDIS_URL = "tu_redis_url_aqui"
        OPENAI_API_KEY = "tu_openai_api_key_aqui"
        ```
        
        **Servicios gratuitos recomendados:**
        - Redis: [Redis Cloud](https://redis.com/try-free/) o [Upstash](https://upstash.com/)
        - OpenAI: [Platform OpenAI](https://platform.openai.com/api-keys)
        """)
        st.stop()
    
    st.write("✅ Configuración completa")
    st.write("🚀 **Cargando aplicación principal...**")
    
    # Importar y ejecutar la aplicación principal
    from app_streamlit import main
    
    # Limpiar mensajes de debug antes de mostrar la app
    st.empty()
    
    # Ejecutar la aplicación principal
    main()
    
except ImportError as e:
    st.error(f"❌ **Error de importación**: {e}")
    st.markdown("""
    **Posibles soluciones:**
    1. Verificar que `app_streamlit.py` existe
    2. Revisar dependencias en `requirements.txt`
    3. Verificar que todos los archivos están en el repositorio
    """)
    st.code(f"Traceback:\n{traceback.format_exc()}")
    
except Exception as e:
    st.error(f"❌ **Error de aplicación**: {e}")
    st.markdown("**Información detallada:**")
    st.code(f"Traceback:\n{traceback.format_exc()}")
    
    st.markdown("**Debug adicional:**")
    st.write(f"- Tipo de error: `{type(e).__name__}`")
    st.write(f"- Mensaje: `{str(e)}`")
    st.write(f"- Directorio: `{os.getcwd()}`")
    st.write(f"- Archivos: `{os.listdir('.')}`") 