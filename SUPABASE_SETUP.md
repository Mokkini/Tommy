# 🚀 Supabase Setup für KPI Dashboard

## Was ist Supabase?
**Supabase = Firebase Alternative** mit PostgreSQL Datenbank
- ✅ **500 MB** kostenloses PostgreSQL
- ✅ **Unbegrenzte Records**
- ✅ **Auto-Backups**
- ✅ **Schnelle API**
- ✅ **Kostenlos für immer**

---

## 📋 Setup in 5 Minuten

### 1️⃣ Supabase Account erstellen

1. Gehe zu [supabase.com](https://supabase.com)
2. **Start your project** klicken
3. Login mit GitHub
4. **New Project** erstellen:
   - **Name**: `kpi-dashboard`
   - **Database Password**: Generiere ein starkes Passwort (SPEICHERN!)
   - **Region**: `Frankfurt` (oder nächste)
   - **Plan**: Free
5. Warte ~2 Minuten bis Projekt erstellt ist

### 2️⃣ Connection String holen

1. In deinem Supabase Projekt → **Settings** → **Database**
2. Scrolle zu **Connection string**
3. Wähle **URI** (nicht Pooler!)
4. Kopiere die Connection String:
   ```
   postgresql://postgres:[PASSWORT]@db.xxx.supabase.co:5432/postgres
   ```
5. Ersetze `[PASSWORT]` mit deinem DB-Passwort aus Schritt 1

### 3️⃣ Datenbank aktivieren

In deinem Projekt:
1. Code anpassen für Supabase
2. Environment Variable setzen

---

## 💻 Code anpassen

### Option A: Nur Supabase nutzen (Empfohlen)

**Schritt 1:** Benenne die Dateien um:
```bash
# Im app/ Ordner
mv database.py database_sqlite.py.backup
mv database_supabase.py database.py
```

**Schritt 2:** Fertig! Der Code nutzt jetzt PostgreSQL statt SQLite.

### Option B: Beide Versionen behalten

In [app.py](app.py) Zeile 14:
```python
# Von:
from database import ...

# Zu:
from database_supabase import ...
```

---

## 🔧 Environment Variables

### Lokal testen

Erstelle `.env` Datei:
```bash
DATABASE_URL=postgresql://postgres:DEIN_PASSWORT@db.xxx.supabase.co:5432/postgres
ADMIN_PASSWORD=dein-admin-pw
USER_PASSWORD=dein-dispo-pw
```

### Vercel Deployment

1. Gehe zu [vercel.com](https://vercel.com) → Dein Projekt
2. **Settings** → **Environment Variables**
3. Füge hinzu:

```
DATABASE_URL = postgresql://postgres:DEIN_PASSWORT@db.xxx.supabase.co:5432/postgres
ADMIN_PASSWORD = dein-admin-passwort
USER_PASSWORD = dein-dispo-passwort
```

4. **Redeploy** auslösen (Settings → Deployments → ... → Redeploy)

---

## ✅ Testen

### Lokal:
```bash
# Installiere Dependencies
pip install -r app/requirements.txt

# Starte App
streamlit run app/app.py
```

Beim ersten Start werden automatisch:
- ✅ Tabellen erstellt
- ✅ Standorte angelegt
- ✅ Indizes erstellt

### Auf Vercel:
Nach dem Redeploy sollte alles funktionieren!

---

## 🔍 Datenbank ansehen

### In Supabase Dashboard:
1. Gehe zu **Table Editor**
2. Siehst du alle Tabellen:
   - `kpi_data` - Deine KPI-Daten
   - `standorte` - Standorte
   - `users` - Login-Daten
   - `audit_log` - Änderungsprotokoll

### Mit SQL Query:
Im **SQL Editor**:
```sql
-- Alle Standorte anzeigen
SELECT * FROM standorte;

-- KPI Daten anzeigen
SELECT * FROM kpi_data ORDER BY datum DESC LIMIT 10;

-- Wie viele Records?
SELECT COUNT(*) FROM kpi_data;
```

---

## 🚀 Vorteile gegenüber SQLite

| Feature | SQLite (Vercel) | Supabase PostgreSQL |
|---------|-----------------|---------------------|
| Persistenz | ❌ Geht verloren | ✅ Persistent |
| Concurrent Users | ⚠️ Probleme | ✅ Kein Problem |
| Backups | ❌ Manuell | ✅ Automatisch |
| Web-Interface | ❌ Nein | ✅ Ja |
| SQL-Features | ⚠️ Basic | ✅ Full PostgreSQL |
| Scalability | ❌ Nein | ✅ Ja |

---

## 📊 Migration von CSV-Daten

Falls du CSV-Daten aus `monatsdaten/` importieren willst:

```python
# migration_script.py
import pandas as pd
from app.database import save_month_data
import os

# Für jeden CSV
for csv_file in os.listdir('monatsdaten'):
    if csv_file.endswith('.csv'):
        month = csv_file.replace('.csv', '')  # z.B. "2025-12"
        df = pd.read_csv(f'monatsdaten/{csv_file}')
        save_month_data(month, df)
        print(f"✓ {month} importiert")
```

---

## 🆘 Troubleshooting

### "Connection refused"
- Prüfe ob `DATABASE_URL` korrekt ist
- Prüfe ob Passwort korrekt (ohne Klammern!)
- Warte 2-3 Min nach Projekt-Erstellung

### "SSL required"
Füge am Ende der Connection String hinzu:
```
?sslmode=require
```

### "Too many connections"
Das passiert nicht mit dem Connection Pool in `database_supabase.py` ✅

### Tabellen werden nicht erstellt
Logs prüfen in Vercel oder lokal. Die `init_database()` Funktion sollte automatisch laufen.

---

## 💡 Nächste Schritte

1. ✅ Supabase Projekt erstellt
2. ✅ Connection String kopiert
3. ✅ Code auf `database_supabase.py` umgestellt
4. ✅ Environment Variables in Vercel gesetzt
5. ✅ Redeploy
6. 🎉 **Dashboard läuft mit persistenter DB!**

---

## 📈 Monitoring

### In Supabase:
- **Database** → **Usage** - Speicherplatz prüfen
- **Logs** - Queries & Errors sehen
- **API** → **Logs** - API Calls tracken

### Limits im Free Tier:
- ✅ 500 MB Speicher
- ✅ 2 GB Transfer/Monat
- ✅ 50 MB Dateien
- ✅ 50,000 MAUs (Monthly Active Users)

**Für dein Dashboard mehr als genug!** 🚀

---

**Viel Erfolg! Bei Problemen melde dich.** 🎉
