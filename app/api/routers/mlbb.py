from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query

from app.api.dependencies import require_api_available
from app.services.mlbb import fetch_mlbb_post

from app.core.errors import _hero_id_or_404
from app.core.filters import (
    ROLE_MAP, LANE_MAP, validate_and_map_multi, validate_and_map_rank
)

router = APIRouter(prefix="/api", tags=["mlbb"], dependencies=[Depends(require_api_available)])

LANGUAGE_DESCRIPTION = (
    "Language code for localized content. Supported codes: "
    "en, id, es, pt, ru, tr, ar, de, fr, it, ja, ko, th, vi, zh-CN, zh-TW."
)

HERO_IDENTIFIER_DESCRIPTION = (
    "Hero identifier as numeric hero ID (minimum: 1; maximum validated dynamically from current MLBB hero list) or hero name. "
    "Name matching ignores spaces/symbols and is case-insensitive (example: luoyi from Luo Yi)."
)

RANK_DESCRIPTION = "Rank filter. Allowed: all, epic, legend, mythic, honor, glory."

SIZE_DESCRIPTION = "Number of items per page."

INDEX_DESCRIPTION = "Page index (starting from 1)."


@router.get(
    path="/hero-list",
    summary="List Heroes",
    description="Get a list of all heroes with basic information.",
)
def hero_list(
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
            description="Sort order by hero ID for hero listing. Allowed: asc, desc.",
        )
    ] = "asc",
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
    description="Get rank statistics for heroes over a specified time window."
)
def hero_rank(
    days: Annotated[
        Literal["1", "3", "7", "15", "30"],
        Query(
            title="Past Days",
            description="Past day window. Allowed: 1, 3, 7, 15, 30.",
        )
    ] = "1",
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title="Rank",
            description=RANK_DESCRIPTION,
        ),
    ] = "all",
    sort_field: Annotated[
        Literal["pick_rate", "ban_rate", "win_rate"],
        Query(
            title="Sort Field",
            description="Sort field. Allowed: pick_rate, ban_rate, win_rate.",
        )
    ] = "win_rate",
    sort_order: Annotated[
        Literal["asc", "desc"],
        Query(
            title="Sort Order",
            description="Sort direction. Allowed: asc, desc.",
        )
    ] = "desc",
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
    payload["pageSize"] = int(size)
    payload["pageIndex"] = int(index)
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
    description="Filter heroes by their position on the map.",
)
def hero_position(
    role: Annotated[
        str,
        Query(
            title="Role",
            description="Role filter. Multi allowed: all, tank, fighter, assassin, mage, marksman, support. Example: tank,fighter",
        )
    ] = "tank,fighter,assassin,mage,marksman,support",
    lane: Annotated[
        str,
        Query(
            title="Lane",
            description="Lane filter. Multi allowed: all, exp, mid, roam, jungle, gold. Example: exp,mid",
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
            description="Sort direction. Allowed: asc, desc.",
        )
    ] = "desc",
    lang: Annotated[
        str,
        Query(
            title="Language",
            description=LANGUAGE_DESCRIPTION,
        )
    ] = "en"
) -> object:
    role_values = validate_and_map_multi(role, ROLE_MAP, ROLE_MAP["all"], "role")
    lane_values = validate_and_map_multi(lane, LANE_MAP, LANE_MAP["all"], "lane")

    payload = {
        "pageSize": int(size),
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
                "data":
                    {
                        "field": "hero_id",
                        "order": order
                    },
                "type": "sequence"
            }
        ],
        "pageIndex": int(index),
        "fields": ["id", "hero_id", "hero.data.name", "hero.data.smallmap", "hero.data.sortid", "hero.data.roadsort"],
        "object": [],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get(
    path="/hero-detail/{hero_identifier}",
    summary="Hero Detail",
    description="Get detailed information about a specific hero.",
)
def hero_detail(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=HERO_IDENTIFIER_DESCRIPTION,
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
    ] = "en"
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": int(size),
        "filters": [
            {
                "field": "hero_id",
                "operator": "eq",
                "value": hero_id
            }
        ],
        "sorts": [],
        "pageIndex": int(index),
        "object": [],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get(
    path="/hero-detail-stats/{hero_identifier}",
    summary="Hero Detail Statistics",
    description="Get detailed statistics for a specific hero.",
)
def hero_detail_stats(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=HERO_IDENTIFIER_DESCRIPTION,
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
    ] = "en"
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": int(size),
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
        "pageIndex": int(index),
    }
    return fetch_mlbb_post("2756567", payload, lang)


@router.get(
    "/hero-skill-combo/{hero_identifier}",
    summary="Hero Skill Combo",
    description="Get the skill combo information for a specific hero.",
)
def hero_skill_combo(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=HERO_IDENTIFIER_DESCRIPTION,
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
    ] = "en"
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": int(size),
        "filters": [
            {
                "field": "hero_id",
                "operator": "eq",
                "value": hero_id
            }
        ],
        "sorts": [],
        "pageIndex": int(index),
        "object": [2684183],
    }
    return fetch_mlbb_post("2674711", payload, lang)


@router.get(
    path="/hero-rate/{hero_identifier}",
    summary="Hero Rate Trends",
    description="Get rate trends for a specific hero over a specified time window.",
)
def hero_rate(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=HERO_IDENTIFIER_DESCRIPTION,
        )
    ],
    rank: Annotated[
        Literal["all", "epic", "legend", "mythic", "honor", "glory"],
        Query(
            title="Rank",
            description=RANK_DESCRIPTION,
        ),
    ] = "all",
    past_days: Annotated[
        Literal["7", "15", "30"],
        Query(
            alias="past-days",
            description="Rate window in days. Allowed: 7, 15, 30."
        ),
    ] = "7",
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
    hero_id = _hero_id_or_404(hero_identifier, lang)
    url_map = {
        "7": "2674709",
        "15": "2687909",
        "30": "2690860"
    }
    payload = {
        "pageSize": int(size),
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
        "pageIndex": int(index),
    }
    return fetch_mlbb_post(url_map.get(past_days, "2674709"), payload, lang)


@router.get(
    path="/hero-relation/{hero_identifier}",
    summary="Hero Relations",
    description="Get information about the relations of a specific hero.",
)
def hero_relation(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=HERO_IDENTIFIER_DESCRIPTION,
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
    ] = "en"
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": int(size),
        "filters": [
            {
                "field": "hero_id",
                "operator": "eq",
                "value": hero_id
            }
        ],
        "sorts": [],
        "pageIndex": int(index),
        "fields": ["hero.data.name"],
        "object": [],
    }
    return fetch_mlbb_post("2756564", payload, lang)


@router.get(
    path="/hero-counter/{hero_identifier}",
    summary="Hero Counters",
    description="Get information about heroes that counter a specific hero.",
)
def hero_counter(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=HERO_IDENTIFIER_DESCRIPTION,
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
    ] = "en"
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": int(size),
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
        "pageIndex": int(index),
    }
    return fetch_mlbb_post("2756569", payload, lang)


@router.get(
    path="/hero-compatibility/{hero_identifier}",
    summary="Hero Compatibility",
    description="Get compatibility information for a specific hero.",
)
def hero_compatibility(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=HERO_IDENTIFIER_DESCRIPTION,
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
    ] = "en"
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    payload = {
        "pageSize": int(size),
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
        "pageIndex": int(index),
    }
    return fetch_mlbb_post("2756569", payload, lang)
