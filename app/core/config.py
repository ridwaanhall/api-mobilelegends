from __future__ import annotations

import os
from typing import Callable, TypeVar

from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T")


def _env_cast(key: str, caster: Callable[[str], T], default: T | None = None) -> T:
    value = os.getenv(key)
    if value is None:
        if default is None:
            raise RuntimeError(f"Missing required environment variable: {key}")
        return default
    try:
        return caster(value)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"Invalid value for environment variable {key}: {value!r}") from exc


def _to_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError("Expected boolean string")


def env_str(key: str, default: str | None = None) -> str:
    return _env_cast(key, str, default)


def env_bool(key: str, default: bool) -> bool:
    return _env_cast(key, _to_bool, default)


def env_int(key: str, default: int) -> int:
    return _env_cast(key, int, default)


# =========================
# Debugging
# =========================
DEBUG: bool = env_bool("DEBUG", default=False)

# =========================
# Availability Settings
# =========================
API_VERSION: str = env_str("API_VERSION", default="3.2.0")
IS_AVAILABLE: bool = env_bool("IS_AVAILABLE", default=True)
DATE_AVAILABLE: str = env_str("DATE_AVAILABLE", default="April 1, 2026")

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

DONATION_MIN: int = env_int("DONATION_MIN", default=1)
DONATION_NOW: int = env_int("DONATION_NOW", default=0)
DONATION_TARGET: int = env_int("DONATION_TARGET", default=500)
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
BASE_URL: str = env_str("BASE_URL", default="https://mlbb.rone.dev/")

API_BASE_URL: str = env_str("API_BASE_URL", default=f"{BASE_URL}api/")
DOCS_BASE_URL: str = env_str("DOCS_BASE_URL", default=f"{BASE_URL}docs")

PROD_URL: str = "http://127.0.0.1:8000/api/" if DEBUG else env_str("PROD_URL", default=API_BASE_URL)

LIVECHAT_LINK: str = env_str("LIVECHAT_LINK", default="https://ridwaanhall.com/guestbook/")
CONTACT_FORM_LINK: str = env_str("CONTACT_FORM_LINK", default="https://ridwaanhall.com/contact/")

# =========================
# Security & Access Keys
# =========================
SECRET_KEY: str = env_str("SECRET_KEY")
RONE_DEV_ACCESS_KEY: str = env_str("RONE_DEV_ACCESS_KEY")
RONE_DEV_ACCESS_KEY_V2: str = env_str("RONE_DEV_ACCESS_KEY_V2")
