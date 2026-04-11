from __future__ import annotations

from copy import deepcopy
from typing import Any

from fastapi import FastAPI

from app.web.openapi_catalog import GROUP_META, WEB_GROUPS, get_group_operations

OPENMLBB_GROUPS: tuple[str, ...] = WEB_GROUPS
OPENMLBB_GROUP_META: dict[str, dict[str, str]] = GROUP_META


def _to_openmlbb_path(group: str, api_path: str) -> str:
    if group == "mlbb":
        suffix = api_path.removeprefix("/api")
    else:
        suffix = api_path.removeprefix(f"/api/{group}")

    if not suffix:
        return f"/openmlbb/{group}"

    if not suffix.startswith("/"):
        suffix = f"/{suffix}"
    return f"/openmlbb/{group}{suffix}"


_SDK_MAP: dict[tuple[str, str], dict[str, str]] = {
    ("GET", "/api/academy/meta/version"): {"call": "client.academy.meta_version(**params)"},
    ("GET", "/api/academy/heroes/catalog"): {"call": "client.academy.heroes_catalog(**params)"},
    ("GET", "/api/academy/roles"): {"call": "client.academy.roles(**params)"},
    ("GET", "/api/academy/equipment"): {"call": "client.academy.equipment(**params)"},
    ("GET", "/api/academy/equipment/expanded"): {"call": "client.academy.equipment_expanded(**params)"},
    ("GET", "/api/academy/spells"): {"call": "client.academy.spells(**params)"},
    ("GET", "/api/academy/emblems"): {"call": "client.academy.emblems(**params)"},
    ("GET", "/api/academy/ranks"): {"call": "client.academy.ranks(**params)"},
    ("GET", "/api/academy/ranks/{rank_id}"): {"call": "client.academy.rank_by_id(rank_id, **params)"},
    ("GET", "/api/academy/recommended"): {"call": "client.academy.recommended(**params)"},
    ("GET", "/api/academy/recommended/{recommended_id}"): {"call": "client.academy.recommended_by_id(recommended_id, **params)"},
    ("GET", "/api/academy/heroes"): {"call": "client.academy.heroes(**params)"},
    ("GET", "/api/academy/heroes/{hero_identifier}/stats"): {"call": "client.academy.hero_stats(hero_identifier, **params)"},
    ("GET", "/api/academy/heroes/{hero_identifier}/lane"): {"call": "client.academy.hero_lane(hero_identifier, **params)"},
    ("GET", "/api/academy/heroes/{hero_identifier}/win-rate/timeline"): {"call": "client.academy.hero_win_rate_timeline(hero_identifier, **params)"},
    ("GET", "/api/academy/heroes/{hero_identifier}/builds"): {"call": "client.academy.hero_builds(hero_identifier, **params)"},
    ("GET", "/api/academy/heroes/{hero_identifier}/counters"): {"call": "client.academy.hero_counters(hero_identifier, **params)"},
    ("GET", "/api/academy/heroes/{hero_identifier}/teammates"): {"call": "client.academy.hero_teammates(hero_identifier, **params)"},
    ("GET", "/api/academy/heroes/{hero_identifier}/trends"): {"call": "client.academy.hero_trends(hero_identifier, **params)"},
    ("GET", "/api/academy/heroes/{hero_identifier}/recommended"): {"call": "client.academy.hero_recommended(hero_identifier, **params)"},
    ("GET", "/api/academy/heroes/ratings"): {"call": "client.academy.heroes_ratings(**params)"},
    ("GET", "/api/academy/heroes/ratings/{subject}"): {"call": "client.academy.heroes_ratings_subject(subject, **params)"},
    ("GET", "/api/heroes"): {"call": "client.mlbb.heroes(**params)"},
    ("GET", "/api/heroes/rank"): {"call": "client.mlbb.heroes_rank(**params)"},
    ("GET", "/api/heroes/positions"): {"call": "client.mlbb.heroes_positions(**params)"},
    ("GET", "/api/heroes/{hero_identifier}"): {"call": "client.mlbb.hero_detail(hero_identifier, **params)"},
    ("GET", "/api/heroes/{hero_identifier}/stats"): {"call": "client.mlbb.hero_stats(hero_identifier, **params)"},
    ("GET", "/api/heroes/{hero_identifier}/skill-combos"): {"call": "client.mlbb.hero_skill_combos(hero_identifier, **params)"},
    ("GET", "/api/heroes/{hero_identifier}/trends"): {"call": "client.mlbb.hero_trends(hero_identifier, **params)"},
    ("GET", "/api/heroes/{hero_identifier}/relations"): {"call": "client.mlbb.hero_relations(hero_identifier, **params)"},
    ("GET", "/api/heroes/{hero_identifier}/counters"): {"call": "client.mlbb.hero_counters(hero_identifier, **params)"},
    ("GET", "/api/heroes/{hero_identifier}/compatibility"): {"call": "client.mlbb.hero_compatibility(hero_identifier, **params)"},
    ("POST", "/api/user/auth/send-vc"): {"call": "client.user.send_vc(role_id=1234567890, zone_id=1234)"},
    ("POST", "/api/user/auth/login"): {"call": "client.user.login(role_id=1234567890, zone_id=1234, vc=\"1234\")"},
    ("POST", "/api/user/auth/logout"): {"call": "client.user.logout(jwt=\"YOUR_JWT\")"},
    ("GET", "/api/user/info"): {"call": "client.user.info(jwt=\"YOUR_JWT\", **params)"},
    ("GET", "/api/user/stats"): {"call": "client.user.stats(jwt=\"YOUR_JWT\", **params)"},
    ("GET", "/api/user/privacy/settings"): {"call": "client.user.privacy_settings(jwt=\"YOUR_JWT\", **params)"},
    ("POST", "/api/user/privacy/settings"): {"call": "client.user.update_privacy_settings(jwt=\"YOUR_JWT\", body={...}, **params)"},
    ("GET", "/api/user/season"): {"call": "client.user.season(jwt=\"YOUR_JWT\", **params)"},
    ("GET", "/api/user/matches"): {"call": "client.user.matches(jwt=\"YOUR_JWT\", **params)"},
    ("GET", "/api/user/matches/{match_id}"): {"call": "client.user.match_detail(match_id, jwt=\"YOUR_JWT\", **params)"},
    ("GET", "/api/user/heroes/frequent"): {"call": "client.user.heroes_frequent(jwt=\"YOUR_JWT\", **params)"},
    ("GET", "/api/user/matches/hero/{hero_identifier}"): {"call": "client.user.matches_by_hero(hero_identifier, jwt=\"YOUR_JWT\", **params)"},
    ("GET", "/api/user/friends"): {"call": "client.user.friends(jwt=\"YOUR_JWT\", **params)"},
    ("GET", "/api/addon/win-rate-calculator"): {"call": "client.addon.win_rate_calculator(match_now=100, wr_now=50, wr_future=60)"},
    ("GET", "/api/addon/ip"): {"call": "client.addon.ip()"},
}


def _build_python_example(sdk_call: str) -> str:
    return (
        "from OpenMLBB import OpenMLBB\n\n"
        "client = OpenMLBB()\n"
        f"response = {sdk_call}\n"
        "print(response)"
    )


def get_openmlbb_group_operations(app: FastAPI, group: str) -> list[dict[str, Any]]:
    api_operations = get_group_operations(app, group)
    if not api_operations:
        return []

    operations: list[dict[str, Any]] = []
    for operation in api_operations:
        method = str(operation.get("method") or "").upper()
        api_path = str(operation.get("api_path") or "")

        sdk_info = _SDK_MAP.get((method, api_path), {})
        sdk_call = sdk_info.get("call", "# SDK mapping unavailable for this endpoint")

        op = deepcopy(operation)
        op["openmlbb_path"] = _to_openmlbb_path(group, api_path)
        op["sdk_call"] = sdk_call
        op["sdk_example"] = _build_python_example(sdk_call)
        operations.append(op)

    return operations
