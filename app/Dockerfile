# KPI Dashboard - Docker Image
FROM python:3.11-slim

# Arbeitsverzeichnis
WORKDIR /app

# System-Dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Datenverzeichnis erstellen
RUN mkdir -p /data

# Port für Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Umgebungsvariablen
ENV DATABASE_PATH=/data/kpi_dashboard.db
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Startbefehl
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
