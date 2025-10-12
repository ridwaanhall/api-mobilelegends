"""
FastAPI Main Application

This is the main entry point for the Mobile Legends API application.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.v1.api import api_router

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    
    Args:
        app: FastAPI application instance
        
    Yields:
        None
    """
    # Startup
    logger.info(f"Starting Mobile Legends API v{settings.API_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"API Available: {settings.IS_AVAILABLE}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Mobile Legends API")


# Initialize FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url=None,  # We'll create custom docs
    redoc_url=None,  # We'll create custom redoc
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "Heroes",
            "description": "Operations related to Mobile Legends heroes",
        },
        {
            "name": "Utilities",
            "description": "Utility endpoints like win rate calculator",
        },
        {
            "name": "Health",
            "description": "Health check and monitoring endpoints",
        },
    ]
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        settings.ALLOWED_ORIGINS
        if not settings.is_development
        else ["*"]
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(
    api_router,
    prefix="/api"
)


@app.get(
    "/",
    include_in_schema=False
)
async def root() -> RedirectResponse:
    """Redirect root to API documentation."""
    return RedirectResponse(url="/api/")


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Check API health status",
    response_description="Health status information"
)
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "api_available": settings.IS_AVAILABLE,
        "environment": settings.ENVIRONMENT
    }


@app.get(
    "/docs",
    include_in_schema=False
)
async def custom_swagger_ui_html():
    """Custom Swagger UI documentation."""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Swagger UI",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )


@app.get(
    "/redoc",
    include_in_schema=False
)
async def custom_redoc_html():
    """Custom ReDoc documentation."""
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - ReDoc",
        redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )


@app.get(
    "/openapi.json",
    include_in_schema=False
)
async def custom_openapi():
    """Custom OpenAPI schema."""
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
async def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Custom 404 handler.
    
    Args:
        request: FastAPI request object
        exc: Exception
        
    Returns:
        JSONResponse: 404 error response
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "path": request.url.path,
            "available_docs": "/docs or /redoc"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Custom 500 handler.
    
    Args:
        request: FastAPI request object
        exc: Exception
        
    Returns:
        JSONResponse: 500 error response
    """
    logger.error(f"Internal server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "support": settings.support_details
        }
    )


# For Vercel deployment
app = app
