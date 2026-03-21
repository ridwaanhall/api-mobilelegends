from __future__ import annotations

from typing import Annotated, Literal


from fastapi import APIRouter, Depends, Path, Query

from app.api.dependencies import require_api_available

from app.core.filters import (
    ROLE_MAP, LANE_MAP, validate_and_map_multi, validate_and_map_rank
)
from app.core.hero_limits import validate_academy_hero_id
from app.services.academy import fetch_academy_post, fetch_ratings_all, fetch_ratings_subject
from app.core.param_descriptions import *

router = APIRouter(prefix="/api/academy", tags=["academy"], dependencies=[Depends(require_api_available)])


@router.get(
    path="/version",
    summary=SUMMARY_ACADEMY_VERSION,
    description=DESCRIPTION_ACADEMY_VERSION,
)
def version(
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    order: Annotated[
        Literal["asc", "desc"],
        Query(
            title=TITLE_SORT_ORDER,
            description=DESCRIPTION_SORT_ORDER,
        )
    ] = "desc",
    lang: Annotated[
        str, Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_HEROES,
    description=DESCRIPTION_ACADEMY_HEROES,
)
def heroes(
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_ROLES,
    description=DESCRIPTION_ACADEMY_ROLES,
)
def roles(
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    order: Annotated[
        Literal["asc", "desc"],
        Query(
            title=TITLE_SORT_ORDER,
            description=DESCRIPTION_SORT_ORDER,
        )
    ] = "asc",
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = "en"
) -> object:
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
    summary=SUMMARY_ACADEMY_EQUIPMENT,
    description=DESCRIPTION_ACADEMY_EQUIPMENT,
)
def equipment(
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_EQUIPMENT_DETAILS,
    description=DESCRIPTION_ACADEMY_EQUIPMENT_DETAILS,
)
def equipment_details(
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_SPELLS,
    description=DESCRIPTION_ACADEMY_SPELLS,
)
def spells(
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_EMBLEMS,
    description=DESCRIPTION_ACADEMY_EMBLEMS,
)
def emblems(
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_RECOMMENDED,
    description=DESCRIPTION_ACADEMY_RECOMMENDED,
)
def recommended(
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    order: Annotated[
        Literal["asc", "desc"],
        Query(
            title=TITLE_SORT_ORDER,
            description=DESCRIPTION_SORT_ORDER,
        ),
    ] = "desc",
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_RECOMMENDED_DETAIL,
    description=DESCRIPTION_ACADEMY_RECOMMENDED_DETAIL,
)
def recommended_detail(
    recommended_id: Annotated[
        int,
        Path(
            title=TITLE_RECOMMENDED_POST_ID,
            description=DESCRIPTION_RECOMMENDED_POST_ID,
            ge=1
        )
    ],
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_GUIDE,
    description=DESCRIPTION_ACADEMY_GUIDE,
)
def guide(
    role: Annotated[
        str,
        Query(
            title=TITLE_ROLE,
            description=DESCRIPTION_ROLE,
        )
    ] = "tank,fighter,assassin,mage,marksman,support",
    lane: Annotated[
        str,
        Query(
            title=TITLE_LANE,
            description=DESCRIPTION_LANE,
        )
    ] = "exp,mid,roam,jungle,gold",
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    order: Annotated[
        Literal["asc", "desc"],
        Query(
            title=TITLE_SORT_ORDER,
            description=DESCRIPTION_SORT_ORDER,
        ),
    ] = "desc",
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_GUIDE_STATS,
    description=DESCRIPTION_ACADEMY_GUIDE_STATS,
)
def guide_stats(
    hero_id: Annotated[
        int,
        Path(
            title=TITLE_HERO_ID,
            description=DESCRIPTION_HERO_ID,
            ge=1,
        )
    ],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_GUIDE_LANE,
    description=DESCRIPTION_ACADEMY_GUIDE_LANE,
)
def guide_lane(
    hero_id: Annotated[
        int,
        Path(
            title=TITLE_HERO_ID,
            description=DESCRIPTION_HERO_ID,
            ge=1,
        )
    ],
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_GUIDE_TIME_WIN_RATE,
    description=DESCRIPTION_ACADEMY_GUIDE_TIME_WIN_RATE,
)
def guide_time_win_rate(
    hero_id: Annotated[
        int,
        Path(
            title=TITLE_HERO_ID,
            description=DESCRIPTION_HERO_ID,
            ge=1,
        )
    ],
    lane: Annotated[
        str,
        Query(
            title=TITLE_LANE,
            description=DESCRIPTION_LANE,
        )
    ] = "exp,mid,roam,jungle,gold",
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_GUIDE_BUILDS,
    description=DESCRIPTION_ACADEMY_GUIDE_BUILDS,
    deprecated=True,
)
def guide_builds(
    hero_id: Annotated[
        int,
        Path(
            title=TITLE_HERO_ID,
            description=DESCRIPTION_HERO_ID,
            ge=1,
        )
    ],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_GUIDE_COUNTERS,
    description=DESCRIPTION_ACADEMY_GUIDE_COUNTERS,
)
def guide_counters(
    hero_id: Annotated[
        int,
        Path(
            title=TITLE_HERO_ID,
            description=DESCRIPTION_HERO_ID,
            ge=1,
        )
    ],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_GUIDE_TEAMMATES,
    description=DESCRIPTION_ACADEMY_GUIDE_TEAMMATES,
)
def guide_teammates(
    hero_id: Annotated[
        int,
        Path(
            title=TITLE_HERO_ID,
            description=DESCRIPTION_HERO_ID,
            ge=1,
        )
    ],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_GUIDE_TRENDS,
    description=DESCRIPTION_ACADEMY_GUIDE_TRENDS,
)
def guide_trends(
    hero_id: Annotated[
        int,
        Path(
            title=TITLE_HERO_ID,
            description=DESCRIPTION_HERO_ID,
            ge=1,
        )
    ],
    days: Annotated[
        Literal["7", "15", "30"],
        Query(
            title=TITLE_TREND_WINDOW,
            description=DESCRIPTION_TREND_WINDOW,
        ),
    ] = "7",
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = "all",
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_GUIDE_RECOMMENDED,
    description=DESCRIPTION_ACADEMY_GUIDE_RECOMMENDED,
)
def guide_recommended(
    hero_id: Annotated[
        int,
        Path(
            ge=1,
            description=DESCRIPTION_HERO_ID,
        )
    ],
    size: Annotated[
        int,
        Query(
            title=TITLE_PAGE_SIZE,
            description=DESCRIPTION_PAGE_SIZE,
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title=TITLE_PAGE_INDEX,
            description=DESCRIPTION_PAGE_INDEX,
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
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
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
    summary=SUMMARY_ACADEMY_HERO_RATINGS,
    description=DESCRIPTION_ACADEMY_HERO_RATINGS,
)
def hero_ratings(
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = "en") -> object:
    return fetch_ratings_all(lang)


@router.get(
    path="/hero-ratings/{subject}",
    summary=SUMMARY_ACADEMY_HERO_RATINGS_SUBJECT,
    description=DESCRIPTION_ACADEMY_HERO_RATINGS_SUBJECT,
)
def hero_ratings_subject(
    subject: Annotated[
        str,
        Path(
            title=TITLE_RATING_SUBJECT,
            description=DESCRIPTION_RATING_SUBJECT,
            min_length=1,
        )
    ],
    lang: Annotated[
        str,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = "en",
) -> object:
    return fetch_ratings_subject(lang, subject)
