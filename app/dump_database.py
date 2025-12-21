#!/usr/bin/env python3
"""
Datenbank-Extraktions-Script
Dumpt alle Daten aus der KPI-Datenbank für Backup/Recovery
"""
import sqlite3
import json
import os
from datetime import datetime

DATABASE_PATH = os.environ.get('DATABASE_PATH', '/data/kpi_dashboard.db')
OUTPUT_PATH = '/data/database_dump_{}.json'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

def dump_database():
    """Exportiert die gesamte Datenbank als JSON."""
    print(f"=== Datenbank-Dump ===")
    print(f"Quelle: {DATABASE_PATH}")
    print(f"Ziel: {OUTPUT_PATH}")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Sammle alle Daten
        dump_data = {}
        
        # KPI-Daten
        cursor.execute('SELECT * FROM kpi_data ORDER BY datum, standort')
        kpi_rows = cursor.fetchall()
        dump_data['kpi_data'] = [dict(row) for row in kpi_rows]
        print(f"✓ KPI-Daten: {len(kpi_rows)} Einträge")
        
        # Prüfe Dezember-Daten speziell
        cursor.execute('''
            SELECT datum, COUNT(*) as count 
            FROM kpi_data 
            WHERE monat = '2025-12' 
            GROUP BY datum 
            ORDER BY datum
        ''')
        dec_dates = cursor.fetchall()
        print(f"\n=== Dezember 2025 Daten ===")
        for row in dec_dates:
            print(f"  {row['datum']}: {row['count']} Einträge")
        
        # Standorte
        cursor.execute('SELECT * FROM standorte')
        standorte = cursor.fetchall()
        dump_data['standorte'] = [dict(row) for row in standorte]
        print(f"\n✓ Standorte: {len(standorte)} Einträge")
        
        # Disponenten
        cursor.execute('SELECT * FROM disponenten')
        disponenten = cursor.fetchall()
        dump_data['disponenten'] = [dict(row) for row in disponenten]
        print(f"✓ Disponenten: {len(disponenten)} Einträge")
        
        # Users
        cursor.execute('SELECT id, username, role, created_at FROM users')
        users = cursor.fetchall()
        dump_data['users'] = [dict(row) for row in users]
        print(f"✓ Benutzer: {len(users)} Einträge")
        
        # Audit Log
        cursor.execute('SELECT * FROM audit_log ORDER BY created_at DESC LIMIT 1000')
        audit = cursor.fetchall()
        dump_data['audit_log'] = [dict(row) for row in audit]
        print(f"✓ Audit Log: {len(audit)} Einträge (letzte 1000)")
        
        conn.close()
        
        # Speichere als JSON
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(dump_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n✅ Dump erfolgreich gespeichert: {OUTPUT_PATH}")
        
        # Zeige auch CSV-Export an
        print(f"\n=== Dezember-Daten zur Ansicht ===")
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT datum, standort, disponent, fahrzeuge, stopps, 
                   unverplante_stopps, kosten_fuhrpark
            FROM kpi_data 
            WHERE monat = '2025-12' AND datum >= '2025-12-05' AND datum <= '2025-12-21'
            ORDER BY datum, standort
        ''')
        rows = cursor.fetchall()
        if rows:
            print(f"Gefundene Einträge vom 05.12 bis 21.12: {len(rows)}")
            for row in rows[:20]:  # Zeige erste 20
                print(f"  {row}")
        else:
            print("❌ KEINE DATEN gefunden für 05.12-21.12!")
        conn.close()
        
        return OUTPUT_PATH
        
    except Exception as e:
        print(f"❌ Fehler beim Dump: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    dump_database()
