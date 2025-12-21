"""
PostgreSQL Database Handler für KPI Dashboard mit Supabase
"""
import psycopg2
from psycopg2 import pool, extras
import pandas as pd
from datetime import datetime, timedelta
import os

# Supabase Connection String (wird als ENV Variable gesetzt)
DATABASE_URL = os.environ.get('DATABASE_URL', '')

# Connection Pool für bessere Performance
connection_pool = None

def get_connection_pool():
    """Erstellt oder gibt den Connection Pool zurück."""
    global connection_pool
    if connection_pool is None:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10,  # Min/Max Connections
            DATABASE_URL
        )
    return connection_pool

def get_connection():
    """Holt eine Connection aus dem Pool."""
    pool = get_connection_pool()
    return pool.getconn()

def return_connection(conn):
    """Gibt eine Connection zurück in den Pool."""
    pool = get_connection_pool()
    pool.putconn(conn)

def init_database():
    """Initialisiert die Datenbank mit allen Tabellen."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # KPI-Daten Tabelle
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kpi_data (
                id SERIAL PRIMARY KEY,
                datum DATE NOT NULL,
                monat VARCHAR(7) NOT NULL,
                standort VARCHAR(100) NOT NULL,
                disponent VARCHAR(100),
                fahrzeuge INTEGER,
                stopps INTEGER,
                unverplante_stopps NUMERIC(10,2),
                kosten_fuhrpark NUMERIC(10,2),
                stoppschnitt NUMERIC(10,2),
                stoppkosten NUMERIC(10,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(datum, standort)
            )
        ''')
        
        # Standorte Tabelle
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS standorte (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                aktiv BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Disponenten Tabelle
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS disponenten (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                standort_id INTEGER REFERENCES standorte(id),
                aktiv BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # User Tabelle für Login
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # History/Audit Log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                action VARCHAR(50) NOT NULL,
                table_name VARCHAR(50),
                record_id INTEGER,
                old_values TEXT,
                new_values TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Indizes für schnellere Abfragen
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_kpi_datum ON kpi_data(datum)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_kpi_monat ON kpi_data(monat)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_kpi_standort ON kpi_data(standort)')
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Fehler bei Datenbank-Initialisierung: {e}")
        raise
    finally:
        return_connection(conn)

def get_months():
    """Gibt alle verfügbaren Monate zurück."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT monat FROM kpi_data ORDER BY monat')
        months = [row[0] for row in cursor.fetchall()]
        return months
    finally:
        return_connection(conn)

def get_month_data(month: str) -> pd.DataFrame:
    """Lädt alle Daten für einen Monat."""
    conn = get_connection()
    try:
        query = '''
            SELECT 
                datum, standort, disponent, fahrzeuge, stopps,
                unverplante_stopps, kosten_fuhrpark, stoppschnitt, stoppkosten
            FROM kpi_data 
            WHERE monat = %s
            ORDER BY datum, standort
        '''
        df = pd.read_sql_query(query, conn, params=(month,))
        
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
            df = df[['Datum', 'Standort', 'Disponent', 'Fahrzeuge', 'Stopps', 
                     'Unverplante Stopps', 'Kosten Fuhrpark', 'Stoppschnitt', 'Stoppkosten']]
        
        return df
    finally:
        return_connection(conn)

def save_month_data(month: str, df: pd.DataFrame):
    """Speichert Daten für einen Monat."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Lösche alte Daten für diesen Monat
        cursor.execute('DELETE FROM kpi_data WHERE monat = %s', (month,))
        
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
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (datum, standort) 
                    DO UPDATE SET
                        disponent = EXCLUDED.disponent,
                        fahrzeuge = EXCLUDED.fahrzeuge,
                        stopps = EXCLUDED.stopps,
                        unverplante_stopps = EXCLUDED.unverplante_stopps,
                        kosten_fuhrpark = EXCLUDED.kosten_fuhrpark,
                        stoppschnitt = EXCLUDED.stoppschnitt,
                        stoppkosten = EXCLUDED.stoppkosten,
                        updated_at = CURRENT_TIMESTAMP
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
        
    except Exception as e:
        conn.rollback()
        raise
    finally:
        return_connection(conn)

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
    try:
        cursor = conn.cursor()
        
        year, month_num = map(int, month.split('-'))
        
        # Generiere Werktage
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
                            INSERT INTO kpi_data (datum, monat, standort)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (datum, standort) DO NOTHING
                        ''', (current.date(), month, standort))
                    except:
                        pass
            current += timedelta(days=1)
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise
    finally:
        return_connection(conn)

def delete_month(month: str) -> bool:
    """Löscht einen Monat (nur wenn keine Daten vorhanden)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Prüfe ob Daten vorhanden
        cursor.execute('''
            SELECT COUNT(*) as count FROM kpi_data 
            WHERE monat = %s AND (fahrzeuge IS NOT NULL OR stopps IS NOT NULL)
        ''', (month,))
        
        if cursor.fetchone()[0] > 0:
            return False
        
        cursor.execute('DELETE FROM kpi_data WHERE monat = %s', (month,))
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        return False
    finally:
        return_connection(conn)

def get_standorte():
    """Gibt alle aktiven Standorte zurück."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM standorte WHERE aktiv = TRUE ORDER BY name')
        standorte = [row[0] for row in cursor.fetchall()]
        return standorte
    finally:
        return_connection(conn)

def init_default_standorte():
    """Initialisiert Standard-Standorte."""
    standorte = [
        'Delmenhorst', 'Güstrow', 'Döbeln', 'Melle', 'Langenfeld',
        'Kassel', 'Berlin', 'Aschaffenburg', 'Renningen'
    ]
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        for standort in standorte:
            try:
                cursor.execute('''
                    INSERT INTO standorte (name) 
                    VALUES (%s) 
                    ON CONFLICT (name) DO NOTHING
                ''', (standort,))
            except:
                pass
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
    finally:
        return_connection(conn)
