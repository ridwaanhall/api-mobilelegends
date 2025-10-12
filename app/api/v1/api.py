"""
API v1 Router

This module aggregates all v1 API endpoints.
"""

from typing import Dict, Any
from fastapi import APIRouter, Request

from app.api.v1.endpoints import heroes, utils
from app.core.config import settings

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    heroes.router,
    tags=["Heroes"]
)
api_router.include_router(
    utils.router,
    tags=["Utilities"]
)


@api_router.get(
    "/",
    summary="API Information",
    description="Get API information and available endpoints",
    response_description="API metadata and endpoint list"
)
async def api_root(request: Request) -> Dict[str, Any]:
    """
    Get API information and available endpoints.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Dict[str, Any]: API information and endpoints
    """
    base_url = str(request.base_url).rstrip("/") + "/api/"
    
    status_info = (
        settings.api_status_messages["available"]
        if settings.IS_AVAILABLE
        else settings.api_status_messages["limited"]
    )
    
    # Build endpoints dict based on availability
    endpoints = {
        "documentation": base_url,
    }
    
    if settings.IS_AVAILABLE:
        endpoints.update({
            "hero_list": f"{base_url}hero-list/",
            "hero_rank": f"{base_url}hero-rank/",
            "hero_position": f"{base_url}hero-position/",
            "hero_detail": f"{base_url}hero-detail/{{hero_id}}/",
            "hero_detail_stats": f"{base_url}hero-detail-stats/{{main_heroid}}/",
            "hero_skill_combo": f"{base_url}hero-skill-combo/{{hero_id}}/",
            "hero_rate": f"{base_url}hero-rate/{{main_heroid}}/",
            "hero_relation": f"{base_url}hero-relation/{{hero_id}}/",
            "hero_counter": f"{base_url}hero-counter/{{main_heroid}}/",
            "hero_compatibility": f"{base_url}hero-compatibility/{{main_heroid}}/",
            "win_rate": f"{base_url}win-rate/?match-now=100&wr-now=50&wr-future=75",
        })
    
    new_api_endpoints = {}
    if settings.IS_AVAILABLE:
        new_api_endpoints = {
            "win_rate": (
                f"{base_url}win-rate/?match-now=100&wr-now=50&wr-future=75"
            ),
        }
    
    return {
        "code": 200,
        "status": "success",
        "message": "Request processed successfully",
        "meta": {
            "version": settings.API_VERSION,
            "author": "ridwaanhall",
            "support": {
                "status": status_info["status"],
                "message": status_info["message"],
                "support_message": settings.SUPPORT_MESSAGE,
                "donation_link": settings.DONATION_LINK
            },
            "available_endpoints": status_info["available_endpoints"]
        },
        "services": {
            "mlbb_api": {
                "status": status_info["status"],
                "message": (
                    "MLBB API is currently under maintenance."
                    if not settings.IS_AVAILABLE
                    else "MLBB API is online."
                ),
                "endpoints": endpoints
            },
            "mlbb_new_api": {
                "status": status_info["status"],
                "message": (
                    "MLBB new API is currently under maintenance."
                    if not settings.IS_AVAILABLE
                    else "MLBB new API is online."
                ),
                "endpoints": new_api_endpoints
            },
        },
        "links": {
            "api_url": (
                "https://mlbb-stats.ridwaanhall.com/api/"
                if settings.IS_AVAILABLE
                else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains"
                     "-mlbb-stats-and-api-pddikti/"
            ),
            "web_url": (
                "https://mlbb-stats.ridwaanhall.com/hero-rank/"
                if settings.IS_AVAILABLE
                else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains"
                     "-mlbb-stats-and-api-pddikti/"
            ),
            "docs": (
                "https://mlbb-stats-docs.ridwaanhall.com/"
                if settings.IS_AVAILABLE
                else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains"
                     "-mlbb-stats-and-api-pddikti/"
            ),
            "FastAPI Docs": (
                "https://mlbb-stats.ridwaanhall.com/docs"
                if settings.IS_AVAILABLE
                else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains"
                     "-mlbb-stats-and-api-pddikti/"
            ),
            "ReDoc": (
                "https://mlbb-stats.ridwaanhall.com/redoc"
                if settings.IS_AVAILABLE
                else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains"
                     "-mlbb-stats-and-api-pddikti/"
            ),
            "github": (
                "https://github.com/ridwaanhall/api-mobilelegends"
                if settings.IS_AVAILABLE
                else "https://ridwaanhall.com/blog/how-usage-monitoring-sustains"
                     "-mlbb-stats-and-api-pddikti/"
            ),
        }
    }


@api_router.get(
    "/docs/",
    include_in_schema=False
)
async def api_docs(request: Request) -> Dict[str, Any]:
    """Alias for root endpoint (backwards compatibility)."""
    return await api_root(request)
