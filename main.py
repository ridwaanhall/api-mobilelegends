"""FastAPI Main Application for Mobile Legends API"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
import logging
import config
from routers import mlbb, additional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mobile Legends API",
    description="Mobile Legends Bang Bang API for hero data, statistics, and MPL ID information",
    version=config.API_VERSION,
    docs_url=None,  # We'll create custom docs
    redoc_url=None,  # We'll create custom redoc
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS if not config.DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper tags for documentation sections
app.include_router(mlbb.router, prefix="/api", tags=["MLBB API"])
app.include_router(additional.router, prefix="/api", tags=["Additional API"])

# Include MPL ID router (endpoints will work when Django is properly configured)
if config.IS_AVAILABLE:
    try:
        # Set up Django before importing the router
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MLBB.settings')
        import django
        django.setup()
        
        # Now import and include the router
        from routers import mplid
        app.include_router(mplid.router, prefix="/api")
        logger.info("MPL ID router loaded successfully")
    except Exception as e:
        logger.warning(f"MPL ID router could not be loaded: {e}")
        # Still log the error for debugging but don't fail the app
        import traceback
        logger.debug(traceback.format_exc())


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation"""
    return RedirectResponse(url="/api/")


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": config.API_VERSION,
        "api_available": config.IS_AVAILABLE
    }


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI documentation"""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Swagger UI",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )


@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    """Custom ReDoc documentation"""
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - ReDoc",
        redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )


@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    """Custom OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom information
    openapi_schema["info"]["x-logo"] = {
        "url": "https://avatars.githubusercontent.com/u/95293968"
    }
    openapi_schema["info"]["contact"] = {
        "name": "ridwaanhall",
        "url": "https://github.com/ridwaanhall",
    }
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "path": request.url.path,
            "available_docs": "/docs or /redoc"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "support": config.SUPPORT_DETAILS
        }
    )


# For Vercel deployment
app = app
