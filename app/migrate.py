"""
Migrations-Script: Konvertiert CSV-Dateien zu SQLite
"""
import os
import sys
import pandas as pd
from datetime import datetime

# Füge Parent-Verzeichnis zum Path hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_connection, init_database, init_default_standorte

def migrate_csv_to_sqlite(csv_dir: str):
    """Migriert alle CSV-Dateien zu SQLite."""
    print("🚀 Starte Migration von CSV zu SQLite...")
    
    # Initialisiere Datenbank
    init_database()
    init_default_standorte()
    print("✅ Datenbank initialisiert")
    
    # Finde alle CSV-Dateien
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    print(f"📁 Gefunden: {len(csv_files)} CSV-Dateien")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    total_rows = 0
    
    for csv_file in sorted(csv_files):
        month = csv_file.replace('.csv', '')
        filepath = os.path.join(csv_dir, csv_file)
        
        print(f"\n📄 Verarbeite: {csv_file}")
        
        try:
            df = pd.read_csv(filepath, sep=';')
            rows_imported = 0
            
            for _, row in df.iterrows():
                try:
                    # Parse Datum
                    datum_str = str(row.get('Datum', '')).strip()
                    if not datum_str or datum_str == 'nan':
                        continue
                    
                    datum = datetime.strptime(datum_str, '%d.%m.%Y').date()
                    
                    # Parse numerische Werte
                    def parse_num(val):
                        if pd.isna(val) or val == '' or str(val).strip() == '':
                            return None
                        try:
                            return float(str(val).replace(',', '.').replace('€', '').strip())
                        except:
                            return None
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO kpi_data 
                        (datum, monat, standort, disponent, fahrzeuge, stopps, 
                         unverplante_stopps, kosten_fuhrpark, stoppschnitt, stoppkosten)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        datum,
                        month,
                        str(row.get('Standort', '')).strip(),
                        str(row.get('Disponent', '')).strip() if pd.notna(row.get('Disponent')) else None,
                        parse_num(row.get('Fahrzeuge')),
                        parse_num(row.get('Stopps')),
                        parse_num(row.get('Unverplante Stopps')),
                        parse_num(row.get('Kosten Fuhrpark')),
                        parse_num(row.get('Stoppschnitt')),
                        parse_num(row.get('Stoppkosten'))
                    ))
                    rows_imported += 1
                    
                except Exception as e:
                    print(f"  ⚠️ Fehler in Zeile: {e}")
                    continue
            
            print(f"  ✅ {rows_imported} Zeilen importiert")
            total_rows += rows_imported
            
        except Exception as e:
            print(f"  ❌ Fehler beim Lesen: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Migration abgeschlossen!")
    print(f"📊 Gesamt: {total_rows} Zeilen in {len(csv_files)} Monaten")

if __name__ == "__main__":
    # Standard CSV-Verzeichnis
    csv_dir = os.environ.get('CSV_DIR', '/data/monatsdaten')
    
    # Fallback für lokales Testing
    if not os.path.exists(csv_dir):
        csv_dir = os.path.join(os.path.dirname(__file__), '..', 'monatsdaten')
    
    if os.path.exists(csv_dir):
        migrate_csv_to_sqlite(csv_dir)
    else:
        print(f"❌ CSV-Verzeichnis nicht gefunden: {csv_dir}")
