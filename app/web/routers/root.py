from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.config import ALTERNATIVE_ENDPOINT_URL, API_STATUS_MESSAGES, IS_AVAILABLE, PROJECT_VERSION
from app.web.openapi_catalog import GROUP_META, WEB_GROUPS, get_group_operations
from app.web.openmlbb_catalog import OPENMLBB_GROUP_META, OPENMLBB_GROUPS, get_openmlbb_group_operations

router = APIRouter(tags=["web"])

_TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))


def _shared_context(request: Request, current_group: str | None = None) -> dict[str, object]:
    return {
        "request": request,
        "group_meta": GROUP_META,
        "groups": WEB_GROUPS,
        "current_group": current_group,
        "current_year": datetime.now(UTC).year,
        "api_version": PROJECT_VERSION,
        "is_available": IS_AVAILABLE,
        "alternative_endpoint": ALTERNATIVE_ENDPOINT_URL,
        "maintenance_message": API_STATUS_MESSAGES["limited"]["message"],
        "seo_description": "Interactive web interface for MLBB Public Data API with endpoint forms, readable response tables, and cURL output.",
        "seo_keywords": "mlbb api, mobile legends api, web ui, fastapi, openapi, response table",
    }


def _normalize_path(value: str) -> str:
    normalized = value.rstrip("/")
    return normalized or "/"


@router.get(path="/", include_in_schema=False, response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
    context = _shared_context(request)
    if IS_AVAILABLE:
        context.update(
            {
                "title": "Home / MLBB Public Data API & Web",
                "web_title": "Home",
                "seo_description": "Modern landing page for MLBB Public Data API. Access docs and a full interactive web playground for all endpoints.",
                "seo_keywords": "mlbb, mobile legends, api docs, web playground, analytics api",
            }
        )
        return templates.TemplateResponse(request, "root/landing_page.html", context)

    context.update(
        {
            "title": "503 Service Unavailable / MLBB Public Data API",
            "web_title": "Service Unavailable",
            "seo_description": "MLBB Public Data API is temporarily unavailable due to high traffic.",
            "seo_keywords": "mlbb api status, service unavailable, high traffic",
        }
    )
    return templates.TemplateResponse(request, "root/landing_page.html", context, status_code=503)


@router.get(path="/web", include_in_schema=False)
def web_home() -> RedirectResponse:
    return RedirectResponse(url="/web/user", status_code=307)


@router.get(path="/web/{group}", include_in_schema=False, response_class=HTMLResponse)
def web_group_page(request: Request, group: str) -> HTMLResponse:
    if group not in WEB_GROUPS:
        raise HTTPException(status_code=404, detail="Web group not found")

    operations = get_group_operations(request.app, group)
    context = _shared_context(request, current_group=group)
    context.update(
        {
            "title": f"{GROUP_META[group]['title']} Endpoints / MLBB Public Data API & Web",
            "web_title": f"{GROUP_META[group]['title']} Endpoints",
            "subtitle": GROUP_META[group]["description"],
            "seo_description": f"Browse and execute {GROUP_META[group]['title']} endpoints from the MLBB Public Data API & Web interface.",
            "seo_keywords": f"mlbb api, {group} endpoints, openapi web ui",
            "operations": operations,
            "sidebar_operations": operations,
            "selected_web_path": None,
        }
    )
    return templates.TemplateResponse(request, "web/group_page.html", context)


@router.get(path="/web/{group}/{endpoint_path:path}", include_in_schema=False, response_class=HTMLResponse)
def web_endpoint_page(request: Request, group: str, endpoint_path: str) -> HTMLResponse:
    if group not in WEB_GROUPS:
        raise HTTPException(status_code=404, detail="Web group not found")

    all_operations = get_group_operations(request.app, group)
    normalized_path = _normalize_path(f"/web/{group}/{endpoint_path}")
    matched_operations = [
        operation
        for operation in all_operations
        if _normalize_path(str(operation["web_path"])) == normalized_path
    ]

    if not matched_operations:
        raise HTTPException(status_code=404, detail="Web endpoint not found")

    context = _shared_context(request, current_group=group)
    operation_summary = str(matched_operations[0].get("summary") or "Endpoint").strip()
    group_title = str(GROUP_META[group]["title"]).strip()
    context.update(
        {
            "title": f"{operation_summary} - {group_title[:-1] if group_title.endswith('s') else group_title} Endpoint / MLBB Public Data API & Web",
            "web_title": f"{group_title[:-1] if group_title.endswith('s') else group_title} Endpoint",
            "subtitle": "Interactive request form for this API endpoint.",
            "seo_description": f"Execute and inspect a {GROUP_META[group]['title']} endpoint from the MLBB API web interface.",
            "seo_keywords": f"mlbb api endpoint, {group}, curl, readable response",
            "operations": matched_operations,
            "sidebar_operations": all_operations,
            "selected_web_path": normalized_path,
        }
    )
    return templates.TemplateResponse(request, "web/group_page.html", context)


@router.get(path="/openmlbb", include_in_schema=False, response_class=HTMLResponse)
def openmlbb_home(request: Request) -> HTMLResponse:
    context = _shared_context(request)
    context.update(
        {
            "title": "OpenMLBB SDK / Home",
            "web_title": "OpenMLBB SDK",
            "subtitle": "Pick a client group to browse Python SDK docs and practical examples, plus a TypeScript alternative.",
            "seo_description": "OpenMLBB Python SDK hub for academy, mlbb, user, and addon docs, with TypeScript alternative guidance.",
            "seo_keywords": "openmlbb, python sdk, typescript sdk, mlbb api, academy, user, addon",
        }
    )
    return templates.TemplateResponse(request, "openmlbb/landing_page.html", context)


@router.get(path="/openmlbb/{group}", include_in_schema=False, response_class=HTMLResponse)
def openmlbb_group_page(request: Request, group: str) -> HTMLResponse:
    if group not in OPENMLBB_GROUPS:
        raise HTTPException(status_code=404, detail="OpenMLBB group not found")

    operations = get_openmlbb_group_operations(request.app, group)
    context = _shared_context(request, current_group=group)
    context.update(
        {
            "title": f"OpenMLBB {OPENMLBB_GROUP_META[group]['title']} Client / SDK Docs",
            "web_title": f"OpenMLBB {OPENMLBB_GROUP_META[group]['title']} Client",
            "subtitle": f"Structured SDK docs for {OPENMLBB_GROUP_META[group]['title']} endpoints using from OpenMLBB import OpenMLBB.",
            "seo_description": f"OpenMLBB Python SDK documentation for {group} endpoints.",
            "seo_keywords": f"openmlbb, python sdk, {group}, mlbb api",
            "operations": operations,
            "sidebar_operations": operations,
            "selected_openmlbb_path": None,
        }
    )
    return templates.TemplateResponse(request, "openmlbb/group_page.html", context)


@router.get(path="/openmlbb/{group}/{endpoint_path:path}", include_in_schema=False, response_class=HTMLResponse)
def openmlbb_endpoint_page(request: Request, group: str, endpoint_path: str) -> HTMLResponse:
    if group not in OPENMLBB_GROUPS:
        raise HTTPException(status_code=404, detail="OpenMLBB group not found")

    all_operations = get_openmlbb_group_operations(request.app, group)
    normalized_path = _normalize_path(f"/openmlbb/{group}/{endpoint_path}")
    matched_operations = [
        operation
        for operation in all_operations
        if _normalize_path(str(operation["openmlbb_path"])) == normalized_path
    ]

    if not matched_operations:
        raise HTTPException(status_code=404, detail="OpenMLBB endpoint not found")

    context = _shared_context(request, current_group=group)
    operation_summary = str(matched_operations[0].get("summary") or "Endpoint").strip()
    context.update(
        {
            "title": f"{operation_summary} / OpenMLBB SDK",
            "web_title": "OpenMLBB Endpoint",
            "subtitle": "SDK call mapping, request requirements, and Python example.",
            "seo_description": f"OpenMLBB endpoint docs for {operation_summary}.",
            "seo_keywords": f"openmlbb endpoint, {group}, python sdk",
            "operations": matched_operations,
            "sidebar_operations": all_operations,
            "selected_openmlbb_path": normalized_path,
        }
    )
    return templates.TemplateResponse(request, "openmlbb/group_page.html", context)
