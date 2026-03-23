from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query

from app.api.dependencies import require_api_available

from app.services.academy import fetch_academy_post, fetch_ratings_all, fetch_ratings_subject

from app.core.errors import _hero_id_or_404

from app.core.enums import LanguageEnum, RankEnum, SortOrderEnum, HeroRoleEnum, HeroLaneEnum
from app.core.filters import (
    ROLE_MAP, LANE_MAP, validate_and_map_multi, validate_and_map_rank
)
from app.core.hero_limits import validate_academy_hero_id
from app.core.param_descriptions import *

router = APIRouter(prefix="/api/academy", tags=["academy"], dependencies=[Depends(require_api_available)])


@router.get(
    path="/version",
    summary="Game Version Info",
    description=(
        "Fetch a list of game versions with their release dates. "
        "Supports query parameters for pagination (`size`, `index`), sorting (`order`), "
        "and localization (`lang`). The response includes version identifiers, timestamps, "
        "and metadata such as form IDs and update information. Useful for tracking "
        "game version history, release cycles, and ensuring compatibility with specific "
        "patches or updates."
    ),
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
    path="/heroes/old",
    summary="Hero Catalog",
    description=(
        "Retrieve a paginated list of all heroes with basic information. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes hero identifiers, names, images (`head`, `head_big`, `painting`), "
        "and lane/role assignments (`roadsort`). Useful for displaying hero collections, "
        "browsing available heroes, and analyzing their basic attributes."
    ),
    deprecated=True,
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
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
    summary="Roles",
    description=(
        "List all hero roles available in the game (Tank, Fighter, Assassin, Mage, Marksman, Support). "
        "Supports query parameters for pagination (`size`, `index`), sorting (`order`), "
        "and localization (`lang`). The response includes role identifiers, titles, icons, "
        "and emblem details such as attributes and bonuses. Useful for displaying role categories, "
        "explaining role-specific attributes, and guiding players in hero selection."
    ),
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
        SortOrderEnum,
        Query(
            title=TITLE_SORT_ORDER,
            description=DESCRIPTION_SORT_ORDER,
        )
    ] = SortOrderEnum.ASCENDING,
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
    description=(
        "List all equipment (items). "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes item identifiers, names, and icons (`equipid`, `equipname`, `equipicon`). "
        "Useful for displaying the full equipment catalog, browsing available items, "
        "and analyzing their basic attributes."
    ),
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
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
    description=(
        "Get detailed information about a specific equipment item. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes item identifiers, names, icons, type, and detailed attributes "
        "such as passive skills, tips, and descriptions (`equipskilldesc`, `equiptips`, `equiptypename`). "
        "Useful for displaying full item details, explaining effects, and guiding players "
        "in equipment selection and strategy."
    ),
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
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
    description=(
        "List all battle spells with details. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes spell identifiers, names, icons, short descriptions, and full skill descriptions "
        "(`skilldesc`, `skillshortdesc`). Useful for displaying the complete catalog of battle spells, "
        "explaining their effects, and guiding players in spell selection and strategy."
    ),
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
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
    description=(
        "List all emblems with details. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes emblem identifiers, names, icons, tiers, and associated skills "
        "(`emblemskill` with skill name, description, and icon). Useful for displaying the full emblem catalog, "
        "explaining emblem effects, and guiding players in emblem selection and optimization."
    ),
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [],
        "sorts": []
    }
    return fetch_academy_post("2718121", payload, lang)


@router.get(
    path="/rank",
    summary="Rank List",
    description=(
        "Retrieve all rank information for MLBB. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes rank identifiers, names, icons, and ranges (`rankid_start`, `rankid_end`) "
        "with corresponding tier labels (`bigrank_name`, `minrank_name`). Useful for displaying the full "
        "rank progression system, explaining rank tiers, and guiding players in understanding MLBB's ranking structure."
    ),
)
def rank(
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
    payload = {
        "pageSize": size,
        "pageIndex": index,
        "filters": [],
        "sorts": [],
        "object": []
    }
    return fetch_academy_post("3210596", payload, lang)


@router.get(
    path="/rank/{rank_id}",
    summary="Rank Details",
    description=(
        "Retrieve details for a specific rank in MLBB by rank ID. "
        "Supports query parameter for localization (`lang`). "
        "The response includes rank identifiers, names, icons, and ranges (`rankid_start`, `rankid_end`) "
        "with corresponding tier labels (`bigrank_name`, `minrank_name`). Useful for displaying detailed "
        "information about a single rank tier, explaining its position in the progression system, "
        "and guiding players in understanding MLBB's ranking structure."
    ),
)
def rank_details(
    rank_id: Annotated[
        int,
        Path(
            title="Rank ID",
            description="Rank ID. Maximum is validated dynamically from current rank list.",
            ge=1,
            le=9999
        )
    ],
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    payload = {
        "pageSize": 1,
        "pageIndex": 1,
        "filters": [
            {
                "field": "rankid_start",
                "operator": "lte",
                "value": rank_id
            },
            {
                "field": "rankid_end",
                "operator": "gte",
                "value": rank_id
            }
        ],
        "sorts": [],
        "object": []
    }
    return fetch_academy_post("3210596", payload, lang)

@router.get(
    path="/recommended",
    summary="Recommended Content",
    description=(
        "List recommended content for players. "
        "Supports query parameters for pagination (`size`, `index`), sorting (`order`), "
        "and localization (`lang`). The response includes guides and builds with metadata such as "
        "hero overview, strengths, weaknesses, recommended equipment, emblems, spells, and cooperative/counter heroes. "
        "It also provides user-generated content details (title, author, snapshot, votes, views) and contextual tips. "
        "Useful for surfacing community guides, personalized builds, and strategic recommendations for MLBB players."
    ),
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
    summary="Recommended Detail",
    description=(
        "Get details for a specific recommended content item by its identifier. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes hero overview, strengths, weaknesses, recommended equipment, emblems, spells, "
        "cooperative and counter heroes, as well as metadata such as title, snapshot, author, votes, and views. "
        "Useful for displaying full details of a single guide or build, explaining strategic recommendations, "
        "and surfacing community-generated content for MLBB players."
    ),
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
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
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
    path="/heroes",
    summary="Hero Filters",
    description=(
        "Retrieve a list of heroes with filtering options for role and lane. "
        "Supports query parameters for role (`tank`, `fighter`, `assassin`, `mage`, `marksman`, `support`) "
        "and lane (`exp`, `mid`, `roam`, `jungle`, `gold`), as well as pagination (`size`, `index`), "
        "sorting (`order`), and localization (`lang`). The response includes hero identifiers, names, "
        "and portrait images. Useful for filtering heroes by gameplay role or lane assignment, "
        "and displaying customized hero lists in MLBB Academy."
    ),
)
def guide(
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
    ] = SortOrderEnum.ASCENDING,
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    role_values = validate_and_map_multi(role, ROLE_MAP, [1, 2, 3, 4, 5, 6], "role")
    lane_values = validate_and_map_multi(lane, LANE_MAP, [1, 2, 3, 4, 5], "lane")
    
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
    path="/heroes/{hero_identifier}/stats",
    summary="Hero Statistics",
    description=(
        "Retrieve performance statistics for a specific hero by rank. "
        "Supports query parameters for rank (`all`, `epic`, `legend`, `mythic`, `honor`, `glory`), "
        "pagination (`size`, `index`), and localization (`lang`). "
        "The response includes hero identifiers, names, portraits, and statistical metrics such as "
        "appearance rate, ban rate, win rate, and synergy with other heroes (`sub_hero`, `sub_hero_last`). "
        "Useful for analyzing hero performance across different ranks, understanding meta trends, "
        "and guiding players in hero selection and strategy."
    ),
)
def guide_stats(
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
    path="/heroes/{hero_identifier}/lane",
    summary="Hero Lane Distribution",
    description=(
        "Retrieve lane distribution information for a specific hero. "
        "Supports query parameters for pagination (`size`, `index`) and localization (`lang`). "
        "The response includes hero identifiers, lane assignments, and lane metadata such as "
        "lane ID, title, and icon (`road_sort_id`, `road_sort_title`, `road_sort_icon`). "
        "Useful for analyzing hero lane preferences, understanding optimal lane assignments, "
        "and guiding players in hero positioning strategies."
    ),
)
def guide_lane(
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
    path="/heroes/{hero_identifier}/time-win-rate/{lane_id}",
    summary="Hero Lane Time-based Win Rate",
    description=(
        "Retrieve time-based win rate statistics for a specific hero in a given lane. "
        "Supports query parameters for rank (`all`, `epic`, `legend`, `mythic`, `honor`, `glory`), "
        "pagination (`size`, `index`), and localization (`lang`). "
        "The response includes hero identifiers, lane ID, overall win rate, and segmented win rates "
        "across different time intervals (`time_min`, `time_max`, `win_rate`). "
        "Useful for analyzing hero performance progression over match duration, "
        "understanding lane-specific strengths, and guiding players in timing strategies."
    ),
)
def guide_time_win_rate(
    hero_identifier: Annotated[
        str,
        Path(
            title=TITLE_HERO_IDENTIFIER,
            description=DESCRIPTION_HERO_IDENTIFIER,
        )
    ],
    lane_id: Annotated[
        int,
        Path(
            title="Lane ID",
            description="Lane ID. Allowed values: 1 (exp), 2 (mid), 3 (roam), 4 (jungle), 5 (gold).",
            ge=1,
            le=5,
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
                "value": lane_id
            },
        ],
        "sorts": [],
    }
    return fetch_academy_post("2777027", payload, lang)


@router.get(
    path="/heroes/{hero_identifier}/builds",
    summary="Hero Recommended Builds",
    description=(
        "Retrieve recommended equipment builds for a specific hero in a given lane. "
        "⚠️ Deprecated: This endpoint is maintained for backward compatibility but may be replaced in future versions. "
        "Supports query parameters for rank (`all`, `epic`, `legend`, `mythic`, `honor`, `glory`), "
        "pagination (`size`, `index`), and localization (`lang`). "
        "The response includes hero identifiers, names, lane assignment, and build details such as "
        "equipment IDs (`equipid`), emblem configuration (`emblem`), battle spell (`battleskill`), rune skills, "
        "and statistical metrics like build pick rate and win rate. "
        "Useful for displaying historical or community-recommended builds, but should be replaced with newer endpoints "
        "for up-to-date build recommendations."
    ),
    deprecated=True,
)
def guide_builds(
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
    path="/heroes/{hero_identifier}/counters",
    summary="Hero Counters",
    description=(
        "Retrieve counter information for a specific hero. "
        "Supports query parameters for rank (`all`, `epic`, `legend`, `mythic`, `honor`, `glory`), "
        "pagination (`size`, `index`), and localization (`lang`). "
        "The response includes hero identifiers, overall statistics such as ban rate, pick rate, and win rate, "
        "as well as a list of counter heroes (`sub_hero`) with their win rates and impact values (`increase_win_rate`). "
        "Useful for analyzing which heroes perform well against the target hero, understanding matchup dynamics, "
        "and guiding players in drafting strategies."
    ),
)
def guide_counters(
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
    path="/heroes/{hero_identifier}/teammates",
    summary="Hero Teammates",
    description=(
        "Retrieve teammate information for a specific hero. "
        "Supports query parameters for rank (`all`, `epic`, `legend`, `mythic`, `honor`, `glory`), "
        "pagination (`size`, `index`), and localization (`lang`). "
        "The response includes hero identifiers, overall statistics such as ban rate, pick rate, and win rate, "
        "as well as a list of teammate heroes (`sub_hero`) with their win rates and impact values (`increase_win_rate`). "
        "Useful for analyzing which heroes synergize well with the target hero, understanding team composition dynamics, "
        "and guiding players in drafting strategies."
    ),
)
def guide_teammates(
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
    path="/heroes/{hero_identifier}/trends",
    summary="Hero Performance Trends",
    description=(
        "Retrieve trend information for a specific hero over a selected time window. "
        "Supports query parameters for days (`7`, `15`, `30`), rank (`all`, `epic`, `legend`, `mythic`, `honor`, `glory`), "
        "pagination (`size`, `index`), and localization (`lang`). "
        "The response includes hero identifiers, rank context, and daily statistics such as "
        "appearance rate (`app_rate`), ban rate (`ban_rate`), and win rate (`win_rate`) over the specified period. "
        "Useful for tracking hero performance changes, identifying meta shifts, and guiding players in understanding "
        "how a hero’s effectiveness evolves across different ranks and timeframes."
    ),
)
def guide_trends(
    hero_identifier: Annotated[
        str,
        Path(
            title=TITLE_HERO_IDENTIFIER,
            description=DESCRIPTION_HERO_IDENTIFIER,
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
    path="/heroes/{hero_identifier}/recommended",
    summary="Hero Recommended Content",
    description=(
        "Retrieve recommended content for a specific hero. "
        "Supports query parameters for pagination (`size`, `index`), sorting (`order` by hotness or creation time), "
        "and localization (`lang`). "
        "The response includes hero identifiers, lane assignments, and community-generated content such as "
        "guides, builds, emblems, equipment, spells, and cooperative/counter strategies. "
        "Each record also contains metadata like title, snapshot image, author information, votes, views, and popularity metrics. "
        "Useful for surfacing curated or community-recommended hero guides, builds, and strategies to help players "
        "optimize gameplay and learn from shared experiences."
    ),
)
def guide_recommended(
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
    order: Annotated[
        SortOrderEnum,
        Query(
            title=TITLE_SORT_ORDER,
            description="Sort order for recommendation hotness and creation time.",
        ),
    ] = SortOrderEnum.DESCENDING,
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
    path="/heroes/ratings",
    summary="Hero Ratings Index",
    description=(
        "Retrieve a list of all hero ratings and community polls. "
        "Supports query parameter for localization (`lang`). "
        "The response includes rating subjects (poll topics), titles, descriptions, and aggregated statistics such as "
        "comment counts, ranking lists of heroes with their scores, total votes, vote counts, and highlighted comments. "
        "Each hero entry contains identifiers, images, score values, and optional hashtags or channels. "
        "Useful for displaying community-driven hero ratings, tracking popularity trends, and surfacing thematic polls "
        "such as 'Most Charismatic Hero' or 'Top Jungler'."
    ),
)
def hero_ratings(
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    return fetch_ratings_all(lang)


@router.get(
    path="/heroes/ratings/{subject}",
    summary="Hero Ratings by Subject",
    description=(
        "Retrieve hero ratings for a specific subject from the ratings index. "
        "Supports query parameter for localization (`lang`). "
        "The response includes hero entries with identifiers, names, images, and rating statistics such as "
        "score value, total score, vote count, and highlighted community comments. "
        "Useful for displaying detailed ratings within a chosen poll or theme (e.g., 'Top Jungler', 'Most Charismatic Hero'), "
        "allowing players to explore community sentiment and popularity for heroes in a specific category."
    ),
)
def hero_ratings_subject(
    subject: Annotated[
        str,
        Path(
            title=TITLE_RATING_SUBJECT,
            description=DESCRIPTION_RATING_SUBJECT,
            min_length=7,
            max_length=7,
        )
    ],
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    return fetch_ratings_subject(lang, subject)
