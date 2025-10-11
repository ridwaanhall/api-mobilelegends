# FastAPI Migration Guide

## Overview

This project has been migrated from Django REST Framework to FastAPI. This document explains the migration and how to use the new FastAPI-based API.

## What Changed

### Framework Migration
- **From**: Django REST Framework (DRF)
- **To**: FastAPI (Pure, without Django dependencies)

### Key Benefits
1. **Automatic Documentation**: Interactive API docs at `/docs` (Swagger UI) and `/redoc` (ReDoc)
2. **Type Safety**: Built-in request/response validation using Python type hints
3. **Better Performance**: Async support and faster response times
4. **Modern Python**: Uses Python 3.12+ features and async/await
5. **Simpler Deployment**: No need for Django settings or WSGI configuration
6. **Minimal Dependencies**: Pure FastAPI without Django overhead

### File Structure Changes

#### New Files
- `main.py` - FastAPI application entry point
- `config.py` - Configuration module (replaces Django settings)
- `utils.py` - Utility functions (crypto, headers, etc.)
- `routers/mlbb.py` - MLBB API endpoints
- `routers/additional.py` - Additional API endpoints (win rate calculator)

#### Deprecated Files (No longer used by FastAPI)
- `MLBB/settings.py` - Django settings (preserved for reference)
- `MLBB/urls.py` - Django URL configuration (preserved for reference)
- `MLBB/wsgi.py` - Django WSGI application (preserved for reference)
- `apps/mlbb_api/views.py` - Django REST Framework views (preserved for reference)
- `apps/mlbb_api/urls.py` - Django URL patterns (preserved for reference)

### Removed Components
- **MPL ID API**: Removed due to Django dependency requirements and complexity
- **Django Framework**: No longer required for FastAPI implementation
- **djangorestframework**: No longer required

## Running the Application

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file based on `.env.example`:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   MLBB_URL=https://your-mlbb-url.com/
   PROD_URL=http://127.0.0.1:8000/api/
   IS_AVAILABLE=True
   API_VERSION=1.2.0
   ```

3. **Run the development server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**:
   - API Root: http://localhost:8000/api/
   - Swagger UI Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Production Deployment (Vercel)

The application is configured for deployment on Vercel:

1. **vercel.json** has been updated to use `main.py` instead of Django's WSGI
2. The app automatically uses production settings when `DEBUG=False`
3. Deploy using the Vercel CLI or GitHub integration

## API Documentation

### Available API Sections

The API provides **3 organized sections**:

1. **MLBB API** (13 endpoints) - Hero data, rankings, statistics, details
2. **Additional API** (1 endpoint) - Win rate calculator
3. **Health Check** (1 endpoint) - Service health status

### MLBB API Endpoints

- `/api/` - API documentation and endpoint listing
- `/api/docs/` - Docs endpoint
- `/api/hero-list/` - Hero list (supports EN/RU languages)
- `/api/hero-rank/` - Hero rankings with filters
- `/api/hero-position/` - Heroes by role and lane
- `/api/hero-detail/{hero_id}` - Detailed hero information
- `/api/hero-detail-stats/{main_heroid}` - Hero statistics
- `/api/hero-skill-combo/{hero_id}` - Hero skill combos
- `/api/hero-rate/{main_heroid}` - Hero rate over time
- `/api/hero-relation/{hero_id}` - Hero relations
- `/api/hero-counter/{main_heroid}` - Hero counters
- `/api/hero-compatibility/{main_heroid}` - Hero compatibility

### Additional API Endpoints

- `/api/win-rate/` - Calculate required matches for target win rate

### Health Check

- `/health` - Health check endpoint

### Response Format

All endpoints maintain the same response formats as the original Django API for backward compatibility.

### Query Parameters

All query parameters work the same way:
- `lang` - Language selection (en, ru)
- `days`, `rank`, `size`, `index` - Pagination and filtering
- `role`, `lane` - Hero filtering by position
- `match-now`, `wr-now`, `wr-future` - Win rate calculation

## Dependencies

### Core Dependencies
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **python-decouple** - Environment variable management
- **requests** - HTTP client for external API calls
- **cryptography** - Encryption utilities

### Removed Dependencies
- Django
- djangorestframework
- beautifulsoup4
- soupsieve
- whitenoise

## Development Notes

### Pure FastAPI Implementation

The application now uses pure FastAPI without any Django dependencies:

- No Django ORM
- No Django middleware
- No Django settings
- No database migrations needed
- Lighter and faster deployment

### Error Handling

FastAPI provides automatic error handling with proper HTTP status codes:
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable (when `IS_AVAILABLE=False`)

### CORS

CORS is configured in `main.py` with allowed origins from `config.py`. In DEBUG mode, all origins are allowed.

## Testing

Test the API endpoints:

```bash
# Test health check
curl http://localhost:8000/health

# Test API root
curl http://localhost:8000/api/

# Test hero list
curl http://localhost:8000/api/hero-list/

# Test win rate calculation
curl "http://localhost:8000/api/win-rate/?match-now=100&wr-now=50&wr-future=75"
```

## Migration Benefits

### For Developers
- Type-safe code with automatic validation
- Better IDE support and autocomplete
- Async support for better performance
- Simpler code structure
- No Django complexity

### For API Users
- Same endpoints and response formats (backward compatible)
- Interactive documentation for easy testing
- Better error messages with validation details
- Automatic API schema generation

### For Operations
- Faster response times
- Lower memory usage
- Simpler deployment configuration
- No database required
- Fewer dependencies to manage

## Support

For issues or questions:
- Check the documentation at `/docs`
- Review environment variables in `.env`
- Check logs for error messages
- Open an issue on GitHub

## Attribution

This FastAPI implementation maintains all original attributions:
- **Moonton** - Developer of Mobile Legends: Bang Bang
- **ridwaanhall** - Creator of MLBB Stats API

All API data and assets remain the property of Moonton.
