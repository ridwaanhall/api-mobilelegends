from __future__ import annotations

from typing import cast

from decouple import config


def env_str(key: str, default: str | None = None) -> str:
    if default is None:
        return cast(str, config(key))
    return cast(str, config(key, default=default))


IS_AVAILABLE: bool = config("IS_AVAILABLE", default=True, cast=bool)
DATE_AVAILABLE: str = env_str("DATE_AVAILABLE", default="March 31, 2026")

SUPPORT_DETAILS: dict[str, str] = {
    "support_message": "You can support us by donating from $1 USD (target: $500 USD) to help enhance API performance and handle high request volumes.",
    "github_sponsors": "https://github.com/sponsors/ridwaanhall",
    "buymeacoffee": "https://www.buymeacoffee.com/ridwaanhall",
    "donation_link": "https://github.com/sponsors/ridwaanhall",
    "id_zone_ori": "original server: 688700997 (8742)",
    "id_zone_adv": "advanced server: 1149309666 (57060)",
}

SITE_TITLE: str = "API Mobile Legends"
TWITTER_HANDLE: str = env_str("TWITTER_HANDLE", default="@ridwaanhall")

WEB_BASE_URL: str = env_str("WEB_BASE_URL", default="https://mlbb-stats.rone.dev/")
API_BASE_URL: str = env_str("API_BASE_URL", default=f"{WEB_BASE_URL}api/")
DOCS_BASE_URL: str = env_str("DOCS_BASE_URL", default="https://mlbb-stats.rone.dev/docs")
OG_IMAGE_URL: str = env_str("OG_IMAGE_URL", default=f"{WEB_BASE_URL}static/favicon.ico")

MAINTENANCE_INFO_URL: str = env_str(
    "MAINTENANCE_INFO_URL",
    default="https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
)

DONATION_MIN: int = config("DONATION_MIN", default=1, cast=int)
DONATION_TARGET: int = config("DONATION_TARGET", default=500, cast=int)
DONATION_CURRENCY: str = env_str("DONATION_CURRENCY", default="USD")

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

API_VERSION: str = env_str("API_VERSION", default="3.0.0")
SECRET_KEY: str = env_str("SECRET_KEY")
MLBB_URL: str = env_str("MLBB_URL")
MLBB_URL_V2: str = env_str("MLBB_URL_V2")

DEBUG: bool = config("DEBUG", default=False, cast=bool)
PROD_URL: str = "http://127.0.0.1:8000/api/" if DEBUG else env_str("PROD_URL", default=API_BASE_URL)
