from __future__ import annotations

from typing import Any

from app.core.config import MLBB_URL, MLBB_URL_V2
from app.core.http import MLBBHeaderBuilder, request_json
from app.core.security import BasePathProvider


def fetch_academy_post(endpoint_id: str, payload: dict[str, Any], lang: str) -> Any:
    base_path = BasePathProvider.get_base_path_academy()
    url = f"{MLBB_URL}{base_path}/{endpoint_id}"
    headers = MLBBHeaderBuilder.get_lang_header(lang)
    return request_json(method="POST", url=url, payload=payload, headers=headers)


def fetch_ratings_all(lang: str) -> Any:
    base_path = BasePathProvider.get_base_path_ratings()
    url = f"{MLBB_URL_V2}{base_path}?offset=0"
    headers = MLBBHeaderBuilder.get_lang_header(lang)
    return request_json(method="GET", url=url, headers=headers)


def fetch_ratings_subject(lang: str, subject: str) -> Any:
    base_path = BasePathProvider.get_base_path_ratings()
    url = f"{MLBB_URL_V2}{base_path}/{subject}"
    headers = MLBBHeaderBuilder.get_lang_header(lang)
    return request_json(method="GET", url=url, headers=headers)
