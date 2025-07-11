#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Streamlit
"""

import os
import subprocess
import sys

def main():
    """Ejecutar la aplicación Streamlit"""
    print("🚀 Iniciando Chat Multi-Usuario...")
    print("💡 La aplicación se abrirá en tu navegador automáticamente")
    print("🔗 Si no se abre, ve a: http://localhost:8501")
    print("⌨️  Presiona Ctrl+C para detener la aplicación")
    print("-" * 50)
    
    # Ejecutar streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app_streamlit.py", 
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--theme.base", "light"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")

if __name__ == "__main__":
    main() 