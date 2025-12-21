# 🚀 KPI Dashboard - Streamlit + Supabase

**Logistik KPI Dashboard** mit PostgreSQL Datenbank

## ✨ Stack

- **Frontend:** Streamlit auf Vercel
- **Backend:** Supabase (PostgreSQL)
- **Auth:** Login-System (Admin/Dispo)
- **Kosten:** 100% Kostenlos! 🎉

---

## ⚡ Quick Start (3 Schritte)

### 1️⃣ Supabase Setup (5 Min)

Folge: **[SUPABASE_SETUP.md](SUPABASE_SETUP.md)**

**TL;DR:**
1. Account bei [supabase.com](https://supabase.com) erstellen
2. Neues Projekt → Connection String kopieren
3. Fertig!

### 2️⃣ Code vorbereiten

```bash
# Database auf Supabase umschalten
cd app
mv database.py database_sqlite.backup
mv database_supabase.py database.py
cd ..

# Git Push
git add .
git commit -m "Supabase Integration"
git push
```

### 3️⃣ Vercel Deployment

1. [vercel.com/new](https://vercel.com/new) → Import Repo
2. **Environment Variables** setzen:
   ```
   DATABASE_URL = postgresql://postgres:PASSWORT@db.xxx.supabase.co:5432/postgres
   ADMIN_PASSWORD = dein-admin-passwort
   USER_PASSWORD = dein-dispo-passwort
   ```
3. **Deploy** klicken

**🎉 Fertig!** Dashboard läuft unter `https://dein-projekt.vercel.app`

---

## 📊 Features

- ✅ Tägliche KPI-Erfassung pro Standort
- ✅ Inline-Bearbeitung mit Validierung
- ✅ Daily Report mit Vormonats-Deltas
- ✅ Wochenvergleich & Trend-Diagramme
- ✅ Monatsvergleich & KPI-Heatmaps
- ✅ Excel & CSV Export
- ✅ Login-System (Admin/Dispo-Rollen)
- ✅ **Persistent** via Supabase PostgreSQL
- ✅ Audit-Log für Änderungen
- ✅ Responsive Design

---

## 👤 Login

| User  | Username | Passwort |
|-------|----------|----------|
| Admin | `admin`  | In Vercel ENV gesetzt |
| Dispo | `dispo`  | In Vercel ENV gesetzt |

---

## 💻 Lokale Entwicklung

```bash
# .env Datei erstellen
DATABASE_URL=postgresql://postgres:xxx@db.xxx.supabase.co:5432/postgres
ADMIN_PASSWORD=test123
USER_PASSWORD=test456

# Dependencies installieren
pip install -r app/requirements.txt

# App starten
streamlit run app/app.py
```

Öffne: http://localhost:8501

---

## 🔄 Updates deployen

So einfach:

```bash
git add .
git commit -m "Meine Änderungen"
git push
```

Vercel deployt **automatisch** in ~30 Sekunden! ⚡

---

## 📁 Projekt-Struktur

```
kpi-dashboard/
├── app/                          # Streamlit App
│   ├── app.py                   # Haupt-App
│   ├── database_supabase.py     # PostgreSQL Handler
│   ├── database_sqlite.backup   # SQLite Backup
│   ├── auth.py                  # Login System
│   ├── Dockerfile               # Optional: Docker
│   └── requirements.txt         # Python Dependencies
├── deployment/                   # Optional: Oracle Cloud
├── monatsdaten/                 # CSV Daten (falls Migration)
├── vercel.json                  # Vercel Config
├── SUPABASE_SETUP.md            # Setup-Anleitung
├── GIT_VERCEL_GUIDE.md          # Git/Vercel Anleitung
└── README.md                    # Diese Datei
```

---

## 🗄️ Datenbank

### Was wird gespeichert?

- **kpi_data**: Tägliche KPI-Werte (Fahrzeuge, Stopps, Kosten, etc.)
- **standorte**: Standort-Verwaltung
- **disponenten**: Disponenten-Verwaltung
- **users**: Login-Daten (Admin/Dispo)
- **audit_log**: Änderungsprotokoll

Details: [DATABASE_ANALYSIS.md](DATABASE_ANALYSIS.md)

### Datenbank ansehen

In Supabase Dashboard → **Table Editor** → Alle Tabellen sichtbar!

---

## 🆘 Troubleshooting

### Database Connection Error

- Prüfe `DATABASE_URL` in Vercel Environment Variables
- Prüfe ob Passwort korrekt (ohne `[` `]`)
- Füge `?sslmode=require` ans Ende der URL

### App startet nicht

Logs prüfen:
- Vercel: Dashboard → Deployments → Logs
- Lokal: Terminal Output

### Tabellen werden nicht erstellt

Die `init_database()` Funktion läuft automatisch beim Start. Prüfe Logs.

---

## 📚 Dokumentation

- **[SUPABASE_SETUP.md](SUPABASE_SETUP.md)** - Detailliertes Supabase Setup
- **[GIT_VERCEL_GUIDE.md](GIT_VERCEL_GUIDE.md)** - Git & Vercel Workflows
- **[DATABASE_ANALYSIS.md](DATABASE_ANALYSIS.md)** - DB-Struktur & Alternativen
- **[VERCEL_DEPLOY.md](VERCEL_DEPLOY.md)** - Quick Deploy Reference

---

## 🎯 Warum Supabase + Vercel?

| Feature | Lösung | Kosten |
|---------|--------|--------|
| Frontend Hosting | Vercel | ✅ Free |
| SSL/HTTPS | Vercel | ✅ Inklusive |
| Database | Supabase PostgreSQL | ✅ Free (500MB) |
| Auto-Deploy | GitHub + Vercel | ✅ Inklusive |
| Backups | Supabase | ✅ Automatisch |
| Monitoring | Beide Dashboards | ✅ Inklusive |

**Total: 0€/Monat** - Production-Ready! 🚀

---

## 💡 Alternative Setups

### Oracle Cloud (Advanced)
- Setup in `deployment/` Ordner
- Für: Volle Kontrolle, eigener Server
- Auch kostenlos, aber komplexer

### Render.com (Einfacher)
- All-in-One: App + DB
- Sleep nach 15 Min (Free Tier)
- Gut für: Quick Tests

---

**🎉 Viel Erfolg mit deinem KPI Dashboard!**

*Bei Fragen → Issue öffnen oder Doku checken*
