from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import re

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.config import API_VERSION
from app.web.openapi_catalog import GROUP_META, WEB_GROUPS, get_group_operations

router = APIRouter(tags=["web"])

_TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))


def _slugify_title(title: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", title.lower())
    return cleaned.strip("-")


_BLOG_POSTS: list[dict[str, object]] = [
    {
        "title": "How to Use MLBB Public Data API Web Project",
        "excerpt": "Complete beginner tutorial to sign in, run endpoint requests, use snippets, read responses, and authorize API docs.",
        "cover_image": "/images/blog/how-to-use-mlbb-public-data-api-web-project-cover.png",
        "published_at": "2026-04-04",
        "read_time": "8 min read",
        "sections": [
            {
                "heading": "Step 1: Open the Website",
                "body": "Visit https://mlbb.rone.dev. On the home page you will see two options: Open Demo Website and Open API Docs. Recommended path for most users is Open Demo Website.",
                "image": "/images/blog/tutorial-step-1-home.png",
                "image_note": "Replace this image at images/blog/tutorial-step-1-home.png",
            },
            {
                "heading": "Step 2: Sign In (Required for User Endpoints)",
                "body": "Click Sign In in the navbar, then fill Role ID and Zone ID once. Click Send VC. A verification code (VC) is sent to in-game mail and expires in 5 minutes.",
                "image": "/images/blog/tutorial-step-2-signin-send-vc.png",
                "image_note": "Replace this image at images/blog/tutorial-step-2-signin-send-vc.png",
            },
            {
                "heading": "Step 3: Login with VC",
                "body": "In the same popup, enter the VC and click Sign In. After success, your profile photo, username, and country appear in navbar. Click your name to see roleId (zoneId) and Copy JWT.",
                "image": "/images/blog/tutorial-step-3-login-vc.png",
                "image_note": "Replace this image at images/blog/tutorial-step-3-login-vc.png",
            },
            {
                "heading": "Step 4: Run Endpoint Requests from Demo Website",
                "body": "Select any endpoint group and endpoint. Example: MLBB heroes detail endpoint. Fill hero_identifier (accepts hero ID or name), optional size/index/lang, then click Execute.",
                "image": "/images/blog/tutorial-step-4-execute-endpoint.png",
                "image_note": "Replace this image at images/blog/tutorial-step-4-execute-endpoint.png",
            },
            {
                "heading": "Step 5: Use Snippets, Readable Response, and Raw JSON",
                "body": "After execution, use language snippets (curl, python, javascript, go, node, php, java, csharp) and Copy Snippet. Review Readable Response with View mode switch (Key-Value or Key As Header), and use Raw JSON + Copy Response when needed.",
                "image": "/images/blog/tutorial-step-5-response-views.png",
                "image_note": "Replace this image at images/blog/tutorial-step-5-response-views.png",
            },
            {
                "heading": "Step 6: Option 2 - Open API Docs",
                "body": "If you prefer Swagger UI, open API Docs from home page. For user endpoints, use JWT from Copy JWT in navbar and authorize with Bearer token in docs.",
                "image": "/images/blog/tutorial-step-6-api-docs-auth.png",
                "image_note": "Replace this image at images/blog/tutorial-step-6-api-docs-auth.png",
            },
        ],
    }
]

for post in _BLOG_POSTS:
    title = str(post.get("title") or "")
    post["slug"] = _slugify_title(title)


def _get_blog_post_or_404(slug: str) -> dict[str, object]:
    normalized = slug.strip().lower()
    for post in _BLOG_POSTS:
        if str(post.get("slug") or "") == normalized:
            return post
    raise HTTPException(status_code=404, detail="Blog post not found")


def _shared_context(request: Request, current_group: str | None = None) -> dict[str, object]:
    return {
        "request": request,
        "group_meta": GROUP_META,
        "groups": WEB_GROUPS,
        "current_group": current_group,
        "current_year": datetime.now(UTC).year,
        "api_version": API_VERSION,
        "seo_description": "Interactive web interface for MLBB Public Data API with endpoint forms, readable response tables, and cURL output.",
        "seo_keywords": "mlbb api, mobile legends api, web ui, fastapi, openapi, response table",
    }


def _normalize_path(value: str) -> str:
    normalized = value.rstrip("/")
    return normalized or "/"


@router.get(path="/", include_in_schema=False, response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
    context = _shared_context(request)
    context.update(
        {
            "title": "Home / MLBB Public Data API & Web",
            "web_title": "Home",
            "seo_description": "Modern landing page for MLBB Public Data API. Access docs and a full interactive web playground for all endpoints.",
            "seo_keywords": "mlbb, mobile legends, api docs, web playground, analytics api",
        }
    )
    return templates.TemplateResponse(request, "root/landing_page.html", context)


@router.get(path="/web", include_in_schema=False)
def web_home() -> RedirectResponse:
    return RedirectResponse(url="/web/user", status_code=307)


@router.get(path="/blog", include_in_schema=False, response_class=HTMLResponse)
def blog_list_page(request: Request) -> HTMLResponse:
    context = _shared_context(request)
    context.update(
        {
            "title": "Tutorial & Blog / MLBB Public Data API Web",
            "web_title": "Tutorial & Blog",
            "subtitle": "Guides and practical tutorials for using MLBB Public Data API & Web effectively.",
            "seo_description": "Read MLBB Public Data API tutorials: login flow, endpoint execution, snippets, readable responses, and API docs authorization.",
            "seo_keywords": "mlbb api tutorial, mlbb web tutorial, mobile legends api guide, swagger authorization",
            "blog_posts": _BLOG_POSTS,
        }
    )
    return templates.TemplateResponse(request, "blog/list_page.html", context)


@router.get(path="/blog/{slug}", include_in_schema=False, response_class=HTMLResponse)
def blog_detail_page(request: Request, slug: str) -> HTMLResponse:
    post = _get_blog_post_or_404(slug)
    context = _shared_context(request)
    context.update(
        {
            "title": f"{post['title']} / MLBB Public Data API Web",
            "web_title": str(post["title"]),
            "subtitle": str(post["excerpt"]),
            "seo_description": str(post["excerpt"]),
            "seo_keywords": "mlbb tutorial, mlbb api guide, endpoint tutorial, jwt login tutorial",
            "blog_post": post,
        }
    )
    return templates.TemplateResponse(request, "blog/detail_page.html", context)


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
