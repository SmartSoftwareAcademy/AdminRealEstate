# Windows Setup Guide (Beginner Friendly)

Follow this walkthrough to install and run AdminRealEstate on a Windows machine. Every command is copy-paste ready and includes context so you always know why you are running it.

## 1. Prerequisites
1. **Python 3.10+** → Download from https://www.python.org/downloads/. During installation tick **“Add Python to PATH”**.
2. **Visual C++ Build Tools** (if prompted by Python packages) → Install via https://visualstudio.microsoft.com/visual-cpp-build-tools/.
3. **MySQL Server 5.7+ / MariaDB 10.4+** → Install using MySQL Installer. Note the root password.
4. **Redis** → Use [Memurai](https://www.memurai.com/) for a native Windows port or enable WSL and install Redis inside Ubuntu (`sudo apt install redis-server`).
5. **Git** → Optional but recommended (https://git-scm.com/downloads).

### Verify installations
```powershell
python --version
mysql --version
redis-server --version  # Memurai reports as Redis as well
```

## 2. Get the Source Code
```powershell
git clone <repo-url>
cd AdminRealEstate
```
> Already have the code? `cd` into the project directory instead.

## 3. Create & Activate a Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```
To deactivate later, simply run `deactivate`.

## 4. Install Python Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If installation fails due to missing MySQL headers, install **MySQL Connector/C** from Oracle and retry.

## 5. Configure Environment Variables
Create a `.env` file beside `manage.py`:
```dotenv
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=realestate
DB_USER=root
DB_PASSWORD=<your-password>
DB_HOST=127.0.0.1
DB_PORT=3306

EMAIL_ADDRESS=<smtp-username>
EMAIL_PASSWORD=<smtp-password>

CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```
> Tip: Copy `.env.example` if you create one, then adjust for production later.

## 6. Prepare the Database
1. Start the MySQL service (Services app → “MySQL80” → Start) or run `net start MySQL80` from PowerShell.
2. Create the database schema:
   ```sql
   CREATE DATABASE realestate CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   ```
3. (Optional) Import sample data for exploration:
   ```powershell
   mysql -u root -p realestate < realestate.sql
   ```

## 7. Apply Migrations & Create a Superuser
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
Forgot the password later? Run `python manage.py changepassword <email>`.

## 8. Collect Static Assets & Ensure Media Folder
```powershell
python manage.py collectstatic --no-input
```
Make sure a `media/` folder exists (create it if missing) so uploads succeed during development.

## 9. Run the Application Stack

### 9.1 Django development server
```powershell
python manage.py runserver
```
Visit http://127.0.0.1:8000 in your browser.

### 9.2 Celery worker & beat (two terminals)
```powershell
celery -A AdminRealEstate worker -l INFO
celery -A AdminRealEstate beat -l INFO
```
Confirm Redis is running before launching these commands.

## 10. Managing Users & Passwords

| Task | Command | Notes |
| --- | --- | --- |
| Create another admin | `python manage.py createsuperuser` | Follow the prompts, supply email + password |
| Change an existing password | `python manage.py changepassword <email>` | Works for any user (staff/tenant) |
| Reset password via shell | ```python
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(email="tenant@example.com")
>>> user.set_password("NewPass123!")
>>> user.save()
``` | Use when you cannot remember the original email or want to script changes |

## 11. Optional Integrations
- **M-Pesa (Daraja API)**: Enter credentials in the Django admin under **Core → Setup**. Use https://ngrok.com to expose your callback URL while testing.
- **Email**: Populate SMTP settings in **Core → Setup**. Test with Gmail app passwords or a transactional email provider.

## 12. Common Maintenance Commands
```powershell
# Run tests
python manage.py test

# Create a database migration when models change
python manage.py makemigrations <app_label>

# Load fixtures/sample data
python manage.py loaddata path\to\fixture.json

# Dump data for backups
python manage.py dumpdata --indent 2 > backup.json
```

## 13. Troubleshooting Checklist
- **MySQL connection error** → ensure the service is running and credentials in `.env` match.
- **Redis refused connection** → start Memurai/Redis or update `CELERY_BROKER_URL` to the correct host/port.
- **Static file 404s** → rerun `collectstatic` and make sure Whitenoise is enabled (already configured in settings).
- **Email not sent** → double-check credentials in `core.Setup`; some providers require TLS/SSL-specific ports.

## 14. Keep Things Clean
- Ignore `.venv/`, `media/`, `staticfiles/`, and diagram exports (see `.gitignore`).
- Use `mysqldump realestate > backup.sql` for periodic DB backups.
- Monitor Celery worker windows for errors, especially around nightly invoice generation.
