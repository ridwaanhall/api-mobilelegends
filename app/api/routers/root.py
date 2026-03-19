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
    DONATION_TARGET,
    DOCS_BASE_URL,
    IS_AVAILABLE,
    MAINTENANCE_INFO_URL,
    SUPPORT_DETAILS,
    SUPPORT_STATUS_MESSAGES,
    WEB_BASE_URL,
)

router = APIRouter(tags=["root"])


def _get_mlbb_stats_endpoints() -> dict[str, str]:
    if IS_AVAILABLE:
        return {
            "documentation": "/api/docs",
            "hero_list": "/api/hero-list/",
            "hero_rank": "/api/hero-rank/",
            "hero_position": "/api/hero-position/",
            "hero_detail": "/api/hero-detail/{hero_id_or_name}/",
            "hero_detail_stats": "/api/hero-detail-stats/{hero_id_or_name}/",
            "hero_skill_combo": "/api/hero-skill-combo/{hero_id_or_name}/",
            "hero_rate": "/api/hero-rate/{hero_id_or_name}/",
            "hero_relation": "/api/hero-relation/{hero_id_or_name}/",
            "hero_counter": "/api/hero-counter/{hero_id_or_name}/",
            "hero_compatibility": "/api/hero-compatibility/{hero_id_or_name}/",
            "win_rate": "/api/win-rate/?match-now=100&wr-now=50&wr-future=75",
        }
    return {"documentation": DOCS_BASE_URL}


def _get_mlbb_academy_endpoints() -> dict[str, str]:
    if IS_AVAILABLE:
        return {
            "version": "/api/academy/version/",
            "heroes": "/api/academy/heroes/",
            "roles": "/api/academy/roles/",
            "equipment": "/api/academy/equipment/",
            "equipment_details": "/api/academy/equipment-details/",
            "spells": "/api/academy/spells/",
            "emblems": "/api/academy/emblems/",
            "recommended": "/api/academy/recommended/",
            "recommended_detail": "/api/academy/recommended/{recommended_id}/",
            "guide": "/api/academy/guide/",
            "guide_stats": "/api/academy/guide/{hero_id}/stats/",
            "guide_lane": "/api/academy/guide/{hero_id}/lane/",
            "guide_time_win_rate": "/api/academy/guide/{hero_id}/time-win-rate/{lane_id}/",
            "guide_builds": "/api/academy/guide/{hero_id}/builds/",
            "guide_counters": "/api/academy/guide/{hero_id}/counters/",
            "guide_teammates": "/api/academy/guide/{hero_id}/teammates/",
            "guide_trends": "/api/academy/guide/{hero_id}/trends/",
            "guide_recommended": "/api/academy/guide/{hero_id}/recommended/",
            "hero_ratings": "/api/academy/hero-ratings/",
            "hero_ratings_subject": "/api/academy/hero-ratings/{subject}/",
        }
    return {}
@router.get("/")
def redirect_to_api() -> RedirectResponse:
    return RedirectResponse(url="/api/", status_code=307)


@router.get("/api/docs", include_in_schema=False)
@router.get("/api/docs/", include_in_schema=False)
def api_docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)


@router.get("/api")
@router.get("/api/")
def api_index() -> dict[str, object]:
    status_key = "available" if IS_AVAILABLE else "limited"
    status_info = API_STATUS_MESSAGES[status_key]
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    base_api_url = API_BASE_URL.rstrip("/") + "/"
    base_web_url = WEB_BASE_URL.rstrip("/") + "/"
    base_docs_url = DOCS_BASE_URL.rstrip("/") + "/"

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
                "donation_target": DONATION_TARGET,
                "donation_currency": DONATION_CURRENCY,
                "donation_links": {
                    "github_sponsors": SUPPORT_DETAILS["github_sponsors"],
                    "buymeacoffee": SUPPORT_DETAILS["buymeacoffee"],
                },
                "message": SUPPORT_STATUS_MESSAGES[status_key],
            },
            "available_services": ["mlbb_api", "mlbb_academy"],
        },
        "services": {
            "mlbb_api": {
                "status": status_info["status"],
                "message": "MLBB API is currently under maintenance." if not IS_AVAILABLE else "MLBB API is online.",
                "base_path": "/api/",
                "endpoints": _get_mlbb_stats_endpoints(),
            },
            "mlbb_academy": {
                "status": status_info["status"],
                "message": "MLBB Academy API is currently under maintenance." if not IS_AVAILABLE else "MLBB Academy API is online.",
                "base_path": "/api/academy/",
                "endpoints": _get_mlbb_academy_endpoints(),
            },
        },
        "links": {
            "api_url": base_api_url if IS_AVAILABLE else MAINTENANCE_INFO_URL,
            "web_url": f"{base_web_url}hero-rank/" if IS_AVAILABLE else MAINTENANCE_INFO_URL,
            "docs": "/api/docs",
            "external_docs": base_docs_url,
        },
    }


@router.get("/robots.txt")
def robots_txt() -> PlainTextResponse:
    sitemap_url = urljoin(WEB_BASE_URL, "sitemap.xml")
    host_url = WEB_BASE_URL.rstrip("/")
    content = "\n".join(["User-agent: *", "Allow: /", "Disallow:", f"Sitemap: {sitemap_url}", f"Host: {host_url}"])
    return PlainTextResponse(content=content)


@router.get("/sitemap.xml")
def sitemap_xml() -> Response:
    base_url = WEB_BASE_URL.rstrip("/") + "/"
    lastmod = datetime.now(timezone.utc).date().isoformat()
    url_entries = [
        ("", "weekly", "1.0"),
        ("api/", "daily", "1.0"),
        ("docs", "daily", "0.9"),
        ("redoc", "weekly", "0.8"),
        ("api/hero-list/", "daily", "0.9"),
        ("api/hero-rank/", "daily", "0.9"),
        ("api/hero-position/", "daily", "0.9"),
        ("api/hero-detail/1/", "weekly", "0.7"),
        ("api/hero-detail-stats/1/", "weekly", "0.7"),
        ("api/hero-skill-combo/1/", "weekly", "0.7"),
        ("api/hero-rate/1/?past-days=7", "weekly", "0.7"),
        ("api/hero-relation/1/", "weekly", "0.7"),
        ("api/hero-counter/1/", "weekly", "0.7"),
        ("api/hero-compatibility/1/", "weekly", "0.7"),
        ("api/win-rate/?match-now=100&wr-now=50&wr-future=60", "weekly", "0.7"),
        ("api/academy/version/", "daily", "0.9"),
        ("api/academy/heroes/", "daily", "0.9"),
        ("api/academy/roles/", "weekly", "0.8"),
        ("api/academy/equipment/", "weekly", "0.8"),
        ("api/academy/equipment-details/", "weekly", "0.8"),
        ("api/academy/spells/", "weekly", "0.8"),
        ("api/academy/emblems/", "weekly", "0.8"),
        ("api/academy/recommended/", "daily", "0.8"),
        ("api/academy/recommended/1/", "weekly", "0.7"),
        ("api/academy/guide/", "daily", "0.9"),
        ("api/academy/guide/1/stats/", "weekly", "0.7"),
        ("api/academy/guide/1/lane/", "weekly", "0.7"),
        ("api/academy/guide/1/time-win-rate/1/", "weekly", "0.7"),
        ("api/academy/guide/1/builds/", "weekly", "0.7"),
        ("api/academy/guide/1/counters/", "weekly", "0.7"),
        ("api/academy/guide/1/teammates/", "weekly", "0.7"),
        ("api/academy/guide/1/trends/?days=7", "weekly", "0.7"),
        ("api/academy/guide/1/recommended/", "weekly", "0.7"),
        ("api/academy/hero-ratings/", "daily", "0.8"),
    ]
    urls_xml = "\n".join(
        [
            "  <url>\n"
            f"    <loc>{escape(urljoin(base_url, path), quote=False)}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
            for path, freq, priority in url_entries
        ]
    )
    content = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        f"{urls_xml}\n"
        "</urlset>"
    )
    return Response(content=content, media_type="application/xml")
