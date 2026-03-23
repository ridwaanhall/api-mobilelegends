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
        "Supports query parameters for pagination (`size`, `index`), sorting (`order`), and localization (`lang`).\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **order**: Sort order for results. Allowed values: `asc`, `desc`.\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero records:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **data**:\n"
        "        - **hero**:\n"
        "            - **data**:\n"
        "                - **head**: Hero head image URL.\n"
        "                - **name**: Hero name.\n"
        "                - **smallmap**: Hero smallmap image URL.\n"
        "        - **hero_id**: Unique hero identifier.\n"
        "        - **relation**:\n"
        "            - **assist**:\n"
        "                - **target_hero_id**: Array of hero IDs assisted.\n"
        "            - **strong**:\n"
        "                - **target_hero_id**: Array of hero IDs this hero is strong against.\n"
        "            - **weak**:\n"
        "                - **target_hero_id**: Array of hero IDs this hero is weak against.\n\n"
        "This endpoint is useful for:\n"
        "    - Displaying hero collections.\n"
        "    - Browsing hero details.\n"
        "    - Analyzing hero relationships (assist, strong, weak)."
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
        "Supports query parameters for filtering by past days, rank tier, sorting, pagination, and localization.\n\n"
        "Query parameters:\n"
        "- **days**: Past day window. Allowed values: `1`, `3`, `7`, `15`, `30`.\n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **sort_field**: Sort field. Allowed values: `pick_rate`, `ban_rate`, `win_rate`.\n"
        "- **sort_order**: Sort order for results. Allowed values: `asc`, `desc`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero rank statistics:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **data**:\n"
        "        - **main_hero**:\n"
        "            - **data**:\n"
        "                - **head**: Hero head image URL.\n"
        "                - **name**: Hero name.\n"
        "        - **main_heroid**: Unique hero identifier.\n"
        "        - **main_hero_channel**:\n"
        "            - **id**: Channel ID reference.\n"
        "        - **main_hero_appearance_rate**: Hero pick rate (appearance frequency).\n"
        "        - **main_hero_ban_rate**: Hero ban rate.\n"
        "        - **main_hero_win_rate**: Hero win rate.\n"
        "        - **sub_hero**: Array of related sub-heroes, each containing:\n"
        "            - **hero**:\n"
        "                - **data**:\n"
        "                    - **head**: Sub-hero head image URL.\n"
        "            - **heroid**: Sub-hero ID.\n"
        "            - **hero_channel**:\n"
        "                - **id**: Channel ID reference.\n"
        "            - **increase_win_rate**: Impact of sub-hero on win rate.\n\n"
        "This endpoint is useful for:\n"
        "    - Analyzing hero performance trends across different ranks.\n"
        "    - Tracking pick, ban, and win rates over time.\n"
        "    - Understanding synergies and counters via sub-hero relationships."
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
        "Supports multiple query parameters for roles and lanes, along with pagination, sorting, and localization.\n\n"
        "Query parameters:\n"
        "- **role**: Role filter (multi allowed). Values: `tank`, `fighter`, `assassin`, `mage`, `marksman`, `support`.\n"
        "    Example: `role=tank&role=fighter`\n"
        "- **lane**: Lane filter (multi allowed). Values: `exp`, `mid`, `roam`, `jungle`, `gold`.\n"
        "    Example: `lane=exp&lane=mid`\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **order**: Sort order for results. Allowed values: `asc`, `desc`.\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero position data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **data**:\n"
        "        - **hero**:\n"
        "            - **data**:\n"
        "                - **name**: Hero name.\n"
        "                - **smallmap**: Hero smallmap image URL.\n"
        "                - **roadsort**: Array of lane metadata objects:\n"
        "                    - **_id**: Unique identifier.\n"
        "                    - **caption**: Lane caption (localized).\n"
        "                    - **configId**: Configuration ID.\n"
        "                    - **createdAt**: Creation timestamp.\n"
        "                    - **createdUser**: Creator username.\n"
        "                    - **data**:\n"
        "                        - **_object**: Object reference ID.\n"
        "                        - **road_sort_icon**: Lane icon URL.\n"
        "                        - **road_sort_id**: Lane ID.\n"
        "                        - **road_sort_title**: Lane title (e.g., Roam).\n"
        "                    - **updatedAt**: Last update timestamp.\n"
        "                    - **updatedUser**: Last updater username.\n"
        "                - **sortid**: Array of role metadata objects:\n"
        "                    - **_id**: Unique identifier.\n"
        "                    - **caption**: Role caption (localized).\n"
        "                    - **configId**: Configuration ID.\n"
        "                    - **createdAt**: Creation timestamp.\n"
        "                    - **createdUser**: Creator username.\n"
        "                    - **data**:\n"
        "                        - **_object**: Object reference ID.\n"
        "                        - **sort_icon**: Role icon URL.\n"
        "                        - **sort_id**: Role ID.\n"
        "                        - **sort_title**: Role title (e.g., Support).\n"
        "                    - **updatedAt**: Last update timestamp.\n"
        "                    - **updatedUser**: Last updater username.\n"
        "        - **hero_id**: Unique hero identifier.\n"
        "        - **relation**:\n"
        "            - **assist**:\n"
        "                - **target_hero_id**: Array of hero IDs assisted.\n"
        "            - **strong**:\n"
        "                - **target_hero_id**: Array of hero IDs this hero is strong against.\n"
        "            - **weak**:\n"
        "                - **target_hero_id**: Array of hero IDs this hero is weak against.\n"
        "    - **id**: Record identifier.\n\n"
        "This endpoint is useful for:\n"
        "    - Building filtered hero lists.\n"
        "    - Analyzing hero roles and lane assignments.\n"
        "    - Understanding hero relationships (assist, strong, weak)."
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
        "Supports query parameters for pagination and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Luo Yi' → `luoyi`).\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero details:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **caption**: Caption or localized label.\n"
        "    - **configId**: Configuration ID.\n"
        "    - **createdAt**: Creation timestamp.\n"
        "    - **createdUser**: Creator username.\n"
        "    - **data**:\n"
        "        - **head**: Hero portrait image URL.\n"
        "        - **head_big**: Larger hero portrait image URL.\n"
        "        - **hero**:\n"
        "            - **data**:\n"
        "                - **heroid**: Hero ID.\n"
        "                - **name**: Hero name.\n"
        "                - **story**: Hero lore or background story.\n"
        "                - **painting**: Hero splash art image URL.\n"
        "                - **speciality**: Array of hero specialties (e.g., Support, Crowd Control).\n"
        "                - **abilityshow**: Array of ability stats.\n"
        "                - **difficulty**: Difficulty rating.\n"
        "                - **heroskilllist**: Array of skill sets, each containing:\n"
        "                    - **skilllist**: Array of skills:\n"
        "                        - **skillid**: Skill ID.\n"
        "                        - **skillname**: Skill name.\n"
        "                        - **skilldesc**: Skill description.\n"
        "                        - **skillicon**: Skill icon URL.\n"
        "                        - **skillcd&cost**: Cooldown and mana cost.\n"
        "                        - **skilltag**: Array of tags:\n"
        "                            - **tagid**: Tag ID.\n"
        "                            - **tagname**: Tag name (e.g., Burst, CC).\n"
        "                            - **tagrgb**: Tag color.\n"
        "                        - **skillvideo**: Skill video URL (if available).\n"
        "                - **roadsort**: Lane assignment metadata:\n"
        "                    - **road_sort_id**: Lane ID.\n"
        "                    - **road_sort_title**: Lane title (e.g., Mid Lane).\n"
        "                    - **road_sort_icon**: Lane icon URL.\n"
        "                - **sortid**: Role assignment metadata:\n"
        "                    - **sort_id**: Role ID.\n"
        "                    - **sort_title**: Role title (e.g., Mage).\n"
        "                    - **sort_icon**: Role icon URL.\n"
        "                - **smallmap**: Hero smallmap image URL.\n"
        "                - **squarehead**: Square portrait image URL.\n"
        "                - **squareheadbig**: Larger square portrait image URL.\n"
        "        - **hero_id**: Unique hero identifier.\n"
        "        - **relation**:\n"
        "            - **assist**:\n"
        "                - **desc**: Description of assist synergy.\n"
        "                - **target_hero_id**: Array of hero IDs assisted.\n"
        "                - **target_hero**: Array of assisted hero metadata (images).\n"
        "            - **strong**:\n"
        "                - **desc**: Description of heroes countered.\n"
        "                - **target_hero_id**: Array of hero IDs countered.\n"
        "                - **target_hero**: Array of countered hero metadata (images).\n"
        "            - **weak**:\n"
        "                - **desc**: Description of heroes that counter this hero.\n"
        "                - **target_hero_id**: Array of hero IDs that counter.\n"
        "                - **target_hero**: Array of counter hero metadata (images).\n"
        "        - **url**: Official lore or profile URL.\n\n"
        "This endpoint is useful for:\n"
        "    - Displaying comprehensive hero profiles.\n"
        "    - Analyzing hero abilities and skill tags.\n"
        "    - Understanding hero synergies and counters.\n"
        "    - Linking lane and role assignments to gameplay analysis."
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
        "Supports query parameters for rank tier, pagination, and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Angela' → `angela`).\n\n"
        "Query parameters:\n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero statistics:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **main_hero**:\n"
        "            - **data**:\n"
        "                - **head**: Hero portrait image URL.\n"
        "                - **name**: Hero name.\n"
        "        - **main_heroid**: Hero ID.\n"
        "        - **main_hero_channel**:\n"
        "            - **id**: Channel ID reference.\n"
        "        - **main_hero_appearance_rate**: Hero pick rate (appearance frequency).\n"
        "        - **main_hero_ban_rate**: Hero ban rate.\n"
        "        - **main_hero_win_rate**: Hero win rate.\n"
        "        - **sub_hero**: Array of synergy heroes, each containing:\n"
        "            - **heroid**: Sub-hero ID.\n"
        "            - **hero_win_rate**: Sub-hero win rate.\n"
        "            - **hero_appearance_rate**: Sub-hero pick rate.\n"
        "            - **increase_win_rate**: Impact of sub-hero on win rate.\n"
        "            - **hero_channel**:\n"
        "                - **id**: Channel ID reference.\n"
        "            - **hero**:\n"
        "                - **data**:\n"
        "                    - **head**: Sub-hero portrait image URL.\n"
        "            - **min_win_rate6**: Win rate in matches ≤ 6 minutes.\n"
        "            - **min_win_rate6_8**: Win rate in matches 6–8 minutes.\n"
        "            - **min_win_rate8_10**: Win rate in matches 8–10 minutes.\n"
        "            - **min_win_rate10_12**: Win rate in matches 10–12 minutes.\n"
        "            - **min_win_rate12_14**: Win rate in matches 12–14 minutes.\n"
        "            - **min_win_rate14_16**: Win rate in matches 14–16 minutes.\n"
        "            - **min_win_rate16_18**: Win rate in matches 16–18 minutes.\n"
        "            - **min_win_rate18_20**: Win rate in matches 18–20 minutes.\n"
        "            - **min_win_rate20**: Win rate in matches ≥ 20 minutes.\n"
        "        - **sub_hero_last**: Array of negative synergy heroes, each containing:\n"
        "            - **heroid**: Sub-hero ID.\n"
        "            - **hero_win_rate**: Sub-hero win rate.\n"
        "            - **hero_appearance_rate**: Sub-hero pick rate.\n"
        "            - **increase_win_rate**: Negative impact on win rate.\n"
        "            - **min_win_rate6** through **min_win_rate20**: Win rate breakdown across match durations.\n\n"
        "This endpoint is useful for:\n"
        "    - Analyzing hero performance trends across different ranks.\n"
        "    - Tracking pick, ban, and win rates.\n"
        "    - Understanding synergy with other heroes.\n"
        "    - Identifying counters and negative synergies across match durations."
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
        "Supports query parameters for pagination and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Marcel' → `marcel`).\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero skill combo details:\n"
        "- **records**: Array of combo entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **caption**: Caption or localized label (e.g., laning, teamfight).\n"
        "    - **configId**: Configuration ID.\n"
        "    - **createdAt**: Creation timestamp.\n"
        "    - **createdUser**: Creator username.\n"
        "    - **data**:\n"
        "        - **hero_id**: Hero ID.\n"
        "        - **title**: Combo title (e.g., 'TEAMFIGHT COMBOS').\n"
        "        - **desc**: Descriptive instructions on how to execute the combo "
        "(e.g., laning phase or teamfight scenarios).\n"
        "        - **skill_id**: Array of skills in recommended sequence, each containing:\n"
        "            - **skillid**: Skill ID.\n"
        "            - **skillicon**: Skill icon URL.\n"
        "            - **_id**, **_createdAt**, **_updatedAt**: Metadata fields.\n"
        "    - **updatedAt**: Last update timestamp.\n"
        "    - **updatedUser**: Last updater username.\n\n"
        "This endpoint is useful for:\n"
        "    - Guiding players on optimal skill usage patterns.\n"
        "    - Teaching effective combos for laning and teamfight scenarios.\n"
        "    - Helping maximize hero performance in different situations."
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
        "Supports query parameters for rank tier, past days window, pagination, and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Balmond' → `balmond`).\n\n"
        "Query parameters:\n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **past-days**: Rate window in days. Allowed values: `7`, `15`, `30`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero rate trend data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **main_heroid**: Hero ID.\n"
        "        - **bigrank**: Rank tier identifier.\n"
        "        - **camp_type**: Camp type indicator.\n"
        "        - **match_type**: Match type indicator.\n"
        "        - **win_rate**: Array of daily statistics, each containing:\n"
        "            - **date**: Date of record.\n"
        "            - **app_rate**: Appearance rate (pick frequency).\n"
        "            - **ban_rate**: Ban rate.\n"
        "            - **win_rate**: Win rate.\n\n"
        "This endpoint is useful for:\n"
        "    - Tracking hero performance trends over time.\n"
        "    - Monitoring hero popularity and ban frequency.\n"
        "    - Comparing win rates across different ranks and time periods."
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
        "Supports query parameters for pagination and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero relation data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **data**:\n"
        "        - **hero**:\n"
        "            - **data**:\n"
        "                - **name**: Hero name.\n"
        "        - **hero_id**: Unique hero identifier.\n"
        "        - **relation**:\n"
        "            - **assist**:\n"
        "                - **target_hero_id**: Array of hero IDs that synergize well.\n"
        "            - **strong**:\n"
        "                - **target_hero_id**: Array of hero IDs that are countered.\n"
        "            - **weak**:\n"
        "                - **target_hero_id**: Array of hero IDs that counter this hero.\n\n"
        "This endpoint is useful for:\n"
        "    - Understanding hero synergies (assist).\n"
        "    - Identifying heroes that are countered (strong).\n"
        "    - Recognizing heroes that counter the selected hero (weak).\n"
        "    - Building balanced team compositions."
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
        "Supports query parameters for rank tier, pagination, and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero counter data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **main_hero**:\n"
        "            - **data**:\n"
        "                - **head**: Main hero portrait image URL.\n"
        "                - **name**: Main hero name.\n"
        "        - **main_heroid**: Main hero ID.\n"
        "        - **main_hero_channel**:\n"
        "            - **id**: Channel ID reference.\n"
        "        - **main_hero_appearance_rate**: Pick rate of the main hero.\n"
        "        - **main_hero_ban_rate**: Ban rate of the main hero.\n"
        "        - **main_hero_win_rate**: Win rate of the main hero.\n"
        "        - **sub_hero**: Array of counter heroes, each containing:\n"
        "            - **heroid**: Counter hero ID.\n"
        "            - **hero_win_rate**: Counter hero win rate.\n"
        "            - **hero_appearance_rate**: Counter hero pick rate.\n"
        "            - **increase_win_rate**: Impact of counter hero on win rate.\n"
        "            - **hero_channel**:\n"
        "                - **id**: Channel ID reference.\n"
        "            - **hero**:\n"
        "                - **data**:\n"
        "                    - **head**: Counter hero portrait image URL.\n"
        "            - **min_win_rate6** through **min_win_rate20**: Win rate breakdown across match durations.\n"
        "        - **sub_hero_last**: Array of negative synergy heroes, each containing:\n"
        "            - **heroid**: Sub-hero ID.\n"
        "            - **hero_win_rate**: Sub-hero win rate.\n"
        "            - **hero_appearance_rate**: Sub-hero pick rate.\n"
        "            - **increase_win_rate**: Negative impact on win rate.\n"
        "            - **min_win_rate6** through **min_win_rate20**: Win rate breakdown across match durations.\n\n"
        "This endpoint is useful for:\n"
        "    - Identifying which heroes are effective counters.\n"
        "    - Analyzing matchup dynamics.\n"
        "    - Understanding performance trends across different ranks and match durations."
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
        "Supports query parameters for rank tier, pagination, and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero compatibility data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **main_hero**:\n"
        "            - **data**:\n"
        "                - **head**: Main hero portrait image URL.\n"
        "                - **name**: Main hero name.\n"
        "        - **main_heroid**: Main hero ID.\n"
        "        - **main_hero_channel**:\n"
        "            - **id**: Channel ID reference.\n"
        "        - **main_hero_appearance_rate**: Pick rate of the main hero.\n"
        "        - **main_hero_ban_rate**: Ban rate of the main hero.\n"
        "        - **main_hero_win_rate**: Win rate of the main hero.\n"
        "        - **sub_hero**: Array of compatible heroes, each containing:\n"
        "            - **heroid**: Compatible hero ID.\n"
        "            - **hero_win_rate**: Compatible hero win rate.\n"
        "            - **hero_appearance_rate**: Compatible hero pick rate.\n"
        "            - **increase_win_rate**: Positive synergy impact on win rate.\n"
        "            - **hero_channel**:\n"
        "                - **id**: Channel ID reference.\n"
        "            - **hero**:\n"
        "                - **data**:\n"
        "                    - **head**: Compatible hero portrait image URL.\n"
        "            - **min_win_rate6** through **min_win_rate20**: Win rate breakdown across match durations.\n"
        "        - **sub_hero_last**: Array of negative synergy heroes, each containing:\n"
        "            - **heroid**: Sub-hero ID.\n"
        "            - **hero_win_rate**: Sub-hero win rate.\n"
        "            - **hero_appearance_rate**: Sub-hero pick rate.\n"
        "            - **increase_win_rate**: Negative impact on win rate.\n"
        "            - **min_win_rate6** through **min_win_rate20**: Win rate breakdown across match durations.\n\n"
        "This endpoint is useful for:\n"
        "    - Identifying which heroes pair well with the selected hero.\n"
        "    - Analyzing synergy and team composition effectiveness.\n"
        "    - Recognizing combinations that reduce performance.\n"
        "    - Understanding matchup dynamics across ranks and match durations."
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
