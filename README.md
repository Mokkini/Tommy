# � KPI Dashboard - Logistik

**Multi-Standort KPI Dashboard** für Dispositionsplanung mit Live-Datenbank

🌐 **Live-App:** https://dispokpi.streamlit.app

## ✨ Stack

- **Frontend:** Streamlit Community Cloud
- **Backend:** Supabase PostgreSQL (500MB Free Tier)
- **Auth:** Session-basiertes Login (Admin/Dispo Rollen)
- **Deployment:** Auto-Deploy via GitHub
- **Kosten:** 100% Kostenlos! 🎉

---

## 🚀 Quick Start (3 Schritte)

### 1️⃣ Supabase Database Setup

1. Erstelle Account bei [supabase.com](https://supabase.com)
2. Neues Projekt anlegen (Region: EU)
3. Gehe zu **Settings** → **Database**
4. Kopiere **Session Pooler Connection String**:
   ```
   postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-x-xx-xxxx.pooler.supabase.com:5432/postgres
   ```
5. Ersetze `[YOUR-PASSWORD]` mit deinem DB-Passwort

📖 **Detaillierte Anleitung:** [SUPABASE_SETUP.md](SUPABASE_SETUP.md)

### 2️⃣ GitHub Repository Public machen

1. Gehe zu GitHub → Repository Settings
2. Scrolle zu **Danger Zone** → **Change visibility**
3. Wähle **"Make public"**

### 3️⃣ Streamlit Cloud Deployment

1. Gehe zu [share.streamlit.io](https://share.streamlit.io)
2. Klicke **"New app"**
3. Wähle Repository: `dein-username/Tommy`
4. **Main file path:** `app/app.py`
5. **Branch:** `main`
6. Klicke **Advanced settings** → **Secrets**
7. Füge ein:
   ```toml
   DATABASE_URL = "postgresql://postgres.xxxxx:PASSWORT@aws-x-xx-xxxx.pooler.supabase.com:5432/postgres"
   ADMIN_PASSWORD = "admin2025"
   USER_PASSWORD = "dispo2025"
   ```
8. Klicke **Deploy**

**🎉 Fertig!** App läuft in 2-3 Minuten unter `https://dein-app-name.streamlit.app`

---

## 📊 Features

### Daten-Management
- ✅ Tägliche KPI-Erfassung für 9 Standorte
- ✅ Inline-Bearbeitung mit Live-Validierung
- ✅ Automatische Berechnungen (Stoppschnitt, Stoppkosten)
- ✅ Werktags-Filter (Mo-Fr automatisch)
- ✅ Bulk-Import via CSV/Excel

### Reporting & Analytics
- ✅ **Daily Report:** Tagesübersicht mit Vormonats-Deltas
- ✅ **Wochenvergleich:** Trend-Diagramme & Performance
- ✅ **Monatsvergleich:** KPI-Heatmaps & Rankings
- ✅ **KPI Verlauf:** Zeitreihen-Analysen
- ✅ Excel & CSV Export

### System
- ✅ Session-basiertes Login (Admin/Dispo Rollen)
- ✅ Persistent via Supabase PostgreSQL
- ✅ Audit-Log für alle Änderungen
- ✅ Responsive Design für Mobile/Tablet
- ✅ Connection Pooling für Performance

---

## 👤 Standard-Login

| Rolle | Username | Passwort | Berechtigungen |
|-------|----------|----------|----------------|
| Admin | `admin`  | `admin2025` | Vollzugriff (Anlegen, Ändern, Löschen) |
| Dispo | `dispo`  | `dispo2025` | Lesen + Bearbeiten |

⚠️ **Wichtig:** Passwörter über Streamlit Secrets ändern!

---

## 💻 Lokale Entwicklung

```bash
# 1. Repository klonen
git clone https://github.com/dein-username/Tommy.git
cd Tommy

# 2. .env Datei erstellen
cat > .env << EOF
DATABASE_URL=postgresql://postgres.xxxxx:PASSWORT@aws-x-xx-xxxx.pooler.supabase.com:5432/postgres
ADMIN_PASSWORD=admin2025
USER_PASSWORD=dispo2025
EOF

# 3. Virtual Environment & Dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r app/requirements.txt

# 4. App starten
streamlit run app/app.py
```

Öffne: **http://localhost:8501**

---

## 🔄 Updates deployen

**Super einfach:**

```bash
git add .
git commit -m "Meine Änderungen"
git push
```

Streamlit Cloud deployt **automatisch** in ~1 Minute! ⚡

Logs: https://share.streamlit.io → Manage app → Logs

---

## 📁 Projekt-Struktur

```
Tommy/
├── .streamlit/
│   └── secrets.toml             # Lokale Secrets (nicht in Git!)
├── app/
│   ├── app.py                   # Haupt-Streamlit App (476 Zeilen)
│   ├── database.py              # PostgreSQL Handler mit Connection Pool
│   ├── auth.py                  # Session-Login System
│   ├── migrate.py               # Datenbank-Migrations Script
│   ├── dump_database.py         # Backup-Tool
│   └── requirements.txt         # Python Dependencies
├── monatsdaten/
│   ├── 2025-10.csv             # Historische Daten (optional)
│   ├── 2025-11.csv
│   └── 2025-12.csv
├── .gitignore                   # .env und Secrets ausgeschlossen
├── README.md                    # Diese Datei
├── SUPABASE_SETUP.md           # Detaillierte DB-Anleitung
└── vercel.json                  # (Veraltet, nicht verwendet)
```

---

## 🗄️ Datenbank-Schema

### Tabellen

**kpi_data** - Haupt-KPI-Daten
```sql
- id (SERIAL PRIMARY KEY)
- datum (DATE) - Werktag
- standort (VARCHAR) - 9 Standorte
- disponent (VARCHAR)
- fahrzeuge (INTEGER)
- stopps (INTEGER)
- unverplante_stopps (INTEGER)
- kosten_fuhrpark (NUMERIC)
- stoppschnitt (NUMERIC) - Berechnet: Stopps ÷ Fahrzeuge
- stoppkosten (NUMERIC) - Berechnet: Kosten ÷ Stopps
- created_at, updated_at (TIMESTAMP)
- UNIQUE(datum, standort) - Verhindert Duplikate
```

**standorte** - Standort-Verwaltung  
**disponenten** - Disponenten-Verwaltung  
**users** - Login-Credentials (bcrypt-gehashed)  
**audit_log** - Änderungsprotokoll

### Datenbank ansehen

**Supabase Dashboard:**
1. https://supabase.com/dashboard
2. **Table Editor** → Alle Tabellen direkt sichtbar
3. **SQL Editor** → Custom Queries möglich

---

## 🔧 Konfiguration

### Umgebungsvariablen (Streamlit Secrets)

```toml
DATABASE_URL = "postgresql://..."    # Supabase Session Pooler URL
ADMIN_PASSWORD = "..."               # Admin Login
USER_PASSWORD = "..."                # Dispo Login
```

**Wichtig:**
- Nutze **Session Pooler** URL (Port 5432, nicht 6543)
- Format: `aws-x-eu-xxxx.pooler.supabase.com`
- Niemals Direct Connection URL in Cloud!

### Secrets ändern

**Streamlit Cloud:**
1. Manage app → Settings → Secrets
2. Secrets ändern → Save
3. Reboot app (⋮ → Reboot)

**Lokal:**
- `.env` Datei bearbeiten (nicht in Git committen!)

---

## 🆘 Troubleshooting

### ❌ "DATABASE_URL is empty!"
**Lösung:** Secrets nicht gespeichert
- Streamlit: Settings → Secrets → Save klicken
- Lokal: `.env` Datei prüfen

### ❌ "Tenant or user not found"
**Lösung:** Falsche Connection URL
- Nutze **Session Pooler** (Port 5432)
- Username muss Format haben: `postgres.projektid`
- Prüfe: Supabase Dashboard → Database Settings → Connection string

### ❌ "Cannot assign requested address"
**Lösung:** IPv6 Problem
- Direct Connection funktioniert nicht von Streamlit Cloud
- Wechsel zu Session Pooler URL

### ❌ Login funktioniert nicht
- Prüfe ADMIN_PASSWORD / USER_PASSWORD in Secrets
- Standard: `admin2025` / `dispo2025`
- Session löschen: Browser-Cache leeren

### 📝 Logs prüfen

**Streamlit Cloud:**
- Manage app → Logs (rechts unten)
- Suche nach `DATABASE_URL loaded:` für Debug-Info

**Lokal:**
- Terminal Output beachten
- Streamlit zeigt Errors im Browser

---

## 📚 Weiterführende Docs

- **[SUPABASE_SETUP.md](SUPABASE_SETUP.md)** - Schritt-für-Schritt Datenbank Setup
- **[app/SYNOLOGY_ANLEITUNG.md](app/SYNOLOGY_ANLEITUNG.md)** - Docker Deployment (optional)

---

## 🎯 Tech Stack Details

| Komponente | Technologie | Version | Zweck |
|------------|-------------|---------|-------|
| **Frontend** | Streamlit | 1.52.2 | Web-UI Framework |
| **Database** | PostgreSQL (Supabase) | 15 | Persistent Storage |
| **DB Driver** | psycopg2-binary | 2.9.11 | PostgreSQL Connector |
| **Data Processing** | pandas | 2.3.3 | DataFrame Operations |
| **Visualisierung** | altair | 6.0.0 | Charts & Graphs |
| **Export** | openpyxl | 3.1.5 | Excel Files |
| **Hosting** | Streamlit Cloud | - | Free Tier |
| **CI/CD** | GitHub | - | Auto-Deploy |

**Warum dieser Stack?**
- ✅ 100% kostenlos (keine Kreditkarte nötig)
- ✅ Production-ready (SSL, Backups, Monitoring inklusive)
- ✅ Auto-Deploy (Push = Live in 1 Minute)
- ✅ Einfach wartbar (kein Docker/Server-Management)

---

## 🚀 Performance

- **Connection Pooling:** 1-10 parallele DB-Connections
- **Session Pooler:** Optimiert für Long-Running Apps
- **Caching:** Streamlit `@st.cache_data` für statische Daten
- **Lazy Loading:** Monatsdaten nur bei Bedarf laden

---

## 🔐 Sicherheit

- ✅ Passwörter nur in Streamlit Secrets (nie im Code)
- ✅ `.env` und `secrets.toml` in `.gitignore`
- ✅ SSL/TLS verschlüsselte DB-Verbindung
- ✅ Session-basierte Authentifizierung
- ✅ Input-Validierung gegen SQL-Injection
- ✅ HTTPS-Only Deployment

---

**🎉 Viel Erfolg mit deinem KPI Dashboard!**

Bei Fragen: GitHub Issues oder Pull Requests welcome! 💪

*Bei Fragen → Issue öffnen oder Doku checken*
