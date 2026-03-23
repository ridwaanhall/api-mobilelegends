from __future__ import annotations

from typing import cast

from decouple import config


def env_str(key: str, default: str | None = None) -> str:
    if default is None:
        return cast(str, config(key))
    return cast(str, config(key, default=default))


# =========================
# Debugging
# =========================
DEBUG: bool = config("DEBUG", default=False, cast=bool)

# =========================
# Availability Settings
# =========================
API_VERSION: str = env_str("API_VERSION", default="3.1.0")
IS_AVAILABLE: bool = config("IS_AVAILABLE", default=True, cast=bool)
DATE_AVAILABLE: str = env_str("DATE_AVAILABLE", default="March 23, 2026")

# =========================
# FastAPI Site
# =========================
TITLE: str = env_str("TITLE", default="Mobile Legends: Bang Bang (MLBB) Public Data API")
SUMMARY: str = env_str(
    "SUMMARY",
    default="Comprehensive MLBB stats, hero analytics, and academy resources for developers, analysts, and fans.",
)
DESCRIPTION: str = env_str(
    "DESCRIPTION",
    default=(
        "This API provides public access to Mobile Legends: Bang Bang (MLBB) data, including hero listings, rank performance, "
        "role and lane filters, matchup data, and win-rate utilities. It also exposes MLBB Academy resources such as heroes, roles, "
        "equipment, emblems, spells, guides, trends, and ratings. All endpoints are designed for analytics, insights, and integration "
        "into third-party tools. The API features interactive documentation, standardized error payloads, and is powered by data from "
        "official MLBB sources. Ideal for developers, analysts, and fans seeking reliable, up-to-date MLBB information."
    ),
)

# =========================
# Support & Donation Details
# =========================
SUPPORT_DETAILS: dict[str, str] = {
    "support_message": "You can support us by donating from $1 USD (target: $500 USD) to help enhance API performance and handle high request volumes.",
    "github_sponsors": "https://github.com/sponsors/ridwaanhall",
    "buymeacoffee": "https://www.buymeacoffee.com/ridwaanhall",
    "donation_link": "https://github.com/sponsors/ridwaanhall",
    "id_zone_ori": "original server: 688700997 (8742)",
    "id_zone_adv": "advanced server: 1149309666 (57060)",
}

DONATION_MIN: int = config("DONATION_MIN", default=1, cast=int)
DONATION_NOW: int = config("DONATION_NOW", default=0, cast=int)
DONATION_TARGET: int = config("DONATION_TARGET", default=500, cast=int)
DONATION_CURRENCY: str = env_str("DONATION_CURRENCY", default="USD")

# =========================
# API Status Messages
# =========================
API_STATUS_MESSAGES: dict[str, dict[str, str | list[str]]] = {
    "limited": {
        "status": "limited",
        "message": f"API is currently in maintenance mode. Will be available {DATE_AVAILABLE}.",
        "available_endpoints": ["Base API"],
    },
    "available": {
        "status": "available",
        "message": "All API endpoints are fully operational.",
        "available_endpoints": ["All endpoints"],
    },
}

SUPPORT_STATUS_MESSAGES: dict[str, str] = {
    "limited": env_str(
        "SUPPORT_MESSAGE_LIMITED",
        default="API is currently in maintenance mode. Donations help cover hosting and performance scaling.",
    ),
    "available": env_str(
        "SUPPORT_MESSAGE_AVAILABLE",
        default="All API endpoints are fully operational. Donations help cover hosting and performance scaling.",
    ),
}

MAINTENANCE_INFO_URL: str = env_str(
    "MAINTENANCE_INFO_URL",
    default="https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
)

# =========================
# URLs & Endpoints & SEO
# =========================
BASE_URL: str = env_str("BASE_URL", default="https://mlbb-stats.rone.dev/")

API_BASE_URL: str = env_str("API_BASE_URL", default=f"{BASE_URL}api/")
DOCS_BASE_URL: str = env_str("DOCS_BASE_URL", default=f"{BASE_URL}docs")

PROD_URL: str = "http://127.0.0.1:8000/api/" if DEBUG else env_str("PROD_URL", default=API_BASE_URL)

OG_IMAGE_URL: str = env_str("OG_IMAGE_URL", default=f"{BASE_URL}static/favicon.ico")
TWITTER_HANDLE: str = env_str("TWITTER_HANDLE", default="@ridwaanhall")

LIVECHAT_LINK: str = env_str("LIVECHAT_LINK", default="https://ridwaanhall.com/guestbook/")
CONTACT_FORM_LINK: str = env_str("CONTACT_FORM_LINK", default="https://ridwaanhall.com/contact/")

# =========================
# Security & Access Keys
# =========================
SECRET_KEY: str = env_str("SECRET_KEY")
RONE_DEV_ACCESS_KEY: str = env_str("RONE_DEV_ACCESS_KEY")
RONE_DEV_ACCESS_KEY_V2: str = env_str("RONE_DEV_ACCESS_KEY_V2")
