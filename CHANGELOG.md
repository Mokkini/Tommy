# Changelog - KPI Dashboard

## Version 2.1 (01.12.2025)

### 🔧 Verbesserungen
- **Wochenvergleich korrigiert**: Aggregation erst pro Tag (alle Standorte), dann pro Woche
  - Zeigt jetzt korrekte Durchschnittswerte pro Tag/Woche
  - Spalten umbenannt zu "Ø Fzg/Tag", "Ø Stopps/Tag" etc.
- **Standorte aktualisiert**: 9 Produktionsstandorte ab Dezember 2025
  - Delmenhorst, Güstrow, Döbeln, Melle, Langenfeld, Kassel, Berlin, Aschaffenburg, Renningen
  - Oktober/November 2025 behalten die 13 alten Standorte
- **Projektaufräumung**: Alte Backup-Dateien und Testdaten entfernt
- **Dokumentation aktualisiert**: README.md und CHANGELOG.md angepasst

## Version 2.0 (01.12.2025)

### 🎉 Neue Features

#### 📊 Excel-Export mit Formatierung
- **Funktion**: `export_to_excel()` erstellt formatierte Excel-Dateien
- **Features**:
  - Professional Header-Styling (Corporate Colors)
  - Automatische Spaltenbreiten-Anpassung
  - Zellformatierung nach Datentyp (€, Zahlen, Dezimalen)
  - Automatische Diagramm-Generierung in separatem Sheet
  - Export-Buttons in:
    - Eingabemaske (neben CSV-Export)
    - Daily Report (für Tages-Report)
    - Wochenvergleich
    - Monatsvergleich

#### 📈 Wochenvergleich (neue Seite)
- **Funktion**: `compare_weeks()` aggregiert Daten pro Kalenderwoche
- **Features**:
  - ISO-Kalenderwochen (KW 1, KW 2, etc.)
  - KPIs pro Woche: Fahrzeuge (Summe), Stopps (Summe), Stoppschnitt (Durchschnitt)
  - Delta-Berechnung Woche zu Woche (absolut)
  - Prozentuale Veränderung (Delta %)
  - Visualisierung mit Line Charts (Stopps & Stoppkosten)
  - Vollständige Tabelle mit allen Deltas
  - Excel-Export der Wochenanalyse

#### 📅 Monatsvergleich (neue Seite)
- **Funktion**: `compare_months()` vergleicht zwei Monate
- **Features**:
  - Auswahl von 2 Monaten via Dropdown
  - Side-by-Side Vergleich aller 5 KPIs
  - Delta-Berechnung absolut und prozentual
  - Interaktive Balkendiagramme (grouped bars)
  - Übersichtliche Tabelle mit allen Metriken
  - Excel-Export des Vergleichs

#### 💾 Autosave
- **Session State**: `autosave_enabled` Flag
- **Features**:
  - Toggle-Switch in Sidebar (aktiviert/deaktiviert)
  - Automatisches Speichern beim Bearbeiten
  - Verhindert Datenverlust bei versehentlichem Schließen
  - Echtzeit-Synchronisation mit CSV
  - Status-Anzeige in der UI

#### ↶ Undo/Redo
- **Session State**: `history` (Liste), `history_index` (Integer)
- **Funktion**: `save_to_history()`, `undo()`, `redo()`
- **Features**:
  - History-Stack mit bis zu 20 Einträgen
  - Undo-Button (↶): Letzte Änderung rückgängig
  - Redo-Button (↷): Rückgängig gemachte Änderung wiederholen
  - History-Counter (X/Y Anzeige)
  - Buttons disabled wenn nicht möglich
  - Speichert vollständige DataFrame-Kopien

#### ✅ Datenvalidierung
- **Funktion**: `validate_data()` prüft alle Eingaben
- **Validierungen**:
  - **Datumsformat**: TT.MM.JJJJ (z.B. 25.11.2025)
  - **Numerische Felder**: Fahrzeuge, Stopps, Unverplante Stopps, Stoppkosten
  - **Negative Werte**: Nicht erlaubt
  - **Pflichtfelder**: Datum, Standort
  - **Datentyp-Prüfung**: Zahlen müssen numerisch sein
- **Feedback**:
  - 🚨 Fehler (rot): Speichern nicht möglich
  - ⚠️ Warnungen (gelb): Speichern möglich, aber unvollständig
  - Liste aller Fehler mit Zeilennummer
  - Speichern-Button deaktiviert bei Fehlern

### 🔧 Technische Verbesserungen

#### Imports
- `openpyxl`: Excel-Manipulation
- `BytesIO`: In-Memory-Dateien für Downloads
- `copy`: Deep-Copying für History
- `timedelta`: Wochenberechnungen

#### Session State Management
- `history`: Liste von DataFrame-States
- `history_index`: Aktueller Position in History
- `autosave_enabled`: Boolean für Autosave
- `last_saved_df`: Letzter gespeicherter Stand

#### Neue Funktionen
```python
validate_data(df) -> (errors, warnings)
save_to_history(df, month_file)
undo() -> DataFrame
redo() -> DataFrame
export_to_excel(df, month_name) -> BytesIO
get_week_number(date) -> int
compare_weeks(df) -> DataFrame
compare_months(file1, file2) -> (DataFrame, df1, df2)
```

### 🎨 UI/UX Verbesserungen
- Neue Navigation: 5 statt 3 Seiten
- Undo/Redo Buttons prominent in Eingabemaske
- Autosave-Toggle in Sidebar
- Excel-Download-Buttons mit 📊 Icon
- Validierungs-Feedback mit Icons (🚨, ⚠️, ✅)
- History-Counter in Eingabemaske
- Disabled-States für Buttons wenn nicht nutzbar

### 📦 Dependencies
```txt
streamlit>=1.28.0
pandas>=2.0.0
altair>=5.0.0
openpyxl>=3.1.0  # NEU
```

### 🐛 Bugfixes
- Streamlit 1.30+ Deprecation Warning behoben (`use_container_width` → `width='stretch'`)
- DataFrame-Type-Handling für Session State verbessert

### 📄 Dateien
- `kpi_dashboard_streamlit.py`: Hauptdatei (701 Zeilen)
- `kpi_dashboard_streamlit_backup.py`: Backup der alten Version
- `requirements.txt`: Aktualisiert mit openpyxl
- `CHANGELOG.md`: Dieses Dokument

### 🚀 Nächste Schritte (Ideen)
- [ ] PDF-Report-Generierung
- [ ] E-Mail-Benachrichtigungen
- [ ] Cloud-Deployment (Streamlit Cloud / Azure)
- [ ] Multi-User mit Login
- [ ] API-Integration für Datenimport
- [ ] Machine Learning Forecasting
