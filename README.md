# AdminRealEstate

AdminRealEstate is a Django-based property management platform that centralizes landlord, tenant, lease, payment, invoicing, and utility workflows. It integrates Celery for scheduled tasks (e.g., nightly invoice generation) and Redis as the task broker, while exposing a modular set of Django apps for day-to-day operations.

## Documentation Map
1. **[Setup Guide](docs/setup.md)** – Windows-first installation, environment configuration, and service orchestration.
2. **[Implementation Overview](docs/implementation.md)** – Breakdown of Django apps, integrations, and architectural responsibilities.
3. **[Database Architecture](docs/erd.md)** – Entity relationship narrative covering models, relationships, and connection details.
4. **[Project Plan](docs/plan.md)** – High-level flows, roadmap ideas, and diagram guidance.

## Key Features
- Authenticated multi-role access built on `account.CustomUser` (Owners, Agents, Staff, Tenants).
- Dashboards and shared services delivered through the `core` app, including centralised SMTP & M-Pesa configuration.
- Property lifecycle management (owner → property → unit → lease) with linked invoicing and payments.
- Cash and M-Pesa payment capture, including STK push integration and automated callbacks.
- Background jobs handled via Celery + Redis (e.g., automated invoice generation).
- TinyMCE for rich text editing and Jazzmin for an enhanced admin UI.

## Technology Stack
- **Backend**: Django 3.2
- **Database**: MySQL / MariaDB via `mysql-connector-python`
- **Task Queue**: Celery with Redis broker & result backend
- **Frontend**: Django templates + static assets (no SPA build toolchain required)
- **Document/PDF utilities**: `xhtml2pdf`, `pyHanko`, `reportlab`
- **Messaging**: SMTP email, M-Pesa STK push

## Getting Started (TL;DR)
> For full instructions, see the [Setup Guide](docs/setup.md).

1. **Clone & enter**
   ```bash
   git clone <repo-url>
   cd AdminRealEstate
   ```
2. **Create venv & install deps**
   ```bash
   python -m venv .venv
   ./.venv/Scripts/activate  # Windows PowerShell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Configure environment** – Copy `.env` template and update Django secret key, MySQL credentials, SMTP, and Redis URLs.
4. **Provision database** – Create the `realestate` schema and optional sample data (`realestate.sql`).
5. **Apply migrations & bootstrap**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. **Run services**
   ```bash
   python manage.py runserver
   celery -A AdminRealEstate worker -l INFO
   celery -A AdminRealEstate beat -l INFO
   ```

## Configuration Notes
- Defaults for MySQL, SMTP, and M-Pesa live in `AdminRealEstate/settings.py` and `core.Setup`; override via environment variables for production.
- Whitenoise (`CompressedManifestStaticFilesStorage`) powers static file serving; run `python manage.py collectstatic` for deploys.
- Use the Django admin (`core.Setup`) to store SMTP credentials and M-Pesa keys securely once deployed.

## Architecture Snapshot
- **User hub**: `account.CustomUser` with one-to-one role profiles (owners, agents, staff, tenants).
- **Property ops**: `property` app manages inventory; `leases` link tenants to units; `invoices` and `payments` close the billing loop.
- **Notifications**: `core.utils.MailSender` handles email, while `notices` manages in-system announcements.
- **Automation**: `invoices.tasks.generate_invoices` scheduled nightly via Celery Beat.
- **Integrations**: Safaricom Daraja API for mobile payments; Redis for async task queueing.

## Project Structure (abridged)
```
account/         # Custom authentication & user management
core/            # Dashboard, context processors, shared utilities, SMTP & M-Pesa config
invoices/        # Invoice models, Celery tasks, list/detail views
landlords/       # Owner & agent profiles tied to CustomUser
leases/          # Lease lifecycle and contractual terms
payments/        # Cash & M-Pesa payment workflows
property/        # Properties, units, and media assets
tenants/         # Tenant metadata (kin, employment, business)
notices/         # System notices and replies
payroll/         # Staff earnings, deductions, and salary payments
templates/       # Django templates grouped by app
static/          # Source static assets (CSS, JS, images)
docs/            # Project documentation (setup, implementation, ERD, plan)
```

## Testing & Quality
- No automated tests ship by default; start with per-app `tests.py` and run:
  ```bash
  python manage.py test
  ```
- Consider adding pytest or Django test factories as the project grows.

## Deployment Checklist
- Set `DEBUG=False` and provide a strong `SECRET_KEY`.
- Update `ALLOWED_HOSTS`, configure HTTPS, and provision production SMTP + M-Pesa credentials.
- Ensure MySQL backups, Redis monitoring, and Celery process supervision (systemd, Supervisor, containers).
- Configure `STATIC_ROOT`/`MEDIA_ROOT` with appropriate permissions.

## Troubleshooting
- **MySQL connection errors** – confirm credentials in `.env`, ensure the driver (`mysqlclient` or `mysql-connector-python`) is installed, and MySQL is running.
- **Redis/Celery issues** – verify Redis service availability and matching URLs between Django settings and `.env`.
- **Static asset problems** – run `collectstatic` and verify Whitenoise configuration.
- **Email failures** – confirm SMTP settings in the admin (`core.Setup`) and ensure TLS/ports align with provider requirements.

Refer to the [Project Plan](docs/plan.md) for roadmap suggestions and diagram guidance.
