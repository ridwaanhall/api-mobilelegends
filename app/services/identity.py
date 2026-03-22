from __future__ import annotations

from typing import Any

from app.core.http import MLBBHeaderBuilder, request_form
from app.core.security import BaseIdentityPathProvider


def fetch_vc_service(
    path: str,
    role_id: int,
    zone_id: int
) -> Any:
    base_path = BaseIdentityPathProvider.get_base_url_path_auth()
    url = f"{base_path}/{path}"
    headers = MLBBHeaderBuilder.get_identity_header()
    payload = {
        "roleId": role_id,
        "zoneId": zone_id
    }
    return request_form(method="POST", url=url, payload=payload, headers=headers)


def fetch_login_service(
    path: str,
    role_id: int,
    zone_id: int,
    vc: int,
    referer: str = "academy",
    type_: str = "web"
) -> Any:
    base_url = BaseIdentityPathProvider.get_base_url_path_auth()
    url = f"{base_url}/{path}"
    headers = MLBBHeaderBuilder.get_identity_header()
    payload = {
        "roleId": role_id,
        "zoneId": zone_id,
        "vc": vc,
        "referer": referer,
        "type": type_,
    }
    return request_form(method="POST", url=url, payload=payload, headers=headers)

def fetch_user_service(
    path: str,
    jwt: str,
    x_actid: str = "2728785",
    x_appid: str = "2713644",
    lang: str = "en",
) -> Any:
    base_url = BaseIdentityPathProvider.get_base_url_path_auth()
    url = f"{base_url}/{path}"
    headers = MLBBHeaderBuilder.get_identity_header(
        lang=lang,
        x_actid=x_actid,
        x_appid=x_appid,
        jwt=jwt
    )
    return request_form(method="POST", url=url, payload={}, headers=headers)

def fetch_logout_service(
    path: str,
    jwt: str,
    token: str
) -> Any:
    base_url = BaseIdentityPathProvider.get_base_url_path_auth()
    url = f"{base_url}/{path}"
    headers = MLBBHeaderBuilder.get_identity_header(
        jwt=jwt,
    )
    payload = {
        "token": token
    }
    return request_form(method="POST", url=url, payload=payload, headers=headers)