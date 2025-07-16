#!/usr/bin/env python3
"""
Archivo principal para Streamlit Cloud
Este archivo debe llamarse 'streamlit_app.py' para que Streamlit Cloud lo reconozca automáticamente
"""

import streamlit as st
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mostrar mensaje de carga
st.write("🔄 Cargando aplicación...")

try:
    # Importar y ejecutar la aplicación principal
    from app_streamlit import main
    
    # Ejecutar la aplicación
    main()
    
except ImportError as e:
    st.error(f"❌ Error de importación: {e}")
    st.write("**Posibles soluciones:**")
    st.write("1. Verificar que todos los archivos estén en el repositorio")
    st.write("2. Revisar las dependencias en requirements.txt")
    
except Exception as e:
    st.error(f"❌ Error en la aplicación: {e}")
    st.write("**Información de debug:**")
    st.write(f"Directorio actual: {os.getcwd()}")
    st.write(f"Archivos disponibles: {os.listdir('.')}") 