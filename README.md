# Tommy KPI Dashboard

Aktives Streamlit-Projekt fuer ein Multi-Standort-KPI-Dashboard im Logistik-/Dispositionskontext.

Status:
- aktives Kunden-/Anwendungsprojekt
- Python/Streamlit-Anwendung
- Datenbasis ueber PostgreSQL / Supabase
- lokaler Start ueber `streamlit run app/app.py`

## Was dieses Projekt ist

Die Anwendung dient zur Erfassung, Verwaltung und Auswertung taeglicher KPI-Daten fuer mehrere Standorte.

Im Fokus stehen:
- KPI-Erfassung
- Rollenbasiertes Login
- Reporting und Vergleiche
- Datenpersistenz ueber PostgreSQL

## Tech Stack

- Streamlit
- pandas
- Altair
- PostgreSQL
- `psycopg2-binary`

Relevante Referenzen:
- `app/app.py`
- `app/requirements.txt`
- `.milestones.json`
- `.devcontainer/devcontainer.json`

## Lokaler Start

```bash
cd /root/projects/client-work/Tommy
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
streamlit run app/app.py
```

Danach im Browser:
- `http://localhost:8501`

## Entwicklungsumgebung

Fuer das Projekt existiert bereits ein Dev-Container:
- `.devcontainer/devcontainer.json`

Damit kann die lokale Entwicklung in VS Code reproduzierbarer erfolgen.

## Kanonische Einstiegspunkte

- Projektwissen und Navigation: `.milestones.json`
- Container-Setup: `.devcontainer/devcontainer.json`
- App-Einstieg: `app/app.py`
- Python-Abhaengigkeiten: `app/requirements.txt`

## Wichtige Hinweise

- Zugangsdaten und Passwoerter gehoeren nicht in die README.
- Lokale oder Cloud-Secrets nur ueber geeignete Secret-Mechanismen verwalten.
- Diese Datei beschreibt bewusst den sicheren Einstieg und nicht komplette Betriebsinterna.
