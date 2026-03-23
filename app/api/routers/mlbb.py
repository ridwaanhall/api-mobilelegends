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
    summary="List Heroes",
    description=(
        "Retrieve a paginated list of all heroes with basic information. "
        "Supports query parameters for pagination (`size`, `index`), sorting (`order`), "
        "and localization (`lang`). The response includes hero identifiers, names, "
        "images (head and smallmap), and relation data (assist, strong, weak) "
        "to other heroes. Useful for displaying hero collections, browsing, "
        "and analyzing hero relationships."
    ),
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
    summary="Hero Rank Statistics",
    description=(
        "Fetch rank statistics for heroes over a specified time window. "
        "Supports query parameters for filtering by past days (`days`), rank tier (`rank`), "
        "sorting (`sort_field`, `sort_order`), pagination (`size`, `index`), and localization (`lang`). "
        "The response includes hero identifiers, names, images, and statistical metrics such as "
        "appearance rate, ban rate, and win rate. It also provides related sub-heroes with their "
        "impact on win rate. Useful for analyzing hero performance trends across different ranks "
        "and time periods."
    ),
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
    summary="Hero Position Filters",
    description=(
        "Filter heroes by their position on the map using role and lane criteria. "
        "Supports multiple query parameters for roles (`tank`, `fighter`, `assassin`, "
        "`mage`, `marksman`, `support`) and lanes (`exp`, `mid`, `roam`, `jungle`, `gold`). "
        "Additional parameters include pagination (`size`, `index`), sorting (`order`), "
        "and localization (`lang`). The response provides hero identifiers, names, images, "
        "and detailed position metadata (`roadsort`, `sortid`) along with relation data "
        "(assist, strong, weak). Useful for building filtered hero lists and analyzing "
        "hero roles and lane assignments."
    ),
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
    summary="Hero Detail",
    description=(
        "Get detailed information for a specific hero by ID or name. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes hero metadata (name, images, speciality, story), "
        "skills with descriptions and tags, lane and role assignments, and relation data "
        "(assist, strong, weak) with other heroes. Useful for displaying comprehensive hero profiles, "
        "analyzing abilities, and understanding hero synergies and counters."
    ),
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
    summary="Hero Detail Statistics",
    description=(
        "Get detailed statistics for a specific hero by ID or name. "
        "Supports query parameters for rank tier (`rank`), pagination (`size`, `index`), "
        "and localization (`lang`). The response includes hero metadata (name, image, ID), "
        "and statistical metrics such as appearance rate, ban rate, and win rate. "
        "It also provides detailed breakdowns of sub-heroes with their win rate contributions "
        "across different match durations, as well as negative synergy data (`sub_hero_last`). "
        "Useful for analyzing hero performance trends, synergy with other heroes, and counters "
        "across different ranks and time intervals."
    ),
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
    path="/hero-skill-combo/{hero_identifier}",
    summary="Hero Skill Combo",
    description=(
        "Get the most effective skill combos for a specific hero by ID or name. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes hero ID, combo title, descriptive instructions on how to execute "
        "the combo (e.g., laning phase or teamfight scenarios), and associated skill icons/IDs "
        "in the recommended sequence. Useful for guiding players on optimal skill usage patterns "
        "to maximize hero performance in different situations."
    ),
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
    summary="Hero Rate Trends",
    description=(
        "Get rate trends for a specific hero by ID or name over a specified time window. "
        "Supports query parameters for rank tier (`rank`), past days window (`past-days`), "
        "pagination (`size`, `index`), and localization (`lang`). The response includes "
        "daily statistics such as appearance rate, ban rate, and win rate, each tied to "
        "a specific date. Useful for tracking hero performance trends, popularity, and "
        "ban frequency across different ranks and time periods."
    ),
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
    summary="Hero Relations",
    description=(
        "Get information about the relations of a specific hero by ID or name. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes hero identifiers, names, and categorized relation data: "
        "`assist` (heroes that synergize well), `strong` (heroes that are countered), "
        "and `weak` (heroes that counter the selected hero). Useful for understanding "
        "hero synergies, strengths, and weaknesses when building team compositions."
    ),
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
    summary="Hero Counters",
    description=(
        "Get information about heroes that counter a specific hero by ID or name. "
        "Supports query parameters for rank tier (`rank`), pagination (`size`, `index`), "
        "and localization (`lang`). The response includes the main hero's metadata "
        "(name, image, ID, appearance rate, ban rate, win rate) and lists counter heroes "
        "with detailed statistics such as win rate, appearance rate, and synergy impact "
        "(`increase_win_rate`). It also provides breakdowns of performance across different "
        "match durations and negative synergy data (`sub_hero_last`). Useful for analyzing "
        "which heroes are effective against the selected hero and understanding matchup dynamics."
    ),
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
    summary="Hero Compatibility",
    description=(
        "Get compatibility information for a specific hero by ID or name. "
        "Supports query parameters for rank tier (`rank`), pagination (`size`, `index`), "
        "and localization (`lang`). The response includes the main hero's metadata "
        "(name, image, ID, appearance rate, ban rate, win rate) and lists compatible heroes "
        "with detailed statistics such as win rate, appearance rate, and synergy impact "
        "(`increase_win_rate`). It also provides breakdowns of performance across different "
        "match durations and negative synergy data (`sub_hero_last`). Useful for analyzing "
        "which heroes pair well with the selected hero and which combinations reduce effectiveness."
    ),
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
