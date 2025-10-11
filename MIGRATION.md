# FastAPI Migration Guide

## Overview

This project has been migrated from Django REST Framework to FastAPI. This document explains the migration and how to use the new FastAPI-based API.

## What Changed

### Framework Migration
- **From**: Django REST Framework (DRF)
- **To**: FastAPI

### Key Benefits
1. **Automatic Documentation**: Interactive API docs at `/docs` (Swagger UI) and `/redoc` (ReDoc)
2. **Type Safety**: Built-in request/response validation using Python type hints
3. **Better Performance**: Async support and faster response times
4. **Modern Python**: Uses Python 3.12+ features and async/await
5. **Simpler Deployment**: No need for Django settings or WSGI configuration

### File Structure Changes

#### New Files
- `main.py` - FastAPI application entry point
- `config.py` - Configuration module (replaces Django settings)
- `utils.py` - Utility functions (crypto, headers, etc.)
- `routers/mlbb.py` - MLBB API endpoints
- `routers/mplid.py` - MPL ID API endpoints (optional, requires Django for scrapers)

#### Deprecated Files (No longer used by FastAPI)
- `MLBB/settings.py` - Django settings
- `MLBB/urls.py` - Django URL configuration
- `MLBB/wsgi.py` - Django WSGI application
- `apps/mlbb_api/views.py` - Django REST Framework views
- `apps/mlbb_api/urls.py` - Django URL patterns

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

## API Compatibility

### Endpoints Remain the Same
All existing API endpoints maintain the same URL structure and functionality:

- `/api/` - API documentation and endpoint listing
- `/api/hero-list/` - Get hero list
- `/api/hero-list-new/` - Get new hero list from MLBB API
- `/api/hero-rank/` - Get hero rankings with filters
- `/api/hero-position/` - Get heroes by role and lane
- `/api/hero-detail/{hero_id}` - Get detailed hero information
- `/api/hero-detail-stats/{main_heroid}` - Get hero statistics
- `/api/hero-skill-combo/{hero_id}` - Get hero skill combos
- `/api/hero-rate/{main_heroid}` - Get hero rate over time
- `/api/hero-relation/{hero_id}` - Get hero relations
- `/api/hero-counter/{main_heroid}` - Get hero counters
- `/api/hero-compatibility/{main_heroid}` - Get hero compatibility
- `/api/win-rate/` - Calculate required matches for target win rate
- `/api/mplid/*` - MPL ID endpoints (standings, teams, stats, etc.)

### Response Format
Response formats remain identical to maintain backward compatibility with existing clients.

### Query Parameters
All query parameters work the same way:
- `lang` - Language selection (en, ru)
- `days`, `rank`, `size`, `index` - Pagination and filtering
- `role`, `lane` - Hero filtering by position
- `match-now`, `wr-now`, `wr-future` - Win rate calculation

## Development Notes

### MPL ID Endpoints
The MPL ID endpoints (`/api/mplid/*`) use the existing Django-based scrapers and serializers. They require:
- Django and djangorestframework installed
- Django settings configured
- The `apps/mpl_api` module with scrapers and serializers

If Django is not properly configured, the MPL ID endpoints will not be available, but the main MLBB API will continue to work.

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

## Documentation

FastAPI automatically generates interactive documentation:

1. **Swagger UI** at `/docs` - Interactive API testing interface
2. **ReDoc** at `/redoc` - Clean, readable API documentation
3. **OpenAPI Schema** at `/openapi.json` - Machine-readable API specification

## Migration Benefits

### For Developers
- Type-safe code with automatic validation
- Better IDE support and autocomplete
- Async support for better performance
- Simpler code structure

### For API Users
- Interactive documentation for easy testing
- Automatic API schema generation
- Better error messages with validation details
- Same endpoints and response formats (backward compatible)

### For Operations
- Faster response times
- Lower memory usage
- Simpler deployment configuration
- Better monitoring and logging

## Support

If you encounter any issues with the FastAPI migration, please:
1. Check the documentation at `/docs`
2. Review the environment variables in `.env`
3. Check the logs for error messages
4. Open an issue on GitHub with details

## Attribution

This FastAPI migration maintains all original attributions:
- **Moonton** - Developer of Mobile Legends: Bang Bang
- **ridwaanhall** - Creator of MLBB Stats API

All API data and assets remain the property of Moonton.

## MPL ID API Configuration

### Important Note

The MPL ID API endpoints (`/api/mplid/*`) require the **correct production SECRET_KEY** to work properly. 

**Why?** The MPL ID scraper classes use encrypted tokens to access external MPL ID data sources. These tokens can only be decrypted with the correct SECRET_KEY that was used to encrypt them.

### Behavior in Different Environments

1. **Production (with correct SECRET_KEY)**:
   - All MPL ID endpoints work normally
   - Returns actual MPL ID data (standings, teams, stats, etc.)

2. **Development/Test (with wrong/test SECRET_KEY)**:
   - MPL ID endpoints are visible in `/docs` and `/redoc`
   - Calling any MPL ID endpoint returns HTTP 503 with a helpful message:
     ```json
     {
       "detail": {
         "error": "Service Unavailable",
         "message": "MPL ID API requires proper SECRET_KEY configuration...",
         "service": "MPL ID API",
         "help": "Please ensure the correct SECRET_KEY environment variable is set."
       }
     }
     ```

### Troubleshooting MPL ID Endpoints

**Problem**: Getting 404 error for `/api/mplid/teams/` or other MPL ID endpoints

**Solutions**:

1. **Check if `IS_AVAILABLE=True` in your environment variables**
   - MPL ID router only loads when `IS_AVAILABLE=True`
   
2. **Verify Django and dependencies are installed**:
   ```bash
   pip install django djangorestframework beautifulsoup4 whitenoise
   ```

3. **Check server logs** for router loading status:
   - Look for: `INFO:main:MPL ID router loaded successfully`
   - If you see errors, the router failed to load

4. **Restart the application** after changing environment variables

5. **For production use**: Ensure the correct SECRET_KEY is set in Vercel/deployment environment

### Testing MPL ID Endpoints Locally

To test MPL ID functionality locally, you need the production SECRET_KEY. Contact the repository owner for the key if you need to test these endpoints.

Alternatively, the endpoints will show in the API documentation but return 503 errors, which is expected behavior in development.
