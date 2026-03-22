from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query

from app.api.dependencies import require_api_available

from app.services.mlbb import fetch_mlbb_post

from app.core.enums import LanguageEnum, RankEnum, SortOrderEnum, HeroRoleEnum, HeroLaneEnum
from app.core.errors import _hero_id_or_404
from app.core.filters import (
    ROLE_MAP, LANE_MAP, validate_and_map_multi, validate_and_map_rank
)
from app.core.param_descriptions import *

router = APIRouter(prefix="/api", tags=["mlbb"], dependencies=[Depends(require_api_available)])


@router.get(
    path="/hero-list",
    summary=SUMMARY_HERO_LIST,
    description=DESCRIPTION_HERO_LIST,
)
def hero_list(
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
        SortOrderEnum,
        Query(
            title=TITLE_SORT_ORDER,
            description=DESCRIPTION_SORT_ORDER,
        )
    ] = SortOrderEnum.DESCENDING,
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    payload = {
        "pageSize": size,
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
        "pageIndex": index,
        "fields": [
            "hero_id",
            "hero.data.head",
            "hero.data.name",
            "hero.data.smallmap"
        ],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get(
    path="/hero-rank",
    summary=SUMMARY_HERO_RANK_STATS,
    description=DESCRIPTION_HERO_RANK_STATS,
)
def hero_rank(
    days: Annotated[
        Literal["1", "3", "7", "15", "30"],
        Query(
            title=TITLE_PAST_DAYS,
            description=DESCRIPTION_PAST_DAYS,
        )
    ] = "1",
    rank: Annotated[
        RankEnum,
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = RankEnum.ALL,
    sort_field: Annotated[
        Literal["pick_rate", "ban_rate", "win_rate"],
        Query(
            title=TITLE_SORT_FIELD,
            description=DESCRIPTION_SORT_FIELD,
        )
    ] = "win_rate",
    sort_order: Annotated[
        SortOrderEnum,
        Query(
            title=TITLE_SORT_ORDER,
            description=DESCRIPTION_SORT_ORDER,
        )
    ] = SortOrderEnum.DESCENDING,
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    def create_rank_payload(rank_value: str) -> dict[str, object]:
        return {
            "pageSize": 20,
            "filters": [
                {
                    "field": "bigrank",
                    "operator": "eq",
                    "value": rank_value
                },
                {
                    "field": "match_type",
                    "operator": "eq",
                    "value": "0"
                },
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

    payload = create_rank_payload(validate_and_map_rank(rank))
    payload["pageSize"] = size
    payload["pageIndex"] = index
    payload["sorts"] = [
        {
            "data":
                {
                    "field": sort_field_map.get(sort_field, "main_hero_win_rate"),
                    "order": sort_order
                },
            "type": "sequence"
        }
    ]

    return fetch_mlbb_post(url_map.get(days, "2756567"), payload, lang)


@router.get(
    path="/hero-position",
    summary=SUMMARY_HERO_POSITION,
    description=DESCRIPTION_HERO_POSITION,
)
def hero_position(
    role: Annotated[
        list[str],
        Query(
            title=TITLE_ROLE,
            description=DESCRIPTION_ROLE,
        )
    ] = [
        HeroRoleEnum.TANK,
        HeroRoleEnum.FIGHTER,
        HeroRoleEnum.ASSASSIN,
        HeroRoleEnum.MAGE,
        HeroRoleEnum.MARKSMAN,
        HeroRoleEnum.SUPPORT,
    ],
    lane: Annotated[
        list[str],
        Query(
            title=TITLE_LANE,
            description=DESCRIPTION_LANE,
        )
    ] = [
        HeroLaneEnum.EXP,
        HeroLaneEnum.MID,
        HeroLaneEnum.ROAM,
        HeroLaneEnum.JUNGLE,
        HeroLaneEnum.GOLD,
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
        SortOrderEnum,
        Query(
            title=TITLE_SORT_ORDER,
            description=DESCRIPTION_SORT_ORDER,
        )
    ] = SortOrderEnum.DESCENDING,
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    role_values = validate_and_map_multi(role, ROLE_MAP, [1,2,3,4,5,6], "role")
    lane_values = validate_and_map_multi(lane, LANE_MAP, [1,2,3,4,5], "lane")

    payload = {
        "pageSize": size,
        "filters": [
            {
                "field": "<hero.data.sortid>",
                "operator": "hasAnyOf",
                "value": role_values
            },
            {
                "field": "<hero.data.roadsort>",
                "operator": "hasAnyOf", 
                "value": lane_values
            },
        ],
        "sorts": [
            {
                "data": {
                    "field": "hero_id",
                    "order": order
                },
                "type": "sequence"
            }
        ],
        "pageIndex": index,
        "fields": ["id", "hero_id", "hero.data.name", "hero.data.smallmap", "hero.data.sortid", "hero.data.roadsort"],
        "object": [],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get(
    path="/hero-detail/{hero_identifier}",
    summary=SUMMARY_HERO_DETAIL,
    description=DESCRIPTION_HERO_DETAIL,
)
def hero_detail(
    hero_identifier: Annotated[
        str,
        Path(
            title=TITLE_HERO_IDENTIFIER,
            description=DESCRIPTION_HERO_IDENTIFIER,
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": size,
        "filters": [
            {
                "field": "hero_id",
                "operator": "eq",
                "value": hero_id
            }
        ],
        "sorts": [],
        "pageIndex": index,
        "object": [],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get(
    path="/hero-detail-stats/{hero_identifier}",
    summary=SUMMARY_HERO_DETAIL_STATS,
    description=DESCRIPTION_HERO_DETAIL_STATS,
)
def hero_detail_stats(
    hero_identifier: Annotated[
        str,
        Path(
            title=TITLE_HERO_IDENTIFIER,
            description=DESCRIPTION_HERO_IDENTIFIER,
        )
    ],
    rank: Annotated[
        RankEnum,
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = RankEnum.ALL,
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": size,
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
                "value": "1"
            },
        ],
        "sorts": [],
        "pageIndex": index,
    }
    return fetch_mlbb_post("2756567", payload, lang)


@router.get(
    "/hero-skill-combo/{hero_identifier}",
    summary=SUMMARY_HERO_SKILL_COMBO,
    description=DESCRIPTION_HERO_SKILL_COMBO,
)
def hero_skill_combo(
    hero_identifier: Annotated[
        str,
        Path(
            title=TITLE_HERO_IDENTIFIER,
            description=DESCRIPTION_HERO_IDENTIFIER,
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": size,
        "filters": [
            {
                "field": "hero_id",
                "operator": "eq",
                "value": hero_id
            }
        ],
        "sorts": [],
        "pageIndex": index,
        "object": [2684183],
    }
    return fetch_mlbb_post("2674711", payload, lang)


@router.get(
    path="/hero-rate/{hero_identifier}",
    summary=SUMMARY_HERO_RATE,
    description=DESCRIPTION_HERO_RATE,
)
def hero_rate(
    hero_identifier: Annotated[
        str,
        Path(
            title=TITLE_HERO_IDENTIFIER,
            description=DESCRIPTION_HERO_IDENTIFIER,
        )
    ],
    rank: Annotated[
        RankEnum,
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = RankEnum.ALL,
    past_days: Annotated[
        Literal["7", "15", "30"],
        Query(
            alias="past-days",
            title=TITLE_RATE_WINDOW,
            description=DESCRIPTION_RATE_WINDOW,
        ),
    ] = "7",
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    url_map = {
        "7": "2674709",
        "15": "2687909",
        "30": "2690860"
    }
    payload = {
        "pageSize": size,
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
                "value": "1"
            },
        ],
        "sorts": [],
        "pageIndex": index,
    }
    return fetch_mlbb_post(url_map.get(past_days, "2674709"), payload, lang)


@router.get(
    path="/hero-relation/{hero_identifier}",
    summary=SUMMARY_HERO_RELATION,
    description=DESCRIPTION_HERO_RELATION,
)
def hero_relation(
    hero_identifier: Annotated[
        str,
        Path(
            title=TITLE_HERO_IDENTIFIER,
            description=DESCRIPTION_HERO_IDENTIFIER,
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": size,
        "filters": [
            {
                "field": "hero_id",
                "operator": "eq",
                "value": hero_id
            }
        ],
        "sorts": [],
        "pageIndex": index,
        "fields": ["hero.data.name"],
        "object": [],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get(
    path="/hero-counter/{hero_identifier}",
    summary=SUMMARY_HERO_COUNTER,
    description=DESCRIPTION_HERO_COUNTER,
)
def hero_counter(
    hero_identifier: Annotated[
        str,
        Path(
            title=TITLE_HERO_IDENTIFIER,
            description=DESCRIPTION_HERO_IDENTIFIER,
        )
    ],
    rank: Annotated[
        RankEnum,
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = RankEnum.ALL,
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": size,
        "filters": [
            {
                "field": "match_type",
                "operator": "eq",
                "value": "0"
            },
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
        ],
        "sorts": [],
        "pageIndex": index,
    }
    return fetch_mlbb_post("2756569", payload, lang)


@router.get(
    path="/hero-compatibility/{hero_identifier}",
    summary=SUMMARY_HERO_COMPATIBILITY,
    description=DESCRIPTION_HERO_COMPATIBILITY,
)
def hero_compatibility(
    hero_identifier: Annotated[
        str,
        Path(
            title=TITLE_HERO_IDENTIFIER,
            description=DESCRIPTION_HERO_IDENTIFIER,
        )
    ],
    rank: Annotated[
        RankEnum,
        Query(
            title=TITLE_RANK,
            description=DESCRIPTION_RANK,
        ),
    ] = RankEnum.ALL,
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": size,
        "filters": [
            {
                "field": "match_type",
                "operator": "eq",
                "value": "1"
            },
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
        ],
        "sorts": [],
        "pageIndex": index,
    }
    return fetch_mlbb_post("2756569", payload, lang)
