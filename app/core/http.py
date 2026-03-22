from __future__ import annotations

import random
from typing import Any

import requests

from app.core.exceptions import AppError


class MLBBHeaderBuilder:
    USER_AGENTS = [
        # --- Android (Samsung, Pixel, Xiaomi, OnePlus) ---
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",

        # --- iOS (iPhone, iPad) ---
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.7 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",

        # --- Windows (Chrome, Firefox, Edge) ---
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/143.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",

        # --- macOS (Safari, Chrome, Firefox) ---
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6; rv:128.0) Gecko/20100101 Firefox/128.0",

        # --- Linux (Ubuntu, Fedora) ---
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",

        # --- Misc (Tablet, Legacy, Bots) ---
        "Mozilla/5.0 (Linux; Android 10; Galaxy Tab S6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    ]

    @classmethod
    def get_random_user_agent(cls) -> str:
        return random.choice(cls.USER_AGENTS)

    @staticmethod
    def get_academy_mlbb_header(lang: str) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": MLBBHeaderBuilder.get_random_user_agent(),
        }
        if lang and lang != "en":
            headers["x-lang"] = lang
        return headers
    
    @staticmethod
    def get_identity_header(
        jwt: str | None = None,
        x_token: str | None = None,
        x_actid: str | None = None,
        x_appid: str | None = None,
        lang: str | None = None,
    ) -> dict[str, str]:
        headers = {
            "User-Agent": MLBBHeaderBuilder.get_random_user_agent(),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://www.mobilelegends.com",
            "Referer": "https://www.mobilelegends.com/",
            "DNT": "1",
        }

        if jwt:
            headers["authorization"] = jwt
            headers["x-token"] = jwt

        if x_actid:
            headers["x-actid"] = x_actid

        if x_appid:
            headers["x-appid"] = x_appid

        if x_token:
            headers["x-token"] = x_token

        if lang:
            headers["x-lang"] = lang

        return headers


def request_json(
    *,
    method: str,
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any] | None = None,
) -> Any:
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        else:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
    except requests.RequestException as exc:
        raise AppError(status_code=502, code="UPSTREAM_REQUEST_FAILED", message="Failed to fetch data", details=str(exc)) from exc

    if response.status_code != 200:
        raise AppError(
            status_code=response.status_code,
            code="UPSTREAM_REQUEST_FAILED",
            message="Failed to fetch data",
            details=response.text,
        )

    try:
        return response.json()
    except ValueError as exc:
        raise AppError(status_code=502, code="UPSTREAM_INVALID_RESPONSE", message="Failed to fetch data", details="Invalid JSON from upstream") from exc

def request_form(
    *,
    url: str,
    method: str,
    headers: dict[str, str],
    payload: dict[str, Any],
) -> Any:
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        else:
            response = requests.post(url, data=payload, headers=headers, timeout=30)
    except requests.RequestException as exc:
        raise AppError(status_code=502, code="UPSTREAM_REQUEST_FAILED", message="Failed to fetch data", details=str(exc)) from exc

    if response.status_code != 200:
        raise AppError(
            status_code=response.status_code,
            code="UPSTREAM_REQUEST_FAILED",
            message="Failed to fetch data",
            details=response.text,
        )

    try:
        return response.json()
    except ValueError as exc:
        raise AppError(status_code=502, code="UPSTREAM_INVALID_RESPONSE", message="Failed to fetch data", details="Invalid JSON from upstream") from exc