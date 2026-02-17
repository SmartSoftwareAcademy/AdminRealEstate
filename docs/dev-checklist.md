# Developer Checklist (Before Opening a PR)

Use this checklist to ensure changes are ready for review and integration.

1. Environment
   - [ ] Activate virtual environment: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/macOS).
   - [ ] Install/update dependencies: `pip install -r requirements.txt`.

2. Local tests & lint
   - [ ] Run unit tests: `python manage.py test`.
   - [ ] Run formatting/linting tools (black, isort, flake8) if configured.

3. Migrations
   - [ ] Make model migrations if required: `python manage.py makemigrations`.
   - [ ] Apply migrations locally and ensure no errors: `python manage.py migrate`.

4. Static files
   - [ ] Rebuild/collect static files if the change affects CSS/JS: `python manage.py collectstatic --no-input`.

5. Manual checks
   - [ ] Start the dev server: `python manage.py runserver`.
   - [ ] Smoke test main flows: login, dashboard, quick actions, create a property/lease/invoice, payment flow (if applicable).
   - [ ] Verify that dropdowns, modals and JS widgets work as expected.

6. Commit & PR
   - [ ] Write a clear commit message summarizing the change.
   - [ ] Add a short description to the PR with steps to reproduce the change and any environment notes.

Optional: Add or update docs or tests for any new behavior.
