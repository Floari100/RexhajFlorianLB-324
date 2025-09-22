# Diary App – LB 324

Kleine Flask-App mit Login (über App-Setting) und einfachem Tagebuch.  
Entwickelt nach Git-Workflow (**dev → PR-Checks → main**) mit **CI/CD nach Azure App Service**.

---

## 🔗 Live-Demo

- **App:** https://flos-diary-app-we-avatfyc6gshjfne7.spaincentral-01.azurewebsites.net  
- **Login:** Der Wert der App-Einstellung `PASSWORD` (bei mir: **Floari100**)

---

## 🧭 Inhalt

- [Ziele / Lernziele](#-ziele--lernziele)
- [Technik-Stack](#-technik-stack)
- [Projektstruktur](#-projektstruktur)
- [Quickstart (lokal)](#-quickstart-lokal)
- [Qualitätssicherung](#-qualitätssicherung)
- [Git-Workflow](#-git-workflow)
- [CI/CD-Pipeline](#-cicd-pipeline)
- [Azure-Konfiguration](#-azure-konfiguration)
- [Secrets (GitHub)](#-secrets-github)
- [Releases & SemVer](#-releases--semver)
- [Troubleshooting](#-troubleshooting)
- [Screenshots (Belege)](#-screenshots-belege)

---

## 🎯 Ziele / Lernziele

- **Git & Branching:** Arbeit auf `dev`, Merge per Pull Request, **PR-Checks** (Tests).  
- **Qualität:** Formatierung/Linting via **pre-commit**; **pytest** lokal & in CI.  
- **CI/CD:** Automatischer Deploy nach Azure beim Push auf `main` (GitHub Actions).  
- **Konfiguration:** Geheimnisse via **GitHub Secrets**, App-Settings in **Azure** (kein Passwort im Code).  
- **Release:** Versionierung nach **Semantic Versioning**.

---

## 🧰 Technik-Stack

- **Python 3.11**, **Flask 3**, **pytest**
- **gunicorn** als Produktions-WSGI
- **GitHub Actions** (Build, Test, Deploy)
- **Azure App Service – Linux / Python 3.11**
- **pre-commit**: black, isort, flake8, pytest-on-push

---

## 🗂 Projektstruktur

├── app.py # Flask-App (WSGI: app)                                  
├── templates/                                              
│ └── index.html                                         
├── tests/                                     
│ └── test_add_entry_with_happiness.py                                     
├── requirements.txt                                     
├── .pre-commit-config.yaml                                     
├── .github/                                     
│ └── workflows/                                     
│ ├── deploy-on-main.yml # Deploy (main)                                     
│ └── pr-checks.yml # PR-Checks (dev)                                     
└── README.md                                     

## App-Setting & Tests
 Login-Passwort lokal als Env-Var setzen:
export PASSWORD=Floari100            # PowerShell: $env:PASSWORD="Floari100"

 Tests ausführen
python -m pytest -q
3) Starten (lokal)
flask --app app run                  # oder: python app.py
 http://127.0.0.1:5000

## Setup
python -m venv .venv
source .venv/bin/activate     Windows: .venv\Scripts\activate
pip install -r requirements.txt

 App-Setting lokal setzen (Login-Passwort)
export PASSWORD=Floari100      PowerShell: $env:PASSWORD="Floari100"

 Tests
pytest -q

 App starten
flask --app app run            oder: python app.py
http://127.0.0.1:5000

pre-commit installiert Hooks für black, isort, flake8.
pre-push führt pytest aus.

Installieren (einmalig):
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push

## Git-Workflow
Feature‐Entwicklung: Branch von dev
PR nach dev: PR-Checks (Tests) müssen grün sein
Merge nach main: triggert Deploy zur Azure-App
Beispiel:
git checkout -b feature/xyz dev
 ... commit ...
git push -u origin feature/xyz
 PR auf GitHub -> dev

## CI/CD-Pipeline
PR Checks (dev)
- Setup Python
- pip install -r requirements.txt
- python -m pytest -q
Deploy to Azure (main)
- Build & Tests wie oben
- App zippen
- ZipDeploy zur Azure Kudu-API (stabil, kein app-name-Mismatch)
Ergebnis: Push auf main ⇒ App ist automatisch online.


## ☁️ Azure-Konfiguration

**Web-App (Linux / Python 3.11)**

### Anwendungseinstellungen (App Settings)
Trage diese Werte in Azure → *Umgebungsvariablen* (bzw. *Konfiguration → Anwendungseinstellungen*) ein und **speichere + starte neu**:
- `PASSWORD` = Floari100
- `SCM_DO_BUILD_DURING_DEPLOYMENT` = `1`   <!-- erzwingt Oryx-Build auf dem Server -->
- `ENABLE_ORYX_BUILD` = `true`             <!-- optional, schadet nicht -->

> **Hinweis:** Das Passwort steht **nicht** im Code, sondern nur hier als App-Setting.

### Allgemeine Einstellungen (Startup)
Azure → *Konfiguration → Allgemeine Einstellungen*:
- **Stapel:** Python  
- **Hauptversion:** 3  
- **Nebenversion:** **3.11**
- **Startbefehl:**
  ```bash
  gunicorn --bind=0.0.0.0 --timeout 600 app:app

  <img width="1418" height="647" alt="image" src="https://github.com/user-attachments/assets/d5ac9b33-62ec-4c26-b5e6-6b47c5cf093b" />
