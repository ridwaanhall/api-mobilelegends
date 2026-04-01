from __future__ import annotations

from typing import Annotated, cast

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import API_STATUS_MESSAGES, IS_AVAILABLE
from app.core.exceptions import AppError
from app.core.http import MLBBHeaderBuilder


user_bearer = HTTPBearer(auto_error=False)


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


def require_user_jwt(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(user_bearer)],
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> str:
    if credentials and credentials.credentials:
        return MLBBHeaderBuilder.normalize_auth_token(credentials.credentials)

    if authorization and authorization.strip():
        return MLBBHeaderBuilder.normalize_auth_token(authorization)

    raise AppError(
        status_code=401,
        code="UNAUTHORIZED",
        message="Authorization header is required",
        details="Provide Authorization: Bearer <jwt>.",
    )
