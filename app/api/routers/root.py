from __future__ import annotations

from datetime import datetime, timezone
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
            "documentation": DOCS_BASE_URL,
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


def _get_other_mlbb_api_endpoints() -> dict[str, str]:
    if IS_AVAILABLE:
        return {"win_rate": "/api/win-rate/?match-now=100&wr-now=50&wr-future=75"}
    return {}


def _get_mpl_id_endpoints() -> dict[str, str]:
    if IS_AVAILABLE:
        return {
            "standings": "/api/mplid/standings/",
            "teams": "/api/mplid/teams/",
            "team_detail": "/api/mplid/teams/{team_id}/",
            "transfers": "/api/mplid/transfers/",
            "team_stats": "/api/mplid/team-stats/",
            "player_stats": "/api/mplid/player-stats/",
            "hero_stats": "/api/mplid/hero-stats/",
            "hero_pools": "/api/mplid/hero-pools/",
            "player_pools": "/api/mplid/player-pools/",
            "standings_mvp": "/api/mplid/standings-mvp/",
            "schedule": "/api/mplid/schedule/",
            "schedule_week": "/api/mplid/schedule/week/{week_number}/",
            "schedule_all_weeks": "/api/mplid/schedule/week/",
        }
    return {}


@router.get("/")
def redirect_to_api() -> RedirectResponse:
    return RedirectResponse(url="/api/", status_code=307)


@router.get("/api")
@router.get("/api/")
@router.get("/api/docs/")
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
            "available_services": ["mlbb_api", "mlbb_academy", "mpl_id", "other_mlbb_api"],
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
            "mpl_id": {
                "status": status_info["status"],
                "message": "MPL ID API is currently under maintenance." if not IS_AVAILABLE else "MPL ID API is online.",
                "base_path": "/api/mplid/",
                "endpoints": _get_mpl_id_endpoints(),
            },
            "other_mlbb_api": {
                "status": status_info["status"],
                "message": "Other MLBB API is currently under maintenance." if not IS_AVAILABLE else "Other MLBB API is online.",
                "base_path": "/api/",
                "endpoints": _get_other_mlbb_api_endpoints(),
            },
        },
        "links": {
            "api_url": base_api_url if IS_AVAILABLE else MAINTENANCE_INFO_URL,
            "web_url": f"{base_web_url}hero-rank/" if IS_AVAILABLE else MAINTENANCE_INFO_URL,
            "docs": base_docs_url,
        },
    }


@router.get("/robots.txt")
def robots_txt() -> PlainTextResponse:
    sitemap_url = urljoin(WEB_BASE_URL, "sitemap.xml")
    content = "\n".join(["User-agent: *", "Allow: /", f"Sitemap: {sitemap_url}"])
    return PlainTextResponse(content=content)


@router.get("/sitemap.xml")
def sitemap_xml() -> Response:
    base_url = WEB_BASE_URL.rstrip("/") + "/"
    lastmod = datetime.now(timezone.utc).date().isoformat()
    url_entries = [
        ("", "weekly", "1.0"),
        ("hero-list/", "daily", "0.9"),
        ("hero-rank/", "daily", "0.9"),
        ("hero-position/", "daily", "0.8"),
        ("hero-detail/1/", "weekly", "0.6"),
        ("api/", "weekly", "0.5"),
        ("api/docs/", "weekly", "0.3"),
    ]
    urls_xml = "\n".join(
        [
            "  <url>\n"
            f"    <loc>{urljoin(base_url, path)}</loc>\n"
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
