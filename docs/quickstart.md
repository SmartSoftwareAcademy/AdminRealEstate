# Quickstart — Run AdminRealEstate (Beginner Friendly)

This quickstart contains step-by-step instructions for two common scenarios:
- Scenario A — You already have a Python virtual environment and want to *activate and run* the project.
- Scenario B — You are starting from scratch on a new machine (create venv, install dependencies, configure DB, run the app).

Commands are shown for Windows PowerShell and are copy-paste ready. Linux/macOS uses identical Python commands but activations differ slightly (see notes).

---

## Before you start (Prerequisites)
- Python 3.10+ installed and on PATH (verify `python --version`).
- MySQL / MariaDB server (or PostgreSQL if you adapt settings).
- Redis (or a Redis-compatible service).
- Git (optional) to clone the repo.

Note: If you already use Docker or WSL and prefer Linux tooling, those are fine; the steps below are written for local virtualenv setups.

---

## Scenario A — Activate an existing virtual environment
This scenario assumes someone else prepared a `venv` for this project or you have an environment available (`.venv`, `env`, `venv`, etc.).

1. Open your terminal and go to the repository root (where `manage.py` lives):
   ```powershell
   cd path\to\AdminRealEstate
   ```
2. Activate your environment (Windows PowerShell):
   ```powershell
   .\.venv\Scripts\activate    # or change `.venv` to your env folder name
   ```
   Linux/macOS: `source .venv/bin/activate`

3. Install any missing dependencies (safe to run even if already installed):
   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Prepare environment variables (if `.env` already exists, check values). Create `.env` beside `manage.py` if missing (see sample below):
   ```dotenv
   SECRET_KEY=change-me
   DEBUG=True
   DB_NAME=realestate
   DB_USER=root
   DB_PASSWORD=<your-password>
   DB_HOST=127.0.0.1
   DB_PORT=3306
   CELERY_BROKER_URL=redis://127.0.0.1:6379/0
   CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
   ```

5. Apply migrations (skip if migrations already applied and DB seeded):
   ```powershell
   python manage.py migrate
   ```

6. Create a superuser (if you need admin access):
   ```powershell
   python manage.py createsuperuser
   ```

7. Run the dev server:
   ```powershell
   python manage.py runserver
   ```

8. (Optional) Start Celery workers (in another terminal with the venv active):
   ```powershell
   celery -A AdminRealEstate worker -l INFO
   celery -A AdminRealEstate beat -l INFO
   ```

You should now be able to open http://127.0.0.1:8000 and log in.

---

## Scenario B — Start from scratch (create venv + database)
Follow these commands to create an environment from scratch.

1. Clone the repo (if you haven't already):
   ```powershell
   git clone <repo-url>
   cd AdminRealEstate
   ```
2. Create & activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Create a database and user (example MySQL commands):
   - Connect using `mysql -u root -p` then run:
     ```sql
     CREATE DATABASE realestate CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
     CREATE USER 'realestate_user'@'localhost' IDENTIFIED BY 'yourpassword';
     GRANT ALL PRIVILEGES ON realestate.* TO 'realestate_user'@'localhost';
     FLUSH PRIVILEGES;
     ```

4. Create `.env` next to `manage.py` and update DB credentials and keys as needed (see sample above).

5. Run migrations & create superuser:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. (Optional) Load sample data if `realestate.sql` is included (handy for demos):
   ```powershell
   mysql -u realestate_user -p realestate < realestate.sql
   ```

7. Collect static files and create media folder:
   ```powershell
   python manage.py collectstatic --no-input
   mkdir media
   ```

8. Run the server and (optionally) Celery as in Scenario A.

---

## Local dev tips
- If `pip install` fails with a MySQL build error, install `mysqlclient` pre-compiled wheel or use `mysql-connector-python` and adjust `requirements.txt`.
- Use `python manage.py runserver_plus` (if installed) for a better debugging workflow.
- Use `./manage.py runserver 0.0.0.0:8000` when you need LAN access.

---

## Test & QA
- Unit tests: `python manage.py test`.
- Linting & type checks: add and run your preferred tools (pre-commit hooks can be integrated).

---

## Troubleshooting quick list
- Database connection problems → Check `DB_HOST`/`DB_PORT`/user/password and ensure the DB service is running.
- Redis connection errors → Ensure Redis/Memurai is running, and urls in `.env` are accurate.
- Assets 404 → Run `python manage.py collectstatic` and ensure `STATIC_ROOT` is configured.
- Dropdowns / JS broken → Ensure `plugins/jquery/jquery.min.js` and `plugins/bootstrap/js/bootstrap.bundle.min.js` are both being loaded in `templates/core/headers.html` or `scripts.html` and that data-* attributes match the loaded Bootstrap version.

---

If you want, I can also add a short `docs/dev-checklist.md` that contains the exact commands to run before creating a PR (lint, tests, run migrations locally, smoke test the UI). Would you like that as a separate file?