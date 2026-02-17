# Project Overview — AdminRealEstate

This document provides a short, clear explanation of what AdminRealEstate is and what components it contains. It is intended for beginners who want to understand the architecture, the responsibilities of each app, and the typical flows in the project.

## What is AdminRealEstate?
AdminRealEstate is a Django-based property management and administration system built to manage owners, agents, properties, tenants, leases, invoices/payments, notices, and staff payroll. It provides role-based portals for Owners, Agents, Property Managers, Tenants and Staff. It also integrates with M-Pesa (mobile money) for payments and uses Celery for background tasks.

## Key Features
- Multi-role user accounts: Owner, Agent, Staff, Tenant, Admin.
- Property management: Create and manage properties and property units/units allocation.
- Leasing & Invoicing: Create leases, generate invoices, record payments, and manage outstanding balances.
- Payments: Support for offline and Mpesa-based workflows (see `payments/` and `mpesa_credentials.py`).
- Notices & Requests: Notice board for maintenance and facility requests for tenants and staff.
- Payroll: Payroll app to manage staff salary, payslips and salary payments.
- Analytics & Dashboard: Role-specific dashboard with quick actions and charts.
- Asynchronous tasks: Celery + Redis for background tasks (invoices, notifications, scheduled jobs).

## Code Structure (top-level apps)
- `account/` — Authentication views, login and user lifecycle helpers.
- `core/` — Central settings, site configuration, common utils, middleware and context processors.
- `property/` — Property and units models, forms and views.
- `tenants/`, `owners/`, `leases/`, `invoices/`, `payments/`, `notices/` — Domain apps handling related flows.
- `staff/`, `payroll/` — Staff and payroll management.

## Important Files
- `manage.py` — Django CLI entrypoint.
- `AdminRealEstate/settings.py` — Django settings (including references to `.env` / environment variables).
- `requirements.txt` — Python dependencies.
- `realestate.sql` — Example/dump schema and content useful for local starting data.
- `templates/` and `static/` — Frontend templates, CSS and JS assets.

## Runtime & External Services
- Database: MySQL/MariaDB (project was tested with MySQL in sample SQL). You can use PostgreSQL too with configuration changes.
- Cache/Broker: Redis (used for Celery broker and result backend).
- Celery: For background jobs (worker + beat recommended).
- Email: SMTP provider for notifications (configured via site setup in Django admin).
- Optional: Ngrok for local webhook testing (M-Pesa callbacks).

## Typical User Flows
- Owner logs in → views dashboard → adds property → generates lease → generates invoice → tenant pays using M-Pesa → payment recorded in system.
- Staff logs in → views maintenance notices → marks as resolved → uses payroll features to generate payslips.

---

If you are new here, see `docs/quickstart.md` for a hands-on setup guide (both "start-from-scratch" and "activate existing env" scenarios).
