
# Tagebuch-App — LB‑324 (Final)

Diese Ablage ist **1:1** auf die **LB‑324** abgestimmt.

## Admin
- Öffentliche Repo-Ablage (NameVornameLB-324) anlegen, URL sofort in Moodle; am Schluss ZIP.

## Lokal starten
(siehe oben im Haupt-README im Repo)

## Hinweise
- PR‑Checks nur auf `dev` (Tests only), Deploy auf `main`.
- PASSWORD via App Settings, Publish Profile als Secret.
- Test `test_add_entry_with_happiness.py` vorhanden.
# Setup ok ✅

## Live
https://flos-diary-app-we-avatfyc6gshjfne7.spaincentral-01.azurewebsites.net

## Lokale Entwicklung
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PASSWORD=<MEIN_GITHUB_USERNAME>
python -m pytest -q
flask --app app run  # oder: python app.py

## CI/CD
- dev: PR-Checks führen Tests aus
- main: GitHub Actions baut + ZipDeploy nach Azure (Kudu)

## Azure-Settings
- PASSWORD (App Setting): <MEIN_GITHUB_USERNAME>
- SCM_DO_BUILD_DURING_DEPLOYMENT=1
- ENABLE_ORYX_BUILD=true
- Startup: gunicorn --bind=0.0.0.0 --timeout 600 app:app

## Secrets (GitHub → Actions)
- AZURE_WEBAPP_PUBLISH_PROFILE: Inhalt aus „Veröffentlichungsprofil herunterladen“

## Troubleshooting
- Application Error → Oryx-Build aktivieren (Settings oben), neu deployen.
- 500 → Log stream prüfen (Diagnose & Problembehandlung).

