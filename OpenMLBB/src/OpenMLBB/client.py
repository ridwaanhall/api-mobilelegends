from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


DEFAULT_BASE_URL = "https://mlbb.rone.dev/api"
DEFAULT_TIMEOUT = 30
DEFAULT_USER_AGENT = "RoneAI-OpenMLBB-Python-SDK"


class OpenMLBBError(Exception):
    """Raised when an OpenMLBB request fails."""

    def __init__(self, message: str, status_code: int | None = None, payload: Any = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


@dataclass(slots=True)
class _Transport:
    base_url: str
    timeout: int
    user_agent: str
    session: requests.Session

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        jwt: str | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        headers: dict[str, str] = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }
        if jwt:
            headers["Authorization"] = f"Bearer {jwt}"

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json_body,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise OpenMLBBError(f"Request failed: {exc}") from exc

        try:
            payload: Any = response.json()
        except ValueError:
            payload = {"raw": response.text}

        if not response.ok:
            raise OpenMLBBError(
                message=f"OpenMLBB API request failed with status {response.status_code}",
                status_code=response.status_code,
                payload=payload,
            )

        if isinstance(payload, dict):
            return payload

        return {"data": payload}


class AcademyClient:
    def __init__(self, transport: _Transport) -> None:
        self._transport = transport

    def meta_version(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/meta/version", params=params)

    def heroes_catalog(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/heroes/catalog", params=params)

    def roles(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/roles", params=params)

    def equipment(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/equipment", params=params)

    def equipment_expanded(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/equipment/expanded", params=params)

    def spells(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/spells", params=params)

    def emblems(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/emblems", params=params)

    def ranks(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/ranks", params=params)

    def rank_by_id(self, rank_id: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/ranks/{rank_id}", params=params)

    def recommended(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/recommended", params=params)

    def recommended_by_id(self, recommended_id: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/recommended/{recommended_id}", params=params)

    def heroes(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/heroes", params=params)

    def hero_stats(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/heroes/{hero_identifier}/stats", params=params)

    def hero_lane(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/heroes/{hero_identifier}/lane", params=params)

    def hero_win_rate_timeline(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/heroes/{hero_identifier}/win-rate/timeline", params=params)

    def hero_builds(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/heroes/{hero_identifier}/builds", params=params)

    def hero_counters(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/heroes/{hero_identifier}/counters", params=params)

    def hero_teammates(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/heroes/{hero_identifier}/teammates", params=params)

    def hero_trends(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/heroes/{hero_identifier}/trends", params=params)

    def hero_recommended(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/heroes/{hero_identifier}/recommended", params=params)

    def heroes_ratings(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/academy/heroes/ratings", params=params)

    def heroes_ratings_subject(self, subject: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/academy/heroes/ratings/{subject}", params=params)


class MlbbClient:
    def __init__(self, transport: _Transport) -> None:
        self._transport = transport

    def heroes(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/heroes", params=params)

    def heroes_rank(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/heroes/rank", params=params)

    def heroes_positions(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/heroes/positions", params=params)

    def hero_detail(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/heroes/{hero_identifier}", params=params)

    def hero_stats(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/heroes/{hero_identifier}/stats", params=params)

    def hero_skill_combos(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/heroes/{hero_identifier}/skill-combos", params=params)

    def hero_trends(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/heroes/{hero_identifier}/trends", params=params)

    def hero_relations(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/heroes/{hero_identifier}/relations", params=params)

    def hero_counters(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/heroes/{hero_identifier}/counters", params=params)

    def hero_compatibility(self, hero_identifier: str | int, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/heroes/{hero_identifier}/compatibility", params=params)


class UserClient:
    def __init__(self, transport: _Transport) -> None:
        self._transport = transport

    def send_vc(self, role_id: int, zone_id: int) -> dict[str, Any]:
        body = {"role_id": role_id, "zone_id": zone_id}
        return self._transport.request("POST", "/user/auth/send-vc", json_body=body)

    def login(self, role_id: int, zone_id: int, vc: str) -> dict[str, Any]:
        body = {"role_id": role_id, "zone_id": zone_id, "vc": vc}
        return self._transport.request("POST", "/user/auth/login", json_body=body)

    def logout(self, jwt: str) -> dict[str, Any]:
        return self._transport.request("POST", "/user/auth/logout", jwt=jwt)

    def info(self, jwt: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/user/info", params=params, jwt=jwt)

    def stats(self, jwt: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/user/stats", params=params, jwt=jwt)

    def privacy_settings(self, jwt: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/user/privacy/settings", params=params, jwt=jwt)

    def update_privacy_settings(self, jwt: str, body: dict[str, Any], **params: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/user/privacy/settings", params=params, json_body=body, jwt=jwt)

    def season(self, jwt: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/user/season", params=params, jwt=jwt)

    def matches(self, jwt: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/user/matches", params=params, jwt=jwt)

    def match_detail(self, match_id: str | int, jwt: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/user/matches/{match_id}", params=params, jwt=jwt)

    def heroes_frequent(self, jwt: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/user/heroes/frequent", params=params, jwt=jwt)

    def matches_by_hero(self, hero_identifier: str | int, jwt: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", f"/user/matches/hero/{hero_identifier}", params=params, jwt=jwt)

    def friends(self, jwt: str, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/user/friends", params=params, jwt=jwt)


class AddonClient:
    def __init__(self, transport: _Transport) -> None:
        self._transport = transport

    def win_rate_calculator(self, match_now: int, wr_now: float, wr_future: float) -> dict[str, Any]:
        params = {
            "match-now": match_now,
            "wr-now": wr_now,
            "wr-future": wr_future,
        }
        return self._transport.request("GET", "/addon/win-rate-calculator", params=params)

    def ip(self) -> dict[str, Any]:
        return self._transport.request("GET", "/addon/ip")


class OpenMLBB:
    """Python SDK for https://mlbb.rone.dev/api."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        session: requests.Session | None = None,
    ) -> None:
        active_session = session or requests.Session()
        self._transport = _Transport(
            base_url=base_url,
            timeout=timeout,
            user_agent=user_agent,
            session=active_session,
        )

        self.academy = AcademyClient(self._transport)
        self.mlbb = MlbbClient(self._transport)
        self.user = UserClient(self._transport)
        self.addon = AddonClient(self._transport)
