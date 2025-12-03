# KPI Dashboard

Ein interaktives Streamlit-Dashboard zur Verwaltung und Visualisierung von Logistik-KPIs.

## 🚀 Installation

```bash
# Virtual Environment aktivieren
.venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt
```

## ▶️ Starten

```bash
streamlit run kpi_dashboard_streamlit.py
```

## 📊 Features

### 📝 Eingabemaske
- Tägliche KPI-Erfassung pro Standort
- Inline-Bearbeitung mit `data_editor`
- Automatische Berechnung des Stoppschnitts
- Undo/Redo Funktionalität für Änderungen
- Datenvalidierung mit Fehler- und Warnhinweisen
- CSV & Excel Export

### 📊 Daily Report
- KPI-Übersicht des letzten Eintrags
- Delta-Vergleich zum Vormonat
- TOP 5 / BOTTOM 5 Standorte nach Stoppkosten
- Performance-Ranking

### 📅 Wochenvergleich
- KPI-Analyse pro Kalenderwoche
- Woche-zu-Woche Deltas (absolut & prozentual)
- Trend-Diagramme für Stopps und Stoppkosten
- Excel Export

### 📈 Monatsvergleich
- **2-Monats-Vergleich**: Direkter Vergleich zweier Monate mit Delta-Berechnung
- **Multi-Monats-Analyse**: Analyse mehrerer Monate gleichzeitig
  - Übersichtstabelle aller KPIs
  - Trend-Diagramme über ausgewählte Monate
  - Monat-zu-Monat Veränderungen
  - KPI Heatmap
- Bar-Charts für visuelle Vergleiche
- Excel Export

### 📉 Verlauf (KPIs)
- Historische Entwicklung pro Standort
- Multi-Standort-Auswahl
- Liniendiagramme für alle KPIs
- Zeitreihenanalyse

### 🗂️ Monatsverwaltung
- Neuen Monat anlegen (automatisch mit allen Werktagen und Standorten vorausgefüllt)
- Monat löschen (nur unbefüllte Monate)
- Separate CSV-Dateien pro Monat

## 📁 Projektstruktur

```
Tommy/
├── kpi_dashboard_streamlit.py   # Hauptanwendung
├── start_dashboard.py           # Quick-Start Script
├── monatsdaten/                 # Monatliche CSV-Dateien
│   ├── 2025-10.csv
│   ├── 2025-11.csv
│   └── 2025-12.csv
├── requirements.txt             # Python Dependencies
├── README.md                    # Dokumentation
└── CHANGELOG.md                 # Versionshistorie
```

## 🎯 KPIs

- Fahrzeuge
- Stopps
- Stoppschnitt
- Unverplante Stopps
- Stoppkosten

## 👥 Standorte

**Produktionsstandorte (ab Dezember 2025):**
9 Standorte: Delmenhorst, Güstrow, Döbeln, Melle, Langenfeld, Kassel, Berlin, Aschaffenburg, Renningen

**Historische Standorte (Oktober-November 2025):**
13 Standorte: Aschaffenburg, Renningen, Hamburg, Hannover, Langenfeld, Föhren, Kassel, Stockstadt, Eutingen, Berlin, Melle, Delmenhorst, Güstrow

## 🛠️ Technische Details

- **Framework**: Streamlit
- **Datenverarbeitung**: Pandas
- **Visualisierung**: Altair
- **Export**: Excel (openpyxl), CSV
- **Datenspeicherung**: CSV-Dateien pro Monat in `monatsdaten/`

## 🔧 Funktionen im Detail

### Automatische Berechnungen
- Stoppschnitt = Stopps ÷ Fahrzeuge (automatisch berechnet)
- Delta-Berechnungen zum Vormonat
- Wöchentliche und monatliche Aggregationen

### Datenvalidierung
- Pflichtfelder: Datum, Standort
- Datumsformat-Prüfung (TT.MM.JJJJ)
- Numerische Werte-Validierung
- Warnungen bei fehlenden Daten

### History Management
- Undo/Redo für alle Änderungen
- History-Index Anzeige
- Schutz vor Datenverlust

## 📝 Workflow

1. **Monat anlegen**: Neuen Monat erstellen (wird mit allen Werktagen vorausgefüllt)
2. **Daten eingeben**: KPIs täglich pro Standort erfassen
3. **Analysieren**: Dashboard-Seiten für verschiedene Analysen nutzen
4. **Exportieren**: Daten als Excel oder CSV exportieren
5. **Vergleichen**: Wochen- oder Monatsvergleiche durchführen
