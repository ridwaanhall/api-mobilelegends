from __future__ import annotations

from typing import Any

from app.core.http import request_form
from app.core.security import BaseIdentityPathProvider


def fetch_identity_post(path: str, payload: dict[str, Any], headers: dict) -> Any:
    base_path = BaseIdentityPathProvider.get_base_url_path_auth()
    url = f"{base_path}/{path}"
    return request_form(method="POST", url=url, payload=payload, headers=headers)