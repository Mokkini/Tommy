# 🚀 KPI Dashboard - Synology NAS Deployment

## Voraussetzungen

- Synology NAS mit **Docker** (Container Manager)
- Zugriff auf DSM (DiskStation Manager)
- Port 8501 in der Fritz!Box freigegeben ✅

---

## Schritt 1: Dateien auf NAS kopieren

### Option A: Per File Station

1. Öffne **File Station** in DSM
2. Erstelle einen Ordner: `/docker/kpi-dashboard`
3. Lade alle Dateien aus dem `docker/` Ordner hoch:
   - `app.py`
   - `database.py`
   - `auth.py`
   - `migrate.py`
   - `requirements.txt`
   - `Dockerfile`
   - `docker-compose.yml`

4. Erstelle einen Ordner für die Daten: `/docker/kpi-dashboard/data`
5. Kopiere deine CSV-Dateien nach: `/docker/kpi-dashboard/monatsdaten/`

### Option B: Per SSH/SCP

```bash
scp -r docker/* benutzer@NAS-IP:/volume1/docker/kpi-dashboard/
scp -r monatsdaten benutzer@NAS-IP:/volume1/docker/kpi-dashboard/
```

---

## Schritt 2: Docker Container erstellen

### Option A: Container Manager (DSM 7.2+)

1. Öffne **Container Manager** in DSM
2. Gehe zu **Projekt**
3. Klicke **Erstellen**
4. Name: `kpi-dashboard`
5. Pfad: `/docker/kpi-dashboard`
6. Wähle die `docker-compose.yml` aus
7. Klicke **Erstellen**

### Option B: Per SSH

```bash
# SSH-Verbindung zur NAS
ssh benutzer@NAS-IP

# Zum Projektordner wechseln
cd /volume1/docker/kpi-dashboard

# Container bauen und starten
sudo docker-compose up -d --build
```

---

## Schritt 3: Daten migrieren (einmalig)

Falls du bestehende CSV-Daten hast:

```bash
# Per SSH auf der NAS
cd /volume1/docker/kpi-dashboard
sudo docker exec -it kpi-dashboard python migrate.py
```

Oder manuell in Container Manager:
1. Wähle den Container `kpi-dashboard`
2. Klicke auf **Terminal**
3. Führe aus: `python migrate.py`

---

## Schritt 4: Zugriff testen

### Lokal (im Netzwerk)
```
http://192.168.178.77:8501
```

### Extern (über DDNS)
```
http://dispo.myds.me:8501
```

---

## 🔐 Login-Daten

Standard-Zugangsdaten (können in docker-compose.yml geändert werden):

| Benutzer | Passwort |
|----------|----------|
| `admin` | `dispo2025` |
| `dispo` | `kpi123` |

### Passwort ändern

In `docker-compose.yml`:
```yaml
environment:
  - ADMIN_PASSWORD=dein_neues_passwort
  - USER_PASSWORD=anderes_passwort
```

Dann Container neu starten:
```bash
sudo docker-compose down
sudo docker-compose up -d
```

---

## 🔧 Wartung & Troubleshooting

### Logs anzeigen
```bash
sudo docker logs kpi-dashboard
```

### Container neu starten
```bash
sudo docker-compose restart
```

### Container stoppen
```bash
sudo docker-compose down
```

### Datenbank sichern
Die Datenbank liegt in `/docker/kpi-dashboard/data/kpi_dashboard.db`

```bash
# Backup erstellen
cp /volume1/docker/kpi-dashboard/data/kpi_dashboard.db \
   /volume1/docker/kpi-dashboard/backup/kpi_dashboard_$(date +%Y%m%d).db
```

---

## 🔒 HTTPS aktivieren (optional, empfohlen)

### Über Synology Reverse Proxy

1. DSM → **Systemsteuerung** → **Anmeldeportal** → **Erweitert**
2. Klicke auf **Reverse Proxy**
3. **Erstellen**:
   - Beschreibung: `KPI Dashboard`
   - Quelle:
     - Protokoll: `HTTPS`
     - Hostname: `dispo.myds.me`
     - Port: `443`
   - Ziel:
     - Protokoll: `HTTP`
     - Hostname: `localhost`
     - Port: `8501`
4. **Speichern**

### Let's Encrypt Zertifikat

1. DSM → **Systemsteuerung** → **Sicherheit** → **Zertifikat**
2. **Hinzufügen** → **Neues Zertifikat hinzufügen**
3. **Zertifikat von Let's Encrypt abrufen**
4. Domainname: `dispo.myds.me`
5. E-Mail eingeben → **Fertig**

Dann ist dein Dashboard erreichbar unter:
```
https://dispo.myds.me
```
(Ohne Port!)

---

## 📁 Ordnerstruktur auf der NAS

```
/volume1/docker/kpi-dashboard/
├── app.py                 # Hauptanwendung
├── database.py            # Datenbankfunktionen
├── auth.py                # Login-System
├── migrate.py             # CSV→SQLite Migration
├── requirements.txt       # Python Dependencies
├── Dockerfile             # Docker Build
├── docker-compose.yml     # Docker Compose Config
├── data/                  # Persistente Daten
│   └── kpi_dashboard.db   # SQLite Datenbank
└── monatsdaten/           # CSV-Dateien (für Migration)
    ├── 2025-10.csv
    ├── 2025-11.csv
    └── 2025-12.csv
```

---

## ❓ FAQ

**Q: Der Container startet nicht?**
A: Prüfe die Logs: `docker logs kpi-dashboard`

**Q: Ich kann nicht von extern zugreifen?**
A: Prüfe die Portfreigabe in der Fritz!Box (Port 8501)

**Q: Die Datenbank ist leer?**
A: Führe die Migration aus: `docker exec -it kpi-dashboard python migrate.py`

**Q: Wie ändere ich die Standorte?**
A: In `database.py` die Funktion `init_default_standorte()` anpassen

---

## 📞 Support

Bei Fragen oder Problemen: [Dokumentation anpassen]

---

*Erstellt am: Dezember 2025*
*Version: 2.0 (SQLite Edition)*
