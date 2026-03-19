from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.api.dependencies import require_api_available
from app.core.errors import AppError
from app.services.mlbb import fetch_mlbb_post, resolve_hero_id

router = APIRouter(prefix="/api", tags=["mlbb"], dependencies=[Depends(require_api_available)])

LANGUAGE_DESCRIPTION = (
    "Language code for localized content. Supported codes: "
    "en, id, es, pt, ru, tr, ar, de, fr, it, ja, ko, th, vi, zh-CN, zh-TW. "
    "Default: en."
)

HERO_IDENTIFIER_DESCRIPTION = (
    "Hero identifier as numeric hero ID (recommended range: 1-132) or hero name. "
    "Name matching ignores spaces/symbols and is case-insensitive (example: fanny)."
)

RANK_DESCRIPTION = "Rank filter. Allowed: all, epic, legend, mythic, honor, glory."


def _hero_id_or_404(hero_identifier: str, lang: str) -> int:
    hero_id = resolve_hero_id(hero_identifier, lang)
    if hero_id <= 0:
        raise AppError(
            status_code=404,
            code="RESOURCE_NOT_FOUND",
            message="Hero not found",
            details=f"No hero found with name: {hero_identifier}",
        )
    return hero_id


@router.get("/hero-list/", summary="List heroes")
def hero_list(
    lang: Annotated[
        str,
        Query(
            description=LANGUAGE_DESCRIPTION,
        ),
    ] = "en",
) -> object:
    payload = {
        "pageSize": 10000,
        "sorts": [{"data": {"field": "hero_id", "order": "desc"}, "type": "sequence"}],
        "pageIndex": 1,
        "fields": ["hero_id", "hero.data.head", "hero.data.name", "hero.data.smallmap"],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get("/hero-rank/", summary="Hero rank stats")
def hero_rank(
    days: Annotated[
        Literal["1", "3", "7", "15", "30"],
        Query(description="Past day window. Allowed: 1, 3, 7, 15, 30."),
    ] = "1",
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(description=RANK_DESCRIPTION),
    ] = "all",
    size: Annotated[int, Query(ge=1, le=100, description="Page size. Recommended range: 1-100.")] = 20,
    index: Annotated[int, Query(ge=1, description="Page index (1-based).")]= 1,
    sort_field: Annotated[
        Literal["pick_rate", "ban_rate", "win_rate"],
        Query(description="Sort field. Allowed: pick_rate, ban_rate, win_rate."),
    ] = "win_rate",
    sort_order: Annotated[
        Literal["asc", "desc"],
        Query(description="Sort direction. Allowed: asc, desc."),
    ] = "desc",
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    def create_rank_payload(rank_value: str) -> dict[str, object]:
        return {
            "pageSize": 20,
            "filters": [
                {"field": "bigrank", "operator": "eq", "value": rank_value},
                {"field": "match_type", "operator": "eq", "value": "0"},
            ],
            "sorts": [],
            "pageIndex": 1,
            "fields": [
                "main_hero",
                "main_hero_appearance_rate",
                "main_hero_ban_rate",
                "main_hero_channel",
                "main_hero_win_rate",
                "main_heroid",
                "data.sub_hero.hero",
                "data.sub_hero.hero_channel",
                "data.sub_hero.increase_win_rate",
                "data.sub_hero.heroid",
            ],
        }

    sort_field_map = {
        "pick_rate": "main_hero_appearance_rate",
        "ban_rate": "main_hero_ban_rate",
        "win_rate": "main_hero_win_rate",
    }
    url_map = {"1": "2756567", "3": "2756568", "7": "2756569", "15": "2756565", "30": "2756570"}
    rank_map = {
        "all": create_rank_payload("101"),
        "epic": create_rank_payload("5"),
        "legend": create_rank_payload("6"),
        "mythic": create_rank_payload("7"),
        "honor": create_rank_payload("8"),
        "glory": create_rank_payload("9"),
    }

    payload = rank_map.get(rank, rank_map["all"])
    payload["pageSize"] = int(size)
    payload["pageIndex"] = int(index)
    payload["sorts"] = [
        {"data": {"field": sort_field_map.get(sort_field, "main_hero_win_rate"), "order": sort_order}, "type": "sequence"}
    ]

    return fetch_mlbb_post(url_map.get(days, "2756567"), payload, lang)


@router.get("/hero-position/", summary="Hero position filters")
def hero_position(
    role: Annotated[
        Literal["all", "tank", "fighter", "ass", "mage", "mm", "supp"],
        Query(
            description="Role filter. Allowed: all, tank, fighter, ass (assassin), mage, mm (marksman), supp (support).",
        ),
    ] = "all",
    lane: Annotated[
        Literal["all", "exp", "mid", "roam", "jungle", "gold"],
        Query(description="Lane filter. Allowed: all, exp, mid, roam, jungle, gold."),
    ] = "all",
    size: Annotated[int, Query(ge=1, le=100, description="Page size. Recommended range: 1-100.")] = 21,
    index: Annotated[int, Query(ge=1, description="Page index (1-based).")]= 1,
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    role_map = {
        "all": [1, 2, 3, 4, 5, 6],
        "tank": [1],
        "fighter": [2],
        "ass": [3],
        "mage": [4],
        "mm": [5],
        "supp": [6],
    }
    lane_map = {
        "all": [1, 2, 3, 4, 5],
        "exp": [1],
        "mid": [2],
        "roam": [3],
        "jungle": [4],
        "gold": [5],
    }
    payload = {
        "pageSize": int(size),
        "filters": [
            {"field": "<hero.data.sortid>", "operator": "hasAnyOf", "value": role_map.get(role, [1, 2, 3, 4, 5, 6])},
            {"field": "<hero.data.roadsort>", "operator": "hasAnyOf", "value": lane_map.get(lane, [1, 2, 3, 4, 5])},
        ],
        "sorts": [{"data": {"field": "hero_id", "order": "desc"}, "type": "sequence"}],
        "pageIndex": int(index),
        "fields": ["id", "hero_id", "hero.data.name", "hero.data.smallmap", "hero.data.sortid", "hero.data.roadsort"],
        "object": [],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get("/hero-detail/{hero_identifier}/", summary="Hero detail")
def hero_detail(
    hero_identifier: Annotated[str, Path(description=HERO_IDENTIFIER_DESCRIPTION)],
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": 20,
        "filters": [{"field": "hero_id", "operator": "eq", "value": hero_id}],
        "sorts": [],
        "pageIndex": 1,
        "object": [],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get("/hero-detail-stats/{hero_identifier}/", summary="Hero detail stats")
def hero_detail_stats(
    hero_identifier: Annotated[str, Path(description=HERO_IDENTIFIER_DESCRIPTION)],
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": 20,
        "filters": [
            {"field": "main_heroid", "operator": "eq", "value": hero_id},
            {"field": "bigrank", "operator": "eq", "value": "101"},
            {"field": "match_type", "operator": "eq", "value": "1"},
        ],
        "sorts": [],
        "pageIndex": 1,
    }
    return fetch_mlbb_post("2756567", payload, lang)


@router.get("/hero-skill-combo/{hero_identifier}/", summary="Hero skill combo")
def hero_skill_combo(
    hero_identifier: Annotated[str, Path(description=HERO_IDENTIFIER_DESCRIPTION)],
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": 20,
        "filters": [{"field": "hero_id", "operator": "eq", "value": hero_id}],
        "sorts": [],
        "pageIndex": 1,
        "object": [2684183],
    }
    return fetch_mlbb_post("2674711", payload, lang)


@router.get("/hero-rate/{hero_identifier}/", summary="Hero rate trends")
def hero_rate(
    hero_identifier: Annotated[str, Path(description=HERO_IDENTIFIER_DESCRIPTION)],
    past_days: Annotated[
        Literal["7", "15", "30"],
        Query(alias="past-days", description="Rate window in days. Allowed: 7, 15, 30."),
    ] = "7",
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    url_map = {"7": "2674709", "15": "2687909", "30": "2690860"}
    payload = {
        "pageSize": 20,
        "filters": [
            {"field": "main_heroid", "operator": "eq", "value": hero_id},
            {"field": "bigrank", "operator": "eq", "value": "8"},
            {"field": "match_type", "operator": "eq", "value": "1"},
        ],
        "sorts": [],
        "pageIndex": 1,
    }
    return fetch_mlbb_post(url_map.get(past_days, "2674709"), payload, lang)


@router.get("/hero-relation/{hero_identifier}/", summary="Hero relation")
def hero_relation(
    hero_identifier: Annotated[str, Path(description=HERO_IDENTIFIER_DESCRIPTION)],
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": 20,
        "filters": [{"field": "hero_id", "operator": "eq", "value": hero_id}],
        "sorts": [],
        "pageIndex": 1,
        "fields": ["hero.data.name"],
        "object": [],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get("/hero-counter/{hero_identifier}/", summary="Hero counters")
def hero_counter(
    hero_identifier: Annotated[str, Path(description=HERO_IDENTIFIER_DESCRIPTION)],
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": 20,
        "filters": [
            {"field": "match_type", "operator": "eq", "value": "0"},
            {"field": "main_heroid", "operator": "eq", "value": hero_id},
            {"field": "bigrank", "operator": "eq", "value": "7"},
        ],
        "sorts": [],
        "pageIndex": 1,
    }
    return fetch_mlbb_post("2756569", payload, lang)


@router.get("/hero-compatibility/{hero_identifier}/", summary="Hero compatibility")
def hero_compatibility(
    hero_identifier: Annotated[str, Path(description=HERO_IDENTIFIER_DESCRIPTION)],
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": 20,
        "filters": [
            {"field": "match_type", "operator": "eq", "value": "1"},
            {"field": "main_heroid", "operator": "eq", "value": hero_id},
            {"field": "bigrank", "operator": "eq", "value": "7"},
        ],
        "sorts": [],
        "pageIndex": 1,
    }
    return fetch_mlbb_post("2756569", payload, lang)


@router.get("/win-rate/", summary="Win-rate calculator")
def win_rate(
    match_now: Annotated[
        str | None,
        Query(alias="match-now", description="Current total matches. Must be an integer >= 0."),
    ] = None,
    wr_now: Annotated[
        str | None,
        Query(alias="wr-now", description="Current win rate in percent. Range: 0-100."),
    ] = None,
    wr_future: Annotated[
        str | None,
        Query(
            alias="wr-future",
            description="Target win rate in percent. Range: >0 to 100 and must be greater than wr-now.",
        ),
    ] = None,
) -> object:
    missing_params = [
        param
        for param, value in [("match-now", match_now), ("wr-now", wr_now), ("wr-future", wr_future)]
        if value is None or value == ""
    ]
    if missing_params:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now,
                "wr_now": wr_now,
                "wr_future": wr_future,
                "required_no_lose_matches": None,
                "message": (
                    f"Missing required parameter(s): {', '.join(missing_params)}. "
                    "Please provide all required parameters: match-now, wr-now, and wr-future."
                ),
            },
        )

    try:
        if "." in str(match_now):
            raise ValueError("match-now must be an integer (no decimals allowed).")
        match_now_int = int(str(match_now))
        wr_now_float = float(str(wr_now))
        wr_future_float = float(str(wr_future))
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now,
                "wr_now": wr_now,
                "wr_future": wr_future,
                "required_no_lose_matches": None,
                "message": "Invalid input. Ensure match-now is an integer and wr-now, wr-future are numeric values.",
            },
        )

    if match_now_int < 0:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "match-now must be a non-negative integer.",
            },
        )

    if not (0 <= wr_now_float <= 100) or not (0 < wr_future_float <= 100):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "Win rates must be between 0 and 100 (wr-future must be greater than 0).",
            },
        )

    if wr_future_float <= wr_now_float:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "The target win rate (wr-future) must be greater than the current win rate (wr-now).",
            },
        )

    current_wins = match_now_int * wr_now_float / 100.0
    wr_future_ratio = wr_future_float / 100.0
    denominator = wr_future_ratio - 1.0
    numerator = current_wins - match_now_int * wr_future_ratio

    if denominator == 0:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": f"It is not possible to reach a {wr_future_float}% win rate with a finite number of matches.",
            },
        )

    required_matches = numerator / denominator
    required_matches_int = int(required_matches) + (1 if required_matches % 1 > 0 else 0)

    if required_matches_int < 0:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "match_now": match_now_int,
                "wr_now": wr_now_float,
                "wr_future": wr_future_float,
                "required_no_lose_matches": None,
                "message": "The target win rate cannot be achieved with only consecutive wins from your current record.",
            },
        )

    return {
        "status": "success",
        "match_now": match_now_int,
        "wr_now": wr_now_float,
        "wr_future": wr_future_float,
        "required_no_lose_matches": required_matches_int,
        "message": (
            f"To achieve a win rate of {wr_future_float}%, "
            f"you need {required_matches_int} consecutive wins without any losses."
        ),
    }
