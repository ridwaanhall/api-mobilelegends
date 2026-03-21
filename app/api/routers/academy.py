from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query

from app.api.dependencies import require_api_available
from app.core.filters import (
    ROLE_MAP, LANE_MAP, validate_and_map_multi, validate_and_map_rank
)
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

SIZE_DESCRIPTION = "Number of items per page."

INDEX_DESCRIPTION = "Page index (starting from 1)."


@router.get(
    path="/version",
    summary="Game Version Info",
    description="Get a list of game versions with release dates.",
)
def version(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    order: Annotated[
        Literal["asc", "desc"],
        Query(
            title="Sort Order",
            description="Sort order for release dates.",
        )
    ] = "desc",
    lang: Annotated[
        str, Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en"
) -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "formId",
                "operator": "eq",
                "value": 2777742
            }
        ],
        "sorts": [
            {
                "data":
                    {
                        "field": "createdAt",
                        "order": order
                    }
                ,
                "type": "sequence"
            }
        ],
        "type": "form.item.all",
        "object": [2675413],
    }
    return fetch_academy_post("2718124", payload, lang)


@router.get(
    path="/heroes",
    summary="Hero Catalog",
    description="Get a list of all heroes with basic information.",
)
def heroes(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en"
) -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [],
        "sorts": [],
        "fields": ["head", "head_big", "hero.data.name", "hero.data.roadsort", "hero_id", "painting"],
        "object": [2667538],
    }
    return fetch_academy_post("2766683", payload, lang)


@router.get(
    path="/roles",
    summary="Hero Roles",
    description="Get a list of hero roles (tank, fighter, assassin, mage, marksman, support).",
)
def roles(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    order: Annotated[
        Literal["asc", "desc"],
        Query(
            title="Sort Order",
            description="Sort order for role IDs.",
        )
    ] = "asc",
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en") -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [],
        "sorts": [
            {
                "data":
                    {
                        "field": "emblem_id",
                        "order": order
                    }
                ,
                "type": "sequence"
            }
        ],
        "object": [],
    }
    return fetch_academy_post("2740642", payload, lang)


@router.get(
    path="/equipment",
    summary="Equipment (Items)",
    description="Get a list of all equipment (items) with details.",
)
def equipment(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en"
) -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [],
        "sorts": []
    }
    return fetch_academy_post("2775075", payload, lang)


@router.get(
    path="/equipment-details",
    summary="Equipment Details",
    description="Get detailed information about a specific piece of equipment.",
)
def equipment_details(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en"
) -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [],
        "sorts": []
    }
    return fetch_academy_post("2713995", payload, lang)


@router.get(
    path="/spells",
    summary="Battle Spells",
    description="Get a list of all battle spells with details.",
)
def spells(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en"
) -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [],
        "sorts": []
    }
    return fetch_academy_post("2718122", payload, lang)


@router.get(
    path="/emblems",
    summary="Emblems",
    description="Get a list of all emblems with details.",
)
def emblems(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en"
) -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [],
        "sorts": []
    }
    return fetch_academy_post("2718121", payload, lang)


@router.get(
    path="/recommended",
    summary="Recommended Content",
    description="Get a list of recommended content.",
)
def recommended(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    order: Annotated[
        Literal["asc", "desc"],
        Query(
            title="Sort Order",
            description="Sort order for recommendation hotness and creation time.",
        ),
    ] = "desc",
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "formId",
                "operator": "eq",
                "value": 2737553
            },
            {
                "field": "data.state",
                "operator": "eq",
                "value": "release"
            },
            {
                "field": "data.channels",
                "operator": "in",
                "value": ["recommend"]
            },
            {
                "field": "uin",
                "operator": "contain",
                "value": "/.*/"
            },
            {
                "field": "data.data.game_version",
                "operator": "contain",
                "value": "/.*/"
            },
            {
                "field": "data.data.language",
                "operator": "eq",
                "value": lang
            },
            {
                "field": "createdAt",
                "operator": "gte",
                "value": 1
            },
        ],
        "sorts": [
            {
                "data":
                {
                    "field": "dynamic.hot",
                    "order": order
                },
                "type": "sequence"
            },
            {
                "data":
                {
                    "field": "createdAt",
                    "order": order
                },
                "type": "sequence"
            },
        ],
        "type": "form.item.all",
        "object": [2675413],
    }
    return fetch_academy_post("2718124", payload, lang)


@router.get(
    path="/recommended/{recommended_id}",
    summary="Recommended Content Detail",
    description="Get detailed information about a specific recommended content item.",
)
def recommended_detail(
    recommended_id: Annotated[
        int,
        Path(
            title="Recommended Post ID",
            description="Recommended post identifier.",
            ge=1
        )
    ],
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "formId",
                "operator": "eq",
                "value": 2737553
            },
            {
                "field": "id",
                "operator": "eq",
                "value": recommended_id
            },
            {
                "field": "data.state",
                "operator": "eq",
                "value": "release"
            },
        ],
        "sorts": [],
        "type": "form.item.all",
        "object": [2675413],
    }
    return fetch_academy_post("2718124", payload, lang)


@router.get(
    path="/guide",
    summary="Guide Hero (Similar to Hero Catalog with role/lane filters)",
    description="Get a list of heroes with filtering options for role and lane.",
)
def guide(
    role: Annotated[
        str,
        Query(
            title="Role",
            description="Role filter. Multi allowed: all, tank, fighter, assassin, mage, marksman, support. Example: tank,fighter"
        )
    ] = "tank,fighter,assassin,mage,marksman,support",
    lane: Annotated[
        str,
        Query(
            title="Lane",
            description="Lane filter. Multi allowed: all, exp, mid, roam, jungle, gold. Example: exp,mid"
        )
    ] = "exp,mid,roam,jungle,gold",
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    order: Annotated[
        Literal["asc", "desc"],
        Query(
            title="Sort Order",
            description="Sort order for hero IDs.",
        ),
    ] = "desc",
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    role_values = validate_and_map_multi(role, ROLE_MAP, ROLE_MAP["all"], "role")
    lane_values = validate_and_map_multi(lane, LANE_MAP, LANE_MAP["all"], "lane")
    
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field":"<hero.data.sortid>",
                "operator": "hasAnyOf",
                "value": role_values
            },
            {
                "field":"<hero.data.roadsort>",
                "operator": "hasAnyOf",
                "value": lane_values
            },
        ],
        "sorts": [
            {
                "data":
                    {
                        "field": "hero_id",
                        "order": order
                    },
                "type": "sequence"
            }
        ],
        "fields": ["head", "hero_id", "hero.data.name"],
        "object": [],
    }
    return fetch_academy_post("2766683", payload, lang)


@router.get(
    path="/guide/{hero_id}/stats",
    summary="Guide Hero Statistics (Win Rate, Pick Rate, Ban Rate, etc.)",
    description="Get statistics for a specific hero based on their performance in different ranks.",
)
def guide_stats(
    hero_id: Annotated[
        int,
        Path(
            title="Hero ID",
            description=HERO_ID_DESCRIPTION,
            ge=1,
        )
    ],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title="Rank",
            description=RANK_DESCRIPTION,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "main_heroid",
                "operator": "eq",
                "value": hero_id
            },
            {
                "field": "bigrank",
                "operator": "eq",
                "value": validate_and_map_rank(rank)
            },
            {
                "field": "match_type",
                "operator": "eq",
                "value": 1
            }
        ],
        "sorts": [],
    }
    return fetch_academy_post("2755183", payload, lang)


@router.get(
    path="/guide/{hero_id}/lane",
    summary="Guide Hero Lane Distribution",
    description="Get lane distribution information for a specific hero.",
)
def guide_lane(
    hero_id: Annotated[
        int,
        Path(
            title="Hero ID",
            description=HERO_ID_DESCRIPTION,
            ge=1,
        )
    ],
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "hero_id",
                "operator": "eq",
                "value": hero_id
            }
        ],
        "sorts": [],
        "fields": ["hero_id", "hero.data.roadsort"],
        "object": [],
    }
    return fetch_academy_post("2766683", payload, lang)


@router.get(
    path="/guide/{hero_id}/time-win-rate/{lane_id}",
    summary="Guide Hero Time-based Win Rate for Lane",
    description="Get time-based win rate information for a specific hero in a specific lane.",
)
def guide_time_win_rate(
    hero_id: Annotated[
        int,
        Path(
            title="Hero ID",
            description=HERO_ID_DESCRIPTION,
            ge=1,
        )
    ],
    lane: Annotated[
        str,
        Query(
            title="Lane",
            description="Lane filter. Multi allowed: all, exp, mid, roam, jungle, gold. Example: exp,mid"
        )
    ] = "exp,mid,roam,jungle,gold",
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title="Rank",
            description=RANK_DESCRIPTION
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "heroid",
                "operator": "eq",
                "value": hero_id
            },
            {
                "field": "big_rank",
                "operator": "eq",
                "value": validate_and_map_rank(rank)
            },
            {
                "field": "real_road",
                "operator": "eq",
                "value": lane
            },
        ],
        "sorts": [],
    }
    return fetch_academy_post("2777027", payload, lang)


@router.get(
    path="/guide/{hero_id}/builds",
    summary="Guide Hero Builds (Recommended Equipment) for Lane",
    description="Get recommended equipment builds for a specific hero in a specific lane.",
    deprecated=True,
)
def guide_builds(
    hero_id: Annotated[
        int,
        Path(
            title="Hero ID",
            description=HERO_ID_DESCRIPTION,
            ge=1,
        )
    ],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title="Rank",
            description=RANK_DESCRIPTION,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "heroid",
                "operator": "eq",
                "value": hero_id
            },
            {
                "field": "real_road",
                "operator": "eq",
                "value": "2"
            },
            {
                "field": "big_rank",
                "operator": "eq",
                "value": validate_and_map_rank(rank)
            }
        ],
        "sorts": [],
    }
    return fetch_academy_post("2776688", payload, lang)


@router.get(
    path="/guide/{hero_id}/counters",
    summary="Guide Hero Counters",
    description="Get counter information for a specific hero.",
)
def guide_counters(
    hero_id: Annotated[
        int,
        Path(
            title="Hero ID",
            description=HERO_ID_DESCRIPTION,
            ge=1,
        )
    ],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title="Rank",
            description=RANK_DESCRIPTION,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "main_heroid",
                "operator": "eq",
                "value": hero_id
            },
            {
                "field": "camp_type",
                "operator": "eq",
                "value": 0
            },
            {
                "field": "big_rank",
                "operator": "eq",
                "value": validate_and_map_rank(rank)
            }
        ],
        "sorts": [],
    }
    return fetch_academy_post("2777391", payload, lang)


@router.get(
    path="/guide/{hero_id}/teammates",
    summary="Guide Hero Teammates",
    description="Get teammate information for a specific hero.",
)
def guide_teammates(
    hero_id: Annotated[
        int,
        Path(
            title="Hero ID",
            description=HERO_ID_DESCRIPTION,
            ge=1,
        )
    ],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title="Rank",
            description=RANK_DESCRIPTION,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "main_heroid",
                "operator": "eq",
                "value": hero_id
            },
            {
                "field": "camp_type",
                "operator": "eq",
                "value": "1"
            },
            {
                "field": "big_rank",
                "operator": "eq",
                "value": validate_and_map_rank(rank)
            }
        ],
        "sorts": [],
    }
    return fetch_academy_post("2777391", payload, lang)


@router.get(
    path="/guide/{hero_id}/trends",
    summary="Guide Hero Trends (Recent Performance Changes)",
    description="Get trend information for a specific hero over a specified time window.",
)
def guide_trends(
    hero_id: Annotated[
        int,
        Path(
            title="Hero ID",
            description=HERO_ID_DESCRIPTION,
            ge=1,
        )
    ],
    days: Annotated[
        Literal["7", "15", "30"],
        Query(
            title="Trend Window (Days)",
            description="Trend window in days. Allowed: 7, 15, 30.",
        ),
    ] = "7",
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title="Rank",
            description=RANK_DESCRIPTION,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    day_map = {
        "7": "2755185",
        "15": "2755186",
        "30": "2755187"
    }
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "main_heroid",
                "operator": "eq",
                "value": hero_id
            },
            {
                "field": "bigrank",
                "operator": "eq",
                "value": validate_and_map_rank(rank)
            },
            {
                "field": "match_type",
                "operator": "eq",
                "value": 1
            }
        ],
        "sorts": [],
    }
    return fetch_academy_post(day_map.get(days, "2755185"), payload, lang)


@router.get(
    path="/guide/{hero_id}/recommended",
    summary="Guide Recommended Content",
    description="Get recommended content for a specific hero.",
)
def guide_recommended(
    hero_id: Annotated[
        int,
        Path(
            ge=1,
            description=HERO_ID_DESCRIPTION,
        )
    ],
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description=SIZE_DESCRIPTION,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description=INDEX_DESCRIPTION,
            ge=1,
        )
    ] = 1,
    order: Annotated[
        Literal["asc", "desc"],
        Query(
            title="Sort Order",
            description="Sort order for recommendation hotness and creation time.",
        ),
    ] = "desc",
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    validate_academy_hero_id(hero_id, lang)
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [
            {
                "field": "formId",
                "operator": "eq",
                "value": 2737553
            },
            {
                "field": "data.state",
                "operator": "eq",
                "value": "release"
            },
            {
                "field": "data.data.hero.hero_id",
                "operator": "eq",
                "value": hero_id
            },
            {
                "field": "data.data.language",
                "operator": "eq",
                "value": lang
            },
        ],
        "sorts": [
            {
                "data":
                    {
                        "field": "data.sort",
                        "order": order
                    },
                "type": "sequence"
            },
            {
                "data":
                    {
                        "field": "createdAt",
                        "order": order
                    },
                "type": "sequence"
            }
        ],
        "type": "form.item.all",
        "object": [2675413],
    }
    return fetch_academy_post("2718124", payload, lang)


@router.get(
    path="/hero-ratings",
    summary="Hero Ratings Index",
    description="Get a list of all hero ratings.",
)
def hero_ratings(
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en") -> object:
    return fetch_ratings_all(lang)


@router.get(
    path="/hero-ratings/{subject}",
    summary="Hero Ratings by Subject ID",
    description="Get hero ratings for a specific subject.",
)
def hero_ratings_subject(
    subject: Annotated[
        str,
        Path(
            description="Rating subject key from the ratings index response.",
            min_length=1,
        )
    ],
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en",
) -> object:
    return fetch_ratings_subject(lang, subject)
