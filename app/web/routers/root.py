from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.web.openapi_catalog import GROUP_META, WEB_GROUPS, get_group_operations

router = APIRouter(tags=["web"])

_TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))


def _shared_context(request: Request, current_group: str | None = None) -> dict[str, object]:
	return {
		"request": request,
		"group_meta": GROUP_META,
		"groups": WEB_GROUPS,
		"current_group": current_group,
	}


def _normalize_path(value: str) -> str:
	normalized = value.rstrip("/")
	return normalized or "/"


@router.get(path="/", include_in_schema=False, response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
	context = _shared_context(request)
	return templates.TemplateResponse(request, "root/landing_page.html", context)


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
			"title": f"{GROUP_META[group]['title']} Endpoints",
			"subtitle": GROUP_META[group]["description"],
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
	context.update(
		{
			"title": f"{GROUP_META[group]['title']} Endpoint",
			"subtitle": "Interactive request form for this API endpoint.",
			"operations": matched_operations,
			"sidebar_operations": all_operations,
			"selected_web_path": normalized_path,
		}
	)
	return templates.TemplateResponse(request, "web/group_page.html", context)
