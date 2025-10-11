# Project File Structure Guide

## FastAPI Application (Active)

These files are used by the new FastAPI application:

### Core Application
- `main.py` - FastAPI application entry point
- `config.py` - Configuration and environment variables
- `utils.py` - Utility functions (crypto, headers)
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel deployment configuration

### Routers
- `routers/__init__.py` - Routers package
- `routers/mlbb.py` - MLBB API endpoints (hero data, stats, etc.)
- `routers/mplid.py` - MPL ID API endpoints (standings, teams, etc.)

### Dependencies for MPL ID
- `apps/mpl_api/scraper.py` - Web scraping logic for MPL data
- `apps/mpl_api/serializers.py` - DRF serializers for data validation
- `apps/mpl_api/utils.py` - Utility functions for MPL scraper

## Django Application (Legacy, Optional)

These files are from the original Django implementation:

### Django Core
- `MLBB/settings.py` - Django settings (not used by FastAPI)
- `MLBB/urls.py` - Django URL configuration (not used by FastAPI)
- `MLBB/wsgi.py` - Django WSGI application (not used by FastAPI)
- `manage.py` - Django management command (not used by FastAPI)

### Django Apps
- `apps/mlbb_api/` - Original Django REST Framework API
  - `views.py` - Django views (replaced by `routers/mlbb.py`)
  - `urls.py` - Django URLs (replaced by FastAPI routes)
  - `utils.py` - Django utilities (crypto functions still used)

- `apps/mlbb_web/` - Web interface (still uses Django)
  - `views.py` - Web views for hero rank page
  - `urls.py` - Web URLs
  - Can still be used if Django is configured

- `apps/mpl_api/` - MPL ID scraping and serialization
  - `scraper.py` - Used by FastAPI's mplid router
  - `serializers.py` - Used by FastAPI's mplid router
  - `utils.py` - Used by scrapers

### Templates (Django Web Interface)
- `templates/` - HTML templates for Django web interface
  - `base.html`, `navbar.html`, `footer.html`

### Static Files (Django)
- `staticfiles/` - Django static files (not used by FastAPI)

## Documentation

- `README.md` - Main project documentation
- `MIGRATION.md` - FastAPI migration guide
- `LICENSE` - BSD 3-Clause License
- `CODE_OF_CONDUCT.md` - Code of conduct
- `SECURITY.md` - Security policy
- `.env.example` - Environment variable template

## Configuration Files

- `.env` - Environment variables (create from .env.example)
- `.gitignore` - Git ignore patterns
- `vercel.json` - Vercel deployment configuration

## Running Different Parts

### FastAPI API Only (Recommended)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- Serves all MLBB API endpoints
- Serves MPL ID endpoints (if Django dependencies available)
- Automatic documentation at /docs

### Django Full Stack (Optional)
```bash
python manage.py runserver
```
- Serves Django web interface
- Serves original Django REST API
- Requires Django settings configured

## Migration Status

✅ **Migrated to FastAPI:**
- All MLBB API endpoints (`/api/hero-*`)
- Win rate calculator (`/api/win-rate/`)
- API documentation endpoint (`/api/`)
- Health check endpoint (`/health`)
- Automatic API docs (`/docs`, `/redoc`)

⚠️ **Partially Migrated:**
- MPL ID endpoints (`/api/mplid/*`) - Use FastAPI routing but rely on Django scrapers/serializers

❌ **Not Migrated (Optional):**
- Web interface (`/hero-rank/`) - Still requires Django
- Django admin interface

## Deployment

### Vercel (FastAPI)
The `vercel.json` is configured for FastAPI deployment:
- Entry point: `main.py`
- All routes handled by FastAPI
- No static file serving needed

### Traditional Hosting (Django)
If you want to use the Django web interface:
- Configure Django settings
- Set up WSGI server (Gunicorn, uWSGI)
- Configure static file serving

## Dependencies

### FastAPI Required
- fastapi
- uvicorn
- python-decouple
- requests
- cryptography

### MPL ID Scraper Required
- beautifulsoup4
- Django
- djangorestframework

### Development
- python 3.12+
