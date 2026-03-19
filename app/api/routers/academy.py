from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import require_api_available
from app.services.academy import fetch_academy_post, fetch_ratings_all, fetch_ratings_subject

router = APIRouter(prefix="/api/academy", tags=["academy"], dependencies=[Depends(require_api_available)])


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


@router.get("/version/")
def version(lang: str = Query(default="en")) -> object:
    payload = {
        "pageSize": 20,
        "pageIndex": 1,
        "filters": [{"field": "formId", "operator": "eq", "value": 2777742}],
        "sorts": [{"data": {"field": "createdAt", "order": "desc"}, "type": "sequence"}],
        "type": "form.item.all",
        "object": [2675413],
    }
    return fetch_academy_post("2718124", payload, lang)


@router.get("/heroes/")
def heroes(lang: str = Query(default="en")) -> object:
    payload = {
        "pageSize": 200,
        "pageIndex": 1,
        "filters": [],
        "sorts": [],
        "fields": ["head", "head_big", "hero.data.name", "hero.data.roadsort", "hero_id", "painting"],
        "object": [2667538],
    }
    return fetch_academy_post("2766683", payload, lang)


@router.get("/roles/")
def roles(lang: str = Query(default="en")) -> object:
    payload = {
        "pageSize": 50,
        "pageIndex": 1,
        "filters": [],
        "sorts": [{"data": {"field": "emblem_id", "order": "asc"}, "type": "sequence"}],
        "object": [],
    }
    return fetch_academy_post("2740642", payload, lang)


@router.get("/equipment/")
def equipment(lang: str = Query(default="en")) -> object:
    payload = {"pageSize": 200, "pageIndex": 1, "filters": [], "sorts": []}
    return fetch_academy_post("2775075", payload, lang)


@router.get("/equipment-details/")
def equipment_details(lang: str = Query(default="en")) -> object:
    payload = {"pageSize": 200, "pageIndex": 1, "filters": [], "sorts": []}
    return fetch_academy_post("2713995", payload, lang)


@router.get("/spells/")
def spells(lang: str = Query(default="en")) -> object:
    payload = {"pageSize": 200, "pageIndex": 1, "filters": [], "sorts": []}
    return fetch_academy_post("2718122", payload, lang)


@router.get("/emblems/")
def emblems(lang: str = Query(default="en")) -> object:
    payload = {"pageSize": 50, "pageIndex": 1, "filters": [], "sorts": []}
    return fetch_academy_post("2718121", payload, lang)


@router.get("/recommended/")
def recommended(page: int = Query(default=1), lang: str = Query(default="en")) -> object:
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


@router.get("/recommended/{recommended_id}/")
def recommended_detail(recommended_id: int, lang: str = Query(default="en")) -> object:
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


@router.get("/guide/")
def guide(
    size: int = Query(default=2000),
    page: int = Query(default=1),
    role: str | None = Query(default=None),
    lane: str | None = Query(default=None),
    lang: str = Query(default="en"),
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


@router.get("/guide/{hero_id}/stats/")
def guide_stats(hero_id: int, rank: str = Query(default="all"), lang: str = Query(default="en")) -> object:
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


@router.get("/guide/{hero_id}/lane/")
def guide_lane(hero_id: int, lang: str = Query(default="en")) -> object:
    payload = {
        "pageSize": 20,
        "pageIndex": 1,
        "filters": [{"field": "hero_id", "operator": "eq", "value": hero_id}],
        "sorts": [],
        "fields": ["hero_id", "hero.data.roadsort"],
        "object": [],
    }
    return fetch_academy_post("2766683", payload, lang)


@router.get("/guide/{hero_id}/time-win-rate/{lane_id}/")
def guide_time_win_rate(
    hero_id: int,
    lane_id: int,
    rank: str = Query(default="all"),
    lang: str = Query(default="en"),
) -> object:
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


@router.get("/guide/{hero_id}/builds/")
def guide_builds(hero_id: int, rank: str = Query(default="all"), lang: str = Query(default="en")) -> object:
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


@router.get("/guide/{hero_id}/counters/")
def guide_counters(hero_id: int, rank: str = Query(default="all"), lang: str = Query(default="en")) -> object:
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


@router.get("/guide/{hero_id}/teammates/")
def guide_teammates(hero_id: int, rank: str = Query(default="all"), lang: str = Query(default="en")) -> object:
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


@router.get("/guide/{hero_id}/trends/")
def guide_trends(
    hero_id: int,
    days: str = Query(default="7"),
    rank: str = Query(default="all"),
    lang: str = Query(default="en"),
) -> object:
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


@router.get("/guide/{hero_id}/recommended/")
def guide_recommended(hero_id: int, page: int = Query(default=1), lang: str = Query(default="en")) -> object:
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


@router.get("/hero-ratings/")
def hero_ratings(lang: str = Query(default="en")) -> object:
    return fetch_ratings_all(lang)


@router.get("/hero-ratings/{subject}/")
def hero_ratings_subject(subject: str, lang: str = Query(default="en")) -> object:
    return fetch_ratings_subject(lang, subject)
