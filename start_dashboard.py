"""
Quick Start Script für das KPI Dashboard
Führe dieses Skript aus um das Dashboard zu starten
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starte KPI Dashboard...\n")
    
    # Prüfe ob Virtual Environment aktiv ist
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual Environment ist nicht aktiv!")
        print("Bitte zuerst ausführen: .venv\\Scripts\\activate\n")
        return
    
    # Prüfe ob alle Packages installiert sind
    try:
        import streamlit
        import pandas
        import altair
        print("✅ Alle Packages installiert\n")
    except ImportError as e:
        print(f"❌ Fehlendes Package: {e}")
        print("Installiere Packages mit: pip install -r requirements.txt\n")
        return
    
    # Starte Streamlit
    print("📊 Öffne Dashboard im Browser...\n")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "kpi_dashboard_streamlit.py"])

if __name__ == "__main__":
    main()
