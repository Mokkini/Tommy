"""
SQLite Database Handler für KPI Dashboard
"""
import sqlite3
import pandas as pd
from datetime import datetime
import os
import time

DATABASE_PATH = os.environ.get('DATABASE_PATH', '/data/kpi_dashboard.db')

def get_connection():
    """Erstellt eine Datenbankverbindung mit Timeout und WAL-Modus."""
    conn = sqlite3.connect(
        DATABASE_PATH, 
        check_same_thread=False,
        timeout=30.0,  # 30 Sekunden warten bei Lock
        isolation_level=None  # Autocommit-Modus
    )
    conn.row_factory = sqlite3.Row
    # WAL-Modus für bessere Concurrency
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=30000')
    return conn

def init_database():
    """Initialisiert die Datenbank mit allen Tabellen."""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # KPI-Daten Tabelle
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kpi_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datum DATE NOT NULL,
                    monat TEXT NOT NULL,
                    standort TEXT NOT NULL,
                    disponent TEXT,
                    fahrzeuge INTEGER,
                    stopps INTEGER,
                    unverplante_stopps REAL,
                    kosten_fuhrpark REAL,
                    stoppschnitt REAL,
                    stoppkosten REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(datum, standort)
                )
            ''')
            
            # Standorte Tabelle
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS standorte (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    aktiv INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Disponenten Tabelle
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS disponenten (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    standort_id INTEGER,
                    aktiv INTEGER DEFAULT 1,
                    FOREIGN KEY (standort_id) REFERENCES standorte(id)
                )
            ''')
            
            # User Tabelle für Login
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # History/Audit Log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    table_name TEXT,
                    record_id INTEGER,
                    old_values TEXT,
                    new_values TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Index für schnellere Abfragen
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_kpi_datum ON kpi_data(datum)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_kpi_monat ON kpi_data(monat)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_kpi_standort ON kpi_data(standort)')
            
            conn.commit()
            conn.close()
            return  # Erfolgreich, beende Funktion
            
        except sqlite3.OperationalError as e:
            if "locked" in str(e) and attempt < max_retries - 1:
                time.sleep(1)  # Warte 1 Sekunde und versuche erneut
                continue
            raise

def get_months():
    """Gibt alle verfügbaren Monate zurück."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT monat FROM kpi_data ORDER BY monat')
    months = [row['monat'] for row in cursor.fetchall()]
    conn.close()
    return months

def get_month_data(month: str) -> pd.DataFrame:
    """Lädt alle Daten für einen Monat."""
    conn = get_connection()
    query = '''
        SELECT 
            datum, standort, disponent, fahrzeuge, stopps,
            unverplante_stopps, kosten_fuhrpark, stoppschnitt, stoppkosten
        FROM kpi_data 
        WHERE monat = ?
        ORDER BY datum, standort
    '''
    df = pd.read_sql_query(query, conn, params=(month,))
    conn.close()
    
    # Formatiere Datum für Anzeige
    if not df.empty:
        df['Datum'] = pd.to_datetime(df['datum']).dt.strftime('%d.%m.%Y')
        df = df.rename(columns={
            'standort': 'Standort',
            'disponent': 'Disponent',
            'fahrzeuge': 'Fahrzeuge',
            'stopps': 'Stopps',
            'unverplante_stopps': 'Unverplante Stopps',
            'kosten_fuhrpark': 'Kosten Fuhrpark',
            'stoppschnitt': 'Stoppschnitt',
            'stoppkosten': 'Stoppkosten'
        })
        # Datum als erste Spalte, entferne die alte 'datum' Spalte
        df = df[['Datum', 'Standort', 'Disponent', 'Fahrzeuge', 'Stopps', 'Unverplante Stopps', 'Kosten Fuhrpark', 'Stoppschnitt', 'Stoppkosten']]
    
    return df

def save_month_data(month: str, df: pd.DataFrame):
    """Speichert Daten für einen Monat."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Lösche alte Daten für diesen Monat
    cursor.execute('DELETE FROM kpi_data WHERE monat = ?', (month,))
    
    # Füge neue Daten ein
    for _, row in df.iterrows():
        try:
            # Parse Datum
            datum_str = str(row.get('Datum', '')).strip()
            if datum_str:
                datum = datetime.strptime(datum_str, '%d.%m.%Y').date()
            else:
                continue
            
            cursor.execute('''
                INSERT INTO kpi_data 
                (datum, monat, standort, disponent, fahrzeuge, stopps, 
                 unverplante_stopps, kosten_fuhrpark, stoppschnitt, stoppkosten)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datum,
                month,
                row.get('Standort', ''),
                row.get('Disponent', ''),
                parse_numeric(row.get('Fahrzeuge')),
                parse_numeric(row.get('Stopps')),
                parse_numeric(row.get('Unverplante Stopps')),
                parse_numeric(row.get('Kosten Fuhrpark')),
                parse_numeric(row.get('Stoppschnitt')),
                parse_numeric(row.get('Stoppkosten'))
            ))
        except Exception as e:
            print(f"Fehler beim Speichern von Zeile: {e}")
            continue
    
    conn.commit()
    conn.close()

def parse_numeric(value):
    """Konvertiert einen Wert zu float."""
    if pd.isna(value) or value == '' or value is None:
        return None
    try:
        return float(str(value).replace(',', '.').replace('€', '').strip())
    except:
        return None

def create_month(month: str, standorte: list):
    """Erstellt einen neuen Monat mit allen Werktagen und Standorten."""
    conn = get_connection()
    cursor = conn.cursor()
    
    year, month_num = map(int, month.split('-'))
    
    # Generiere Werktage
    from datetime import timedelta
    start_date = datetime(year, month_num, 1)
    if month_num == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month_num + 1, 1) - timedelta(days=1)
    
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Mo-Fr
            for standort in standorte:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO kpi_data 
                        (datum, monat, standort)
                        VALUES (?, ?, ?)
                    ''', (current.date(), month, standort))
                except:
                    pass
        current += timedelta(days=1)
    
    conn.commit()
    conn.close()

def delete_month(month: str) -> bool:
    """Löscht einen Monat (nur wenn keine Daten vorhanden)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Prüfe ob Daten vorhanden
    cursor.execute('''
        SELECT COUNT(*) as count FROM kpi_data 
        WHERE monat = ? AND (fahrzeuge IS NOT NULL OR stopps IS NOT NULL)
    ''', (month,))
    
    if cursor.fetchone()['count'] > 0:
        conn.close()
        return False
    
    cursor.execute('DELETE FROM kpi_data WHERE monat = ?', (month,))
    conn.commit()
    conn.close()
    return True

def get_standorte():
    """Gibt alle aktiven Standorte zurück."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM standorte WHERE aktiv = 1 ORDER BY name')
    standorte = [row['name'] for row in cursor.fetchall()]
    conn.close()
    return standorte

def init_default_standorte():
    """Initialisiert Standard-Standorte."""
    standorte = [
        'Delmenhorst', 'Güstrow', 'Döbeln', 'Melle', 'Langenfeld',
        'Kassel', 'Berlin', 'Aschaffenburg', 'Renningen'
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    for standort in standorte:
        try:
            cursor.execute('INSERT OR IGNORE INTO standorte (name) VALUES (?)', (standort,))
        except:
            pass
    
    conn.commit()
    conn.close()
