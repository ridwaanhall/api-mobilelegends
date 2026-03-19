from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query

from app.api.dependencies import require_api_available
from app.core.hero_limits import validate_academy_hero_id
from app.services.academy import fetch_academy_post, fetch_ratings_all, fetch_ratings_subject

router = APIRouter(prefix="/api/academy", tags=["academy"], dependencies=[Depends(require_api_available)])

LANGUAGE_DESCRIPTION = (
    "Language code for localized content. Supported codes: "
    "en, id, es, pt, ru, tr, ar, de, fr, it, ja, ko, th, vi, zh-CN, zh-TW. "
    "Default: en."
)

RANK_DESCRIPTION = "Rank filter. Allowed: all, epic, legend, mythic, honor, glory."
HERO_ID_DESCRIPTION = (
    "Hero ID. Minimum: 1. Maximum is validated dynamically from current `/api/academy/guide` total."
)


def _rank_value(rank: str) -> str:
    rank_map = {
        "all": "101",
        "epic": "5",
        "legend": "6",
        "mythic": "7",
        "honor": "8",
        "glory": "9",
    }
    return rank_map.get(rank.lower(), "101")


@router.get("/version", summary="Academy version info")
def version(lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en") -> object:
    payload = {
        "pageSize": 20,
        "pageIndex": 1,
        "filters": [{"field": "formId", "operator": "eq", "value": 2777742}],
        "sorts": [{"data": {"field": "createdAt", "order": "desc"}, "type": "sequence"}],
        "type": "form.item.all",
        "object": [2675413],
    }
    return fetch_academy_post("2718124", payload, lang)


@router.get("/heroes", summary="Academy hero catalog")
def heroes(lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en") -> object:
    payload = {
        "pageSize": 200,
        "pageIndex": 1,
        "filters": [],
        "sorts": [],
        "fields": ["head", "head_big", "hero.data.name", "hero.data.roadsort", "hero_id", "painting"],
        "object": [2667538],
    }
    return fetch_academy_post("2766683", payload, lang)


@router.get("/roles", summary="Role and emblem list")
def roles(lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en") -> object:
    payload = {
        "pageSize": 50,
        "pageIndex": 1,
        "filters": [],
        "sorts": [{"data": {"field": "emblem_id", "order": "asc"}, "type": "sequence"}],
        "object": [],
    }
    return fetch_academy_post("2740642", payload, lang)


@router.get("/equipment", summary="Equipment list")
def equipment(lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en") -> object:
    payload = {"pageSize": 200, "pageIndex": 1, "filters": [], "sorts": []}
    return fetch_academy_post("2775075", payload, lang)


@router.get("/equipment-details", summary="Equipment detail list")
def equipment_details(lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en") -> object:
    payload = {"pageSize": 200, "pageIndex": 1, "filters": [], "sorts": []}
    return fetch_academy_post("2713995", payload, lang)


@router.get("/spells", summary="Battle spells list")
def spells(lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en") -> object:
    payload = {"pageSize": 200, "pageIndex": 1, "filters": [], "sorts": []}
    return fetch_academy_post("2718122", payload, lang)


@router.get("/emblems", summary="Emblems list")
def emblems(lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en") -> object:
    payload = {"pageSize": 50, "pageIndex": 1, "filters": [], "sorts": []}
    return fetch_academy_post("2718121", payload, lang)


@router.get("/recommended", summary="Recommended content list")
def recommended(
    page: Annotated[int, Query(ge=1, description="Page index (1-based).")] = 1,
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    payload = {
        "pageSize": 10,
        "pageIndex": page,
        "filters": [
            {"field": "formId", "operator": "eq", "value": 2737553},
            {"field": "data.state", "operator": "eq", "value": "release"},
            {"field": "data.channels", "operator": "in", "value": ["recommend"]},
            {"field": "uin", "operator": "contain", "value": "/.*/"},
            {"field": "data.data.game_version", "operator": "contain", "value": "/.*/"},
            {"field": "data.data.language", "operator": "eq", "value": lang},
            {"field": "createdAt", "operator": "gte", "value": 1},
        ],
        "sorts": [
            {"data": {"field": "dynamic.hot", "order": "desc"}, "type": "sequence"},
            {"data": {"field": "createdAt", "order": "desc"}, "type": "sequence"},
        ],
        "type": "form.item.all",
        "object": [2675413],
    }
    return fetch_academy_post("2718124", payload, lang)


@router.get("/recommended/{recommended_id}", summary="Recommended content detail")
def recommended_detail(
    recommended_id: Annotated[int, Path(ge=1, description="Recommended post identifier.")],
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    payload = {
        "pageSize": 20,
        "pageIndex": 1,
        "filters": [
            {"field": "formId", "operator": "eq", "value": 2737553},
            {"field": "id", "operator": "eq", "value": recommended_id},
            {"field": "data.state", "operator": "eq", "value": "release"},
        ],
        "sorts": [],
        "type": "form.item.all",
        "object": [2675413],
    }
    return fetch_academy_post("2718124", payload, lang)


@router.get("/guide", summary="Guide hero list")
def guide(
    size: Annotated[int, Query(ge=1, le=5000, description="Page size. Recommended range: 1-5000.")] = 2000,
    page: Annotated[int, Query(ge=1, description="Page index (1-based).")] = 1,
    role: Annotated[
        str | None,
        Query(
            description="Role code list separated by comma. Allowed values: t (tank), f (fighter), a (assassin), m (mage), mm (marksman), s (support). Example: t,mm",
        ),
    ] = None,
    lane: Annotated[
        str | None,
        Query(
            description="Lane code list separated by comma. Allowed values: e (exp), m (mid), r (roam), j (jungle), g (gold). Example: e,j",
        ),
    ] = None,
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    role_map = {"t": 1, "f": 2, "a": 3, "m": 4, "mm": 5, "s": 6}
    lane_map = {"e": 1, "m": 2, "r": 3, "j": 4, "g": 5}

    role_values: list[int] = []
    if role:
        role_values = [role_map[item] for item in role.split(",") if item in role_map]

    lane_values: list[int] = []
    if lane:
        lane_values = [lane_map[item] for item in lane.split(",") if item in lane_map]

    payload = {
        "pageSize": size,
        "pageIndex": page,
        "filters": [
            {"field": "<hero.data.sortid>", "operator": "hasAnyOf", "value": role_values or [1, 2, 3, 4, 5, 6]},
            {"field": "<hero.data.roadsort>", "operator": "hasAnyOf", "value": lane_values or [1, 2, 3, 4, 5]},
        ],
        "sorts": [{"data": {"field": "hero_id", "order": "desc"}, "type": "sequence"}],
        "fields": ["head", "hero_id", "hero.data.name"],
        "object": [],
    }
    return fetch_academy_post("2766683", payload, lang)


@router.get("/guide/{hero_id}/stats", summary="Guide hero stats")
def guide_stats(
    hero_id: Annotated[int, Path(ge=1, description=HERO_ID_DESCRIPTION)],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(description=RANK_DESCRIPTION),
    ] = "all",
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": 20,
        "pageIndex": 1,
        "filters": [
            {"field": "main_heroid", "operator": "eq", "value": hero_id},
            {"field": "bigrank", "operator": "eq", "value": _rank_value(rank)},
            {"field": "match_type", "operator": "eq", "value": 1},
        ],
        "sorts": [],
    }
    return fetch_academy_post("2755183", payload, lang)


@router.get("/guide/{hero_id}/lane", summary="Guide hero lane")
def guide_lane(
    hero_id: Annotated[int, Path(ge=1, description=HERO_ID_DESCRIPTION)],
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": 20,
        "pageIndex": 1,
        "filters": [{"field": "hero_id", "operator": "eq", "value": hero_id}],
        "sorts": [],
        "fields": ["hero_id", "hero.data.roadsort"],
        "object": [],
    }
    return fetch_academy_post("2766683", payload, lang)


@router.get("/guide/{hero_id}/time-win-rate/{lane_id}", summary="Guide lane time win-rate")
def guide_time_win_rate(
    hero_id: Annotated[int, Path(ge=1, description=HERO_ID_DESCRIPTION)],
    lane_id: Annotated[int, Path(ge=1, le=5, description="Lane ID. Allowed values: 1 (exp), 2 (mid), 3 (roam), 4 (jungle), 5 (gold).")],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(description=RANK_DESCRIPTION),
    ] = "all",
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": 20,
        "pageIndex": 1,
        "filters": [
            {"field": "heroid", "operator": "eq", "value": hero_id},
            {"field": "big_rank", "operator": "eq", "value": _rank_value(rank)},
            {"field": "real_road", "operator": "eq", "value": lane_id},
        ],
        "sorts": [],
    }
    return fetch_academy_post("2777027", payload, lang)


@router.get("/guide/{hero_id}/builds", summary="Guide recommended builds")
def guide_builds(
    hero_id: Annotated[int, Path(ge=1, description=HERO_ID_DESCRIPTION)],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(description=RANK_DESCRIPTION),
    ] = "all",
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": 20,
        "pageIndex": 1,
        "filters": [
            {"field": "heroid", "operator": "eq", "value": hero_id},
            {"field": "real_road", "operator": "eq", "value": "2"},
            {"field": "big_rank", "operator": "eq", "value": _rank_value(rank)},
        ],
        "sorts": [],
    }
    return fetch_academy_post("2776688", payload, lang)


@router.get("/guide/{hero_id}/counters", summary="Guide counters")
def guide_counters(
    hero_id: Annotated[int, Path(ge=1, description=HERO_ID_DESCRIPTION)],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(description=RANK_DESCRIPTION),
    ] = "all",
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": 200,
        "pageIndex": 1,
        "filters": [
            {"field": "main_heroid", "operator": "eq", "value": hero_id},
            {"field": "camp_type", "operator": "eq", "value": 0},
            {"field": "big_rank", "operator": "eq", "value": _rank_value(rank)},
        ],
        "sorts": [],
    }
    return fetch_academy_post("2777391", payload, lang)


@router.get("/guide/{hero_id}/teammates", summary="Guide teammates")
def guide_teammates(
    hero_id: Annotated[int, Path(ge=1, description=HERO_ID_DESCRIPTION)],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(description=RANK_DESCRIPTION),
    ] = "all",
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": 200,
        "pageIndex": 1,
        "filters": [
            {"field": "main_heroid", "operator": "eq", "value": hero_id},
            {"field": "camp_type", "operator": "eq", "value": "1"},
            {"field": "big_rank", "operator": "eq", "value": _rank_value(rank)},
        ],
        "sorts": [],
    }
    return fetch_academy_post("2777391", payload, lang)


@router.get("/guide/{hero_id}/trends", summary="Guide win-rate trends")
def guide_trends(
    hero_id: Annotated[int, Path(ge=1, description=HERO_ID_DESCRIPTION)],
    days: Annotated[
        Literal["7", "15", "30"],
        Query(description="Trend window in days. Allowed: 7, 15, 30."),
    ] = "7",
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(description=RANK_DESCRIPTION),
    ] = "all",
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    day_map = {"7": "2755185", "15": "2755186", "30": "2755187"}
    payload = {
        "pageSize": 20,
        "pageIndex": 1,
        "filters": [
            {"field": "main_heroid", "operator": "eq", "value": hero_id},
            {"field": "bigrank", "operator": "eq", "value": _rank_value(rank)},
            {"field": "match_type", "operator": "eq", "value": 1},
        ],
        "sorts": [],
    }
    return fetch_academy_post(day_map.get(days, "2755185"), payload, lang)


@router.get("/guide/{hero_id}/recommended", summary="Guide recommended content")
def guide_recommended(
    hero_id: Annotated[int, Path(ge=1, description=HERO_ID_DESCRIPTION)],
    page: Annotated[int, Query(ge=1, description="Page index (1-based).")] = 1,
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": 20,
        "pageIndex": page,
        "filters": [
            {"field": "formId", "operator": "eq", "value": 2737553},
            {"field": "data.state", "operator": "eq", "value": "release"},
            {"field": "data.data.hero.hero_id", "operator": "eq", "value": hero_id},
            {"field": "data.data.language", "operator": "eq", "value": lang},
        ],
        "sorts": [
            {"data": {"field": "data.sort", "order": "desc"}, "type": "sequence"},
            {"data": {"field": "createdAt", "order": "desc"}, "type": "sequence"},
        ],
        "type": "form.item.all",
        "object": [2675413],
    }
    return fetch_academy_post("2718124", payload, lang)


@router.get("/hero-ratings", summary="Hero ratings list")
def hero_ratings(lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en") -> object:
    return fetch_ratings_all(lang)


@router.get("/hero-ratings/{subject}", summary="Hero ratings by subject")
def hero_ratings_subject(
    subject: Annotated[str, Path(min_length=1, description="Rating subject key from the ratings index response.")],
    lang: Annotated[str, Query(description=LANGUAGE_DESCRIPTION)] = "en",
) -> object:
    return fetch_ratings_subject(lang, subject)
