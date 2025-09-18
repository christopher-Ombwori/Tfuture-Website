# TFuture Website (Django + Wagtail)

This repository contains the TFuture website built with Django 5 and Wagtail 7. It separates business operations (Django Admin) from content management (Wagtail CMS), and integrates Brevo for transactional email.

## Architecture Overview

- Apps
  - `core`: Business logic, services, service requests, email integration, sitemaps, context processors, and Django Admin.
  - `cms`: Wagtail content models for Projects (portfolio), Blog, and Products; plus templated stream blocks and editor hooks.
- Routing
  - `TFuture/urls.py` wires core views first, then Wagtail admin/docs and Django sitemaps, and finally Wagtail page routing.
- Templates
  - Global layout in `templates/base.html` using Tailwind CDN. Includes a service request modal posting to `core.submit_service_request`.
  - Email templates under `templates/core/emails/` for both customer confirmation and admin notification.
- Emails (Brevo)
  - `core/brevo_api.py` wraps Brevo v3 SMTP endpoint. Two functions send customer and admin emails; both are called from `submit_service_request`.
- Sitemaps
  - `core/sitemaps.py` provides Django sitemaps for Services, Static views, and Wagtail pages.

See `project_architecture.md` for a more detailed diagram and rationale.

## Requirements

- Python 3.12+
- PostgreSQL (default), or override via `DB_ENGINE`.
- Windows or Unix. Commands below are for Windows PowerShell.

## Quick start (Windows/PowerShell)

1. Create and activate a virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root

```dotenv
# Django
SECRET_KEY=replace-with-a-secure-secret
DEBUG=true
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (PostgreSQL example)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=tfuture
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432

# Site & Email
SITE_URL=http://localhost:8000
DEFAULT_FROM_EMAIL=contact@tfuturedesigns.studio
DEFAULT_FROM_NAME=TFuture
ADMIN_EMAIL=contact@tfuturedesigns.studio
# Optional list: comma-separated
ADMIN_EMAILS=

# Brevo
BREVO_API_KEY=your-brevo-api-key

# Internationalization
LANGUAGE_CODE=en-us
TIME_ZONE=Africa/Nairobi
USE_I18N=true
USE_TZ=true

# Whitenoise (prod)
WHITENOISE_ALLOW_ALL_ORIGINS=true
```

4. Apply migrations and create a superuser

```powershell
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server

```powershell
python manage.py runserver
```

- Django Admin (business): `http://localhost:8000/my-admin-futuristic`
- Wagtail Admin (content): `http://localhost:8000/admin/`

## Initial content checklist

- In Wagtail Admin, create:
  - Root pages as needed: Project Index, Blog Index, Products Page.
  - Project and Blog pages under their respective indexes.
- In Django Admin, add at least one `Service` named "General Inquiry" with slug `general-inquiry` and mark it invisible; do not delete it. Other services can be added and set visible.

## Tests and utilities

- Email tests
  - `test_brevo_api.py`: Validates Brevo config and sends a test email to `ADMIN_EMAIL`.
  - `test_email_templates.py`: Renders templates to temporary files and opens them in your browser.
  - `test_email_template.py` and `test_admin_notification.py`: Lightweight manual tests for HTML rendering and SMTP.

Run examples:

```powershell
python test_brevo_api.py
python test_email_templates.py
```

## Notes

- Static assets are served by Whitenoise. In production, set `DEBUG=false` and configure security settings via `.env`.
- Tailwind CDN is used for simplicity; consider building locally if you need purge and custom plugins.
- `core/context_processors.py` supplies Wagtail pages to nav links and the `general_inquiry` service for the Contact buttons.

## Troubleshooting

- Missing `.env` keys: The app uses `python-decouple`. Ensure required keys are present; see `.env` sample above.
- Database connection: If you prefer SQLite for quick local runs, set `DB_ENGINE=django.db.backends.sqlite3` and `DB_NAME=db.sqlite3` and remove other DB settings.
- Emails not sending: Confirm `BREVO_API_KEY` is set and valid; check the output from `test_brevo_api.py`.
