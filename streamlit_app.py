#!/usr/bin/env python3
"""
Archivo principal para Streamlit Cloud en la raíz del repositorio
"""

import streamlit as st
import sys
import os

# Agregar el directorio chat_multi_usuario al path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chat_multi_usuario'))

# Mostrar mensaje de carga
st.write("🔄 Cargando Chat Multi-Usuario...")

try:
    # Importar y ejecutar la aplicación principal
    from app_streamlit import main
    
    # Ejecutar la aplicación
    main()
    
except ImportError as e:
    st.error(f"❌ Error de importación: {e}")
    st.write("**Información de debug:**")
    st.write(f"Directorio actual: {os.getcwd()}")
    st.write(f"Archivos disponibles: {os.listdir('.')}")
    st.write(f"Path de Python: {sys.path}")
    
    st.write("**Posibles soluciones:**")
    st.write("1. Verificar que el directorio chat_multi_usuario existe")
    st.write("2. Revisar las dependencias en requirements.txt")
    st.write("3. Configurar secretos en Streamlit Cloud (REDIS_URL y OPENAI_API_KEY)")
    
except Exception as e:
    st.error(f"❌ Error en la aplicación: {e}")
    st.write("**Más información:**")
    st.exception(e) 