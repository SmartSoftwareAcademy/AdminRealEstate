# AdminRealEstate

AdminRealEstate is a Django-based property management platform that centralizes landlord, tenant, lease, payment, invoicing, and utility workflows. It integrates Celery for scheduled tasks (e.g., nightly invoice generation) and Redis as the task broker.

## Features
- Authenticated multi-role access built on a custom `account.CustomUser`.
- Dashboards and analytics powered by the `core` app.
- Comprehensive modules for landlords, tenants, property inventory, leases, invoices, notices, payroll, payments (including M-Pesa support), and utilities.
- Rich text editing through TinyMCE and a themed admin experience via Jazzmin.
- Background jobs handled with Celery and Redis (e.g., automated invoice generation).

## Prerequisites
- Python 3.10 or newer
- MySQL 5.7+ or MariaDB 10.4+
- Redis 5+ (for Celery broker/result backend)
- Node/Yarn are **not** required to run the project (static assets are pre-built), but you may add them if you plan to rebuild the frontend assets manually.

## Initial Setup
1. **Clone and enter the project**
   ```bash
   git clone <repo-url>
   cd AdminRealEstate
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   .\env\Scripts\activate  # Windows
   # source .env/bin/activate  # macOS/Linux
   ```
3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Environment Configuration
Create a `.env` file in the project root (next to `manage.py`) and supply the required configuration. The project currently reads some values directly from settings; moving them to environment variables is recommended.

```env
# Django
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (MySQL)
DB_NAME=realestate
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306

# Email (SMTP)
EMAIL_ADDRESS=your-smtp-username
EMAIL_PASSWORD=your-smtp-password

# Celery / Redis
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

Update `AdminRealEstate/settings.py` (or use `django-environ`) to pull from these environment variables before deploying to production.

## Database Preparation
1. Create the MySQL database and user:
   ```sql
   CREATE DATABASE realestate CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   CREATE USER 'realestate_user'@'localhost' IDENTIFIED BY 'strong-password';
   GRANT ALL PRIVILEGES ON realestate.* TO 'realestate_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
2. Optionally seed sample data using the provided `realestate.sql` dump:
   ```bash
   mysql -u realestate_user -p realestate < realestate.sql
   ```

## Running the Project
1. Apply migrations and create a superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
2. Collect static assets (only required for production or when serving via Whitenoise):
   ```bash
   python manage.py collectstatic
   ```
3. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

## Celery Workers & Scheduled Tasks
Celery is configured in `celery.py` to run nightly invoice generation (`invoices.tasks.generate_invoices`). Ensure Redis is running, then start the worker and beat scheduler in separate shells:

```bash
celery -A AdminRealEstate worker -l info
celery -A AdminRealEstate beat -l info
```

## Static & Media Assets
- `static/` contains the project's source assets and should remain under version control.
- `staticfiles/` is the collectstatic output and can be regenerated; it is safe to ignore in VCS.
- `media/` stores user uploads (avatars, documents, property images) and **must not** be committed.

## Testing
No automated tests are currently defined. You can start by creating tests within each app's `tests.py`. Run the test suite with:

```bash
python manage.py test
```

## Deployment Notes
- Switch `DEBUG` to `False` and set a unique `SECRET_KEY`.
- Update `ALLOWED_HOSTS` with your domain.
- Configure HTTPS (e.g., via a reverse proxy).
- Ensure `STATIC_ROOT` and `MEDIA_ROOT` directories are writable by the application server.
- Set up process supervision for the Django app, Celery worker, and Celery beat (e.g., systemd, Supervisor, or Docker).

## Project Structure (abridged)
```
account/         # Custom authentication & user management
core/            # Dashboard, analytics, and shared utilities
invoices/        # Invoice models, views, and Celery tasks
landlords/       # Landlord management
leases/          # Lease tracking
payments/        # Payment flows, including Mpesa integration
property/        # Property and unit inventory
tenants/         # Tenant profiles and lease links
utilities/       # Utility billing management
templates/       # Django templates grouped by app
static/          # Source static assets (CSS, JS, images)
```

## Troubleshooting
- **MySQL connection errors**: confirm credentials in `.env`, ensure MySQL is running, and verify the driver (`mysqlclient` or `mysql-connector-python`) is installed.
- **Celery connection refused**: verify Redis is installed and accessible at the configured host/port.
- **Static asset issues**: re-run `python manage.py collectstatic` and make sure `STATIC_URL`, `STATIC_ROOT`, and `STATICFILES_DIRS` are set correctly.
- **Email failures**: confirm SMTP credentials (`EMAIL_ADDRESS`, `EMAIL_PASSWORD`) and enable TLS on the account.


