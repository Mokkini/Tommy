# Changelog

## 21. Dezember 2025 - Vercel Ready! 🚀

### ✅ Vereinfacht für GitHub + Vercel Deployment

Das Projekt wurde drastisch vereinfacht für **1-Click Deployment** auf Vercel:

#### Neue Dateien
- ✅ `vercel.json` - Vercel Konfiguration für Streamlit
- ✅ `GIT_VERCEL_GUIDE.md` - Schritt-für-Schritt Git + Vercel Anleitung
- ✅ `VERCEL_DEPLOY.md` - Quick Reference
- ✅ Vereinfachte `README.md`

#### Deployment-Optionen

**Option 1: Vercel (Empfohlen für einfaches Setup)**
- ✅ Git Push = Auto Deploy
- ✅ Kostenloses SSL
- ✅ GitHub Integration
- ⚠️ Stateless (DB geht bei Redeploy verloren)
- 👉 Perfekt für: Demos, Testing, Read-Only

**Option 2: Oracle Cloud (Empfohlen für Production)**
- ✅ Dauerhaft kostenlos
- ✅ Persistente Datenbank
- ✅ Volle Kontrolle
- 👉 Setup in `deployment/` Ordner

### 📦 Projekt-Struktur

```
kpi-dashboard/
├── app/                      # Production App mit SQLite & Login
│   ├── app.py
│   ├── database.py
│   ├── auth.py
│   └── requirements.txt
├── deployment/               # Oracle Cloud Setup (falls Vercel nicht reicht)
│   ├── docker-compose.prod.yml
│   ├── setup.sh
│   └── ...
├── monatsdaten/             # CSV Daten
├── vercel.json              # Vercel Config
├── GIT_VERCEL_GUIDE.md      # Git + Vercel Anleitung
└── README.md                # Hauptdokumentation
```

### 🚀 Quick Start

```bash
# 1. Git Push
git init
git add .
git commit -m "Initial commit"
git push

# 2. Vercel Deploy
# → vercel.com/new → Import Repo → Deploy
```

**Fertig!** ⚡

---

## Vorherige Änderungen

### Oracle Cloud Setup (archiviert)
Komplexeres Setup mit Docker, Nginx, SSL ist noch verfügbar in:
- `deployment/` Ordner
- `archive/CHANGELOG_oracle.md`
