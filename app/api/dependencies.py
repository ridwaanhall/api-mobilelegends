from __future__ import annotations

from typing import cast

from app.core.config import API_STATUS_MESSAGES, IS_AVAILABLE
from app.core.errors import AppError


def require_api_available() -> None:
    if IS_AVAILABLE:
        return

    status_info = API_STATUS_MESSAGES["limited"]
    raise AppError(
        status_code=503,
        code="SERVICE_UNAVAILABLE",
        message=cast(str, status_info["message"]),
        details={
            "available_endpoints": status_info["available_endpoints"],
        },
    )
