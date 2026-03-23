from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from urllib.parse import urljoin

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, RedirectResponse, Response

from app.core.config import (
    API_BASE_URL,
    API_STATUS_MESSAGES,
    API_VERSION,
    DONATION_CURRENCY,
    DONATION_MIN,
    DONATION_NOW,
    DONATION_TARGET,
    DOCS_BASE_URL,
    IS_AVAILABLE,
    MAINTENANCE_INFO_URL,
    SUPPORT_DETAILS,
    SUPPORT_STATUS_MESSAGES,
    BASE_URL,
)


from fastapi.routing import APIRoute
from fastapi import Request
from app.services.mlbb import fetch_mlbb_post

router = APIRouter(tags=["root"])



# Utility to get all available endpoints from the FastAPI app
def get_available_endpoints(app, include_methods: set[str] | None = None) -> list[dict]:
    endpoints: list[dict] = []
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        if include_methods and not (set(route.methods) & include_methods):
            continue
        # Exclude docs, openapi, redoc, static
        if route.path in {"/openapi.json", "/docs", "/redoc", "/static"}:
            continue
        endpoints.append({
            "path": route.path,
            "methods": list(route.methods),
            "name": route.name,
            "summary": getattr(route, "summary", None),
            "include_in_schema": getattr(route, "include_in_schema", True),
        })
    return endpoints

# Only public endpoints for maintenance mode
def is_public_endpoint(path: str) -> bool:
    # Only allow endpoints that do not require user authentication or sensitive data
    # Exclude /api/user, /api/addon/check-ip, etc.
    if path.startswith("/api/user"):
        return False
    if path.startswith("/api/addon/check-ip"):
        return False
    # Allow all others
    return True

# Get all hero IDs
def get_all_hero_ids() -> list[int]:
    payload: dict = {
        "pageSize": 200,
        "sorts": [{"data": {"field": "hero_id", "order": "asc"}, "type": "sequence"}],
        "pageIndex": 1,
        "fields": ["hero_id"],
    }
    data = fetch_mlbb_post("2756564", payload, "en")
    ids: list[int] = []
    for record in data.get("data", {}).get("records", []):
        hero_id = record.get("data", {}).get("hero_id")
        if isinstance(hero_id, int):
            ids.append(hero_id)
    return ids


@router.get(
    path="/",
    include_in_schema=False,
)
@router.get(
    path="/api/docs",
    include_in_schema=False,
)
def api_docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)



@router.get(
    path="/api",
    summary="API Index and Status",
    description=(
        "Provides API metadata, current status, and available endpoints. "
        "The response includes general information such as version, author, base URL, "
        "support and donation details, and a list of available endpoints. "
        "It also returns operational status messages and links to API documentation and base URLs."
    ),
)
async def api_index(request: Request) -> dict:
    from fastapi import FastAPI
    app: FastAPI = request.app
    status_key = "available" if IS_AVAILABLE else "limited"
    status_info = API_STATUS_MESSAGES[status_key]
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    base_api_url = API_BASE_URL.rstrip("/")
    docs_url = DOCS_BASE_URL.rstrip("/")


    always_available: set[str] = {"/", "/api", "/api/docs", "/robots.txt"}
    endpoints = get_available_endpoints(app, include_methods={"GET", "POST"})
    if IS_AVAILABLE:
        available_endpoints: list[str] = [ep["path"] for ep in endpoints if ep["include_in_schema"] and is_public_endpoint(ep["path"])]
    else:
        available_endpoints: list[str] = [ep["path"] for ep in endpoints if ep["path"] in always_available]

    return {
        "code": 200,
        "status": "success",
        "message": "Request processed successfully",
        "timestamp": timestamp,
        "meta": {
            "version": API_VERSION,
            "author": "ridwaanhall",
            "base_url": base_api_url,
            "support": {
                "status": status_info["status"],
                "donation_min": DONATION_MIN,
                "donation_now": DONATION_NOW,
                "donation_target": DONATION_TARGET,
                "donation_currency": DONATION_CURRENCY,
                "donation_links": {
                    "github_sponsors": SUPPORT_DETAILS["github_sponsors"],
                    "buymeacoffee": SUPPORT_DETAILS["buymeacoffee"],
                },
                "message": SUPPORT_STATUS_MESSAGES[status_key],
            },
        },
        "endpoints": available_endpoints,
        "links": {
            "api_url": base_api_url if IS_AVAILABLE else MAINTENANCE_INFO_URL,
            "docs": docs_url,
        },
    }


@router.get(
    path="/robots.txt",
    summary="Robots.txt for Web Crawlers",
    description=(
        "Provides instructions for web crawlers and bots accessing the API. "
        "The response defines rules for user-agents, allowed/disallowed paths, "
        "and includes references to the host information. "
        "This helps search engines and automated crawlers understand how to index "
        "and interact with the API resources."
    ),
)
def robots_txt() -> PlainTextResponse:
    host_url = BASE_URL.rstrip("/")
    content = "\n".join(["User-agent: *", "Allow: /", "Disallow:", f"Host: {host_url}"])
    return PlainTextResponse(content=content)
