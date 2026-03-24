from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query

from app.api.dependencies import require_api_available

from app.services.academy import fetch_academy_post, fetch_ratings_all, fetch_ratings_subject

from app.core.errors import _hero_id_or_404

from app.core.enums import LanguageEnum, RankEnum, SortOrderEnum, HeroRoleEnum, HeroLaneEnum
from app.utils.client_ip import bind_client_ip
from app.utils.filters import (
    ROLE_MAP, LANE_MAP, validate_and_map_multi, validate_and_map_rank, validate_and_single
)

router = APIRouter(
    prefix="/api/academy",
    tags=["academy"],
    dependencies=[
        Depends(require_api_available),
        Depends(bind_client_ip)
    ]
)


@router.get(
    path="/meta/version",
    summary="Game Version Info",
    description=(
        "Fetch a list of game versions with their release dates. "
        "Supports query parameters for pagination, sorting, and localization.\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **order**: Sort order for results. Allowed values: `asc`, `desc`.\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes game version data:\n"
        "- **records**: Array of version entries, each containing:\n"
        "    - **id**: Unique version record identifier.\n"
        "    - **uin**: User identifier associated with the record.\n"
        "    - **createdAt**: Creation timestamp.\n"
        "    - **updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **game_version**: Version string (e.g., `2.1.18`).\n"
        "    - **form**:\n"
        "        - **id**: Form ID reference.\n"
        "    - **vote_all** (optional): Voting metadata, if available:\n"
        "        - **target**: Target record ID.\n"
        "        - **vote**:\n"
        "            - **id**: Vote ID.\n\n"
        "This endpoint is useful for:\n"
        "- Tracking game version history.\n"
        "- Monitoring release cycles.\n"
        "- Ensuring compatibility with specific patches or updates."
    ),
)
def version(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    order: Annotated[
        SortOrderEnum,
        Query(
            title="Sort Order",
            description="Sort order for results.",
        )
    ] = SortOrderEnum.DESCENDING,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
    path="/heroes/catalog",
    summary="Hero Catalog",
    description=(
        "Supports query parameters for pagination and localization.\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero catalog data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **data**:\n"
        "        - **head**: Hero portrait image URL.\n"
        "        - **head_big**: Larger hero portrait image URL.\n"
        "        - **painting**: Hero splash art image URL.\n"
        "        - **hero**:\n"
        "            - **data**:\n"
        "                - **name**: Hero name.\n"
        "                - **roadsort**: Lane assignment metadata:\n"
        "                    - **_id**: Unique identifier.\n"
        "                    - **caption**: Lane caption (localized).\n"
        "                    - **configId**: Configuration ID.\n"
        "                    - **createdAt**: Creation timestamp.\n"
        "                    - **createdUser**: Creator username.\n"
        "                    - **data**:\n"
        "                        - **road_sort_icon**: Lane icon URL.\n"
        "                        - **road_sort_id**: Lane ID.\n"
        "                        - **road_sort_title**: Lane title (e.g., Roam).\n"
        "                    - **updatedAt**: Last update timestamp.\n"
        "                    - **updatedUser**: Last updater username.\n"
        "        - **hero_id**: Unique hero identifier.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying hero collections.\n"
        "- Browsing available heroes.\n"
        "- Analyzing basic hero attributes.\n\n"
    ),
    deprecated=True,
)
def heroes_old(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "Supports query parameters for pagination, sorting, and localization.\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **order**: Sort order for results. Allowed values: `asc`, `desc`.\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes role data:\n"
        "- **records**: Array of role entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **caption**: Localized role caption (e.g., '坦克', '法师').\n"
        "    - **configId**: Configuration ID.\n"
        "    - **createdAt**: Creation timestamp.\n"
        "    - **createdUser**: Creator username.\n"
        "    - **updatedAt**: Last update timestamp.\n"
        "    - **updatedUser**: Last updater username.\n"
        "    - **data**:\n"
        "        - **emblem_id**: Emblem ID associated with the role.\n"
        "        - **emblem_title**: Emblem title (e.g., 'Tank', 'Mage').\n"
        "        - **emblem_icon**: Emblem icon URL.\n"
        "        - **emblem_detail**:\n"
        "            - **_id**: Emblem detail record ID.\n"
        "            - **_createdAt**: Creation timestamp.\n"
        "            - **_updatedAt**: Last update timestamp.\n"
        "            - **data**:\n"
        "                - **emblemid**: Emblem ID.\n"
        "                - **emblemname**: Emblem name (e.g., 'Assassin').\n"
        "                - **emblemattrid**: Attribute ID.\n"
        "                - **emblemattr**: Attribute bonuses (e.g., '+500 Extra Max HP').\n"
        "                - **attriicon**: Attribute icon URL.\n"
        "                - **attriicon2**: Secondary attribute icon URL (optional).\n"
        "                - **emblembg**: Background indicator.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying role categories.\n"
        "- Explaining role-specific attributes and emblem bonuses.\n"
        "- Guiding players in hero selection based on roles."
    ),
)
def roles(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    order: Annotated[
        SortOrderEnum,
        Query(
            title="Sort Order",
            description="Sort order by emblem_id.",
        )
    ] = SortOrderEnum.ASCENDING,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "List all equipment (items). Supports query parameters for pagination and localization.\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes equipment data:\n"
        "- **records**: Array of equipment entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **equipid**: Equipment ID.\n"
        "        - **equipname**: Equipment name (e.g., 'Bud of Hope').\n"
        "        - **equipicon**: Equipment icon URL.\n"
        "    - **id**: Internal record ID.\n"
        "    - **sourceId**: Source reference ID.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying the full equipment catalog.\n"
        "- Browsing available items.\n"
        "- Analyzing basic item attributes."
    ),
)
def equipment(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
    path="/equipment/expanded",
    summary="Equipment Expanded",
    description=(
        "Get detailed information about a specific equipment item. "
        "Supports query parameters for pagination and localization.\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes detailed equipment data:\n"
        "- **records**: Array of equipment entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **equipid**: Equipment ID.\n"
        "        - **equipname**: Equipment name (e.g., 'Demon Boots - Favor').\n"
        "        - **equipicon**: Equipment icon URL.\n"
        "        - **equiptype**: Equipment type ID.\n"
        "        - **equiptypename**: Equipment type name (e.g., 'Roam').\n"
        "        - **equipskill1–7**: Passive skills or effects (raw text segments).\n"
        "        - **equipskilldesc**: Full description of equipment skills and effects.\n"
        "        - **equiptips**: Item tips or stat bonuses (e.g., '+40 Movement Speed').\n"
        "        - **targetequipid**: Target equipment ID (if linked).\n"
        "    - **id**: Internal record ID.\n"
        "    - **sourceId**: Source reference ID.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying full item details.\n"
        "- Explaining equipment effects and passive skills.\n"
        "- Guiding players in equipment selection and strategy."
    ),
)
def equipment_details(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "List all battle spells with details. Supports query parameters for pagination and localization.\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes battle spell data:\n"
        "- **records**: Array of spell entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **battleskillid**: Battle spell ID.\n"
        "        - **skillid**: Skill ID.\n"
        "        - **skillname**: Spell name (e.g., 'Arrival').\n"
        "        - **skillicon**: Spell icon URL.\n"
        "        - **skillshortdesc**: Short description (e.g., 'Long-range Support').\n"
        "        - **skilldesc**: Full description of spell effects.\n"
        "        - **skilldescemblem**: Emblem-specific description (if applicable).\n"
        "        - **skillvideo**: Video reference (if available).\n"
        "    - **id**: Internal record ID.\n"
        "    - **sourceId**: Source reference ID.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying the complete catalog of battle spells.\n"
        "- Explaining spell effects and mechanics.\n"
        "- Guiding players in spell selection and strategy."
    ),
)
def spells(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "List all emblems with details. Supports query parameters for pagination and localization.\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes emblem data:\n"
        "- **records**: Array of emblem entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **giftid**: Emblem ID.\n"
        "        - **gifttiers**: Emblem tier level.\n"
        "        - **emblemskill**: Associated skill details:\n"
        "            - **skillid**: Skill ID.\n"
        "            - **skillid_lv**: Skill ID with level reference.\n"
        "            - **skillname**: Skill name (e.g., 'Weapons Master').\n"
        "            - **skillicon**: Skill icon URL.\n"
        "            - **skilldesc**: Full description of skill effects.\n"
        "            - **skilldesc_text**: Template-based description with placeholders.\n"
        "            - **skilldescemblem**: Emblem-specific description.\n"
        "            - **numdescribe**: Numeric effect values (e.g., '5%').\n"
        "    - **id**: Internal record ID.\n"
        "    - **sourceId**: Source reference ID.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying the full emblem catalog.\n"
        "- Explaining emblem effects and associated skills.\n"
        "- Guiding players in emblem selection and optimization."
    ),
)
def emblems(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
    path="/ranks",
    summary="Ranks List",
    description=(
        "Retrieve all rank information for MLBB. Supports query parameters for pagination and localization.\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes rank data:\n"
        "- **records**: Array of rank entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **configId**: Configuration ID.\n"
        "    - **caption**: Localized caption (e.g., '1-4勇士Ⅲ').\n"
        "    - **createdAt**: Creation timestamp.\n"
        "    - **createdUser**: Creator username.\n"
        "    - **updatedAt**: Last update timestamp.\n"
        "    - **updatedUser**: Last updater username.\n"
        "    - **data**:\n"
        "        - **bigrank**: Major rank ID (e.g., 1).\n"
        "        - **bigrank_name**: Major rank name (e.g., '勇士').\n"
        "        - **icon**: Rank icon URL.\n"
        "        - **minrank**: Minor rank ID (e.g., '1').\n"
        "        - **minrank_name**: Minor rank name (e.g., 'Ⅲ').\n"
        "        - **rankid_start**: Starting rank ID in the range.\n"
        "        - **rankid_end**: Ending rank ID in the range.\n"
        "    - **id**: Internal record ID.\n"
        "    - **sort**: Sorting index.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying the full rank progression system.\n"
        "- Explaining rank tiers and ranges.\n"
        "- Guiding players in understanding MLBB's ranking structure."
    ),
)
def ranks(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
    path="/ranks/{rank_id}",
    summary="Ranks Details",
    description=(
        "Retrieve details for a specific rank in MLBB by rank ID. "
        "Supports query parameter for localization.\n\n"
        "Path parameters:\n"
        "- **rank_id**: Rank ID (validated dynamically from current rank list). "
        "Minimum: 1, Maximum: 9999.\n\n"
        "Query parameters:\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes detailed rank data:\n"
        "- **records**: Array of rank entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **configId**: Configuration ID.\n"
        "    - **caption**: Localized caption (e.g., '236-9999荣耀神话').\n"
        "    - **createdAt**: Creation timestamp.\n"
        "    - **createdUser**: Creator username.\n"
        "    - **updatedAt**: Last update timestamp.\n"
        "    - **updatedUser**: Last updater username.\n"
        "    - **data**:\n"
        "        - **bigrank**: Major rank ID (e.g., 7).\n"
        "        - **bigrank_name**: Major rank name (e.g., '荣耀神话').\n"
        "        - **icon**: Rank icon URL.\n"
        "        - **rankid_start**: Starting rank ID in the range.\n"
        "        - **rankid_end**: Ending rank ID in the range.\n"
        "    - **id**: Internal record ID.\n"
        "    - **linkId**: Linked object references.\n"
        "    - **sort**: Sorting index.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying detailed information about a single rank tier.\n"
        "- Explaining its position in the progression system.\n"
        "- Guiding players in understanding MLBB's ranking structure."
    ),
)
def ranks_details(
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
            title="Language",
            description="Language code for localized content.",
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
        "List recommended content for players. Supports query parameters for pagination, sorting, and localization.\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **order**: Sort order for results. Allowed values: `asc`, `desc`.\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes recommended content data:\n"
        "- **records**: Array of recommended entries, each containing:\n"
        "    - **createdAt**: Creation timestamp.\n"
        "    - **updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **channels**: Content channels (e.g., 'UGC', 'recommend').\n"
        "        - **type**: Content type (e.g., 'ugc_hero').\n"
        "        - **state**: Content state (e.g., 'release').\n"
        "        - **data**:\n"
        "            - **hero**: Hero metadata including:\n"
        "                - **hero_id**: Hero ID.\n"
        "                - **hero_lane**: Lane assignment.\n"
        "                - **hero_overview**: Overview description.\n"
        "                - **hero_strength**: Strengths.\n"
        "                - **hero_weakness**: Weaknesses.\n"
        "                - **hero_tags**: Array of tag IDs.\n"
        "            - **equips**: Recommended equipment builds.\n"
        "            - **emblems**: Recommended emblem sets.\n"
        "            - **spell**: Recommended battle spell.\n"
        "            - **cooperates**: Cooperative hero synergies.\n"
        "            - **counters**: Counter heroes.\n"
        "            - **dominants**: Dominant strategies or tips.\n"
        "            - **recommend**: General recommendation notes.\n"
        "            - **snapshot**: Snapshot image URL.\n"
        "            - **game_version**: Version reference.\n"
        "            - **language**: Content language.\n"
        "            - **pages**: Content sections (e.g., 'hero', 'spell', 'equip').\n"
        "            - **title**: Guide or build title.\n"
        "        - **user**: Author metadata including:\n"
        "            - **name**: Author name.\n"
        "            - **avatar**: Author avatar URL.\n"
        "            - **level**: Author level.\n"
        "            - **roleId**: Role ID.\n"
        "            - **zoneId**: Zone ID.\n"
        "        - **dynamic**: Engagement metrics:\n"
        "            - **views**: Total views.\n"
        "            - **votes**: Total votes.\n"
        "            - **hot**: Hotness score.\n"
        "            - **views_by_4h_total_24h**: Views in last 24h.\n"
        "        - **vote_all**: Voting metadata:\n"
        "            - **average**: Average rating.\n"
        "            - **count**: Vote count.\n"
        "            - **total**: Total votes.\n"
        "            - **user_count**: Number of users voted.\n"
        "            - **vote**: Vote ID reference.\n\n"
        "This endpoint is useful for:\n"
        "- Surfacing community guides and builds.\n"
        "- Providing personalized hero strategies.\n"
        "- Highlighting cooperative and counter hero recommendations.\n"
        "- Guiding players with contextual tips and strategic insights."
    ),
)
def recommended(
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    order: Annotated[
        SortOrderEnum,
        Query(
            title="Sort Order",
            description="Order by trending and creation date.",
        )
    ] = SortOrderEnum.DESCENDING,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "Supports query parameters for pagination and localization.\n\n"
        "Path parameters:\n"
        "- **recommended_id**: Identifier for the recommended post (minimum: 1).\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes detailed recommended content data:\n"
        "- **records**: Array of recommended entries, each containing:\n"
        "    - **createdAt**: Creation timestamp.\n"
        "    - **updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **channels**: Content channels (e.g., 'UGC', 'recommend').\n"
        "        - **type**: Content type (e.g., 'ugc_hero').\n"
        "        - **state**: Content state (e.g., 'release').\n"
        "        - **data**:\n"
        "            - **hero**: Hero metadata including:\n"
        "                - **hero_id**: Hero ID.\n"
        "                - **hero_lane**: Lane assignment.\n"
        "                - **hero_overview**: Overview description.\n"
        "                - **hero_strength**: Strengths.\n"
        "                - **hero_weakness**: Weaknesses.\n"
        "                - **hero_tags**: Array of tag IDs.\n"
        "            - **equips**: Recommended equipment builds with IDs and descriptions.\n"
        "            - **emblems**: Recommended emblem sets with IDs and descriptions.\n"
        "            - **spell**: Recommended battle spell with ID and description.\n"
        "            - **cooperates**: Cooperative hero synergies with descriptions and rates.\n"
        "            - **counters**: Counter heroes with descriptions and rates.\n"
        "            - **dominants**: Dominant strategies or tips.\n"
        "            - **recommend**: General recommendation notes.\n"
        "            - **snapshot**: Snapshot image URL.\n"
        "            - **game_version**: Version reference.\n"
        "            - **language**: Content language.\n"
        "            - **pages**: Content sections (e.g., 'hero', 'spell', 'equip').\n"
        "            - **title**: Guide or build title.\n"
        "        - **user**: Author metadata including:\n"
        "            - **name**: Author name.\n"
        "            - **avatar**: Author avatar URL.\n"
        "            - **level**: Author level.\n"
        "            - **roleId**: Role ID.\n"
        "            - **zoneId**: Zone ID.\n"
        "        - **dynamic**: Engagement metrics:\n"
        "            - **views**: Total views.\n"
        "            - **votes**: Total votes.\n"
        "            - **hot**: Hotness score.\n"
        "            - **views_by_4h_total_24h**: Views in last 24h.\n"
        "        - **vote_all**: Voting metadata:\n"
        "            - **average**: Average rating.\n"
        "            - **count**: Vote count.\n"
        "            - **total**: Total votes.\n"
        "            - **user_count**: Number of users voted.\n"
        "            - **vote**: Vote ID reference.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying full details of a single guide or build.\n"
        "- Explaining strategic recommendations.\n"
        "- Surfacing community-generated content for MLBB players."
    ),
)
def recommended_detail(
    recommended_id: Annotated[
        int,
        Path(
            title="Recommended Post ID",
            description="The ID of the recommended post to retrieve.",
            ge=1
        )
    ],
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "Supports query parameters for role, lane, pagination, sorting, and localization.\n\n"
        "Query parameters:\n"
        "- **role**: Role filter. Multi allowed: `tank`, `fighter`, `assassin`, `mage`, `marksman`, `support`. "
        "Example: `role=tank&role=fighter`.\n"
        "- **lane**: Lane filter. Multi allowed: `exp`, `mid`, `roam`, `jungle`, `gold`. "
        "Example: `lane=exp&lane=mid`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **order**: Sort order for results. Allowed values: `asc`, `desc`.\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero filter data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **data**:\n"
        "        - **hero_id**: Unique hero identifier.\n"
        "        - **head**: Hero portrait image URL.\n"
        "        - **hero**:\n"
        "            - **data**:\n"
        "                - **name**: Hero name (e.g., 'Miya').\n\n"
        "This endpoint is useful for:\n"
        "- Filtering heroes by gameplay role.\n"
        "- Filtering heroes by lane assignment.\n"
        "- Displaying customized hero lists in MLBB Academy."
    ),
)
def heroes(
    role: Annotated[
        list[str],
        Query(
            title="Role",
            description="Filter heroes by role.",
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
            title="Lane",
            description="Filter heroes by lane.",
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
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    order: Annotated[
        SortOrderEnum,
        Query(
            title="Sort Order",
            description="Sort order by hero ID.",
        )
    ] = SortOrderEnum.ASCENDING,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "Supports query parameters for rank, pagination, and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero statistics data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **main_hero**:\n"
        "            - **data**:\n"
        "                - **hero**:\n"
        "                    - **data**:\n"
        "                        - **head**: Main hero portrait image URL.\n"
        "                        - **name**: Main hero name.\n"
        "        - **main_heroid**: Main hero ID.\n"
        "        - **main_hero_appearance_rate**: Pick rate of the main hero.\n"
        "        - **main_hero_ban_rate**: Ban rate of the main hero.\n"
        "        - **main_hero_win_rate**: Win rate of the main hero.\n"
        "        - **sub_hero**: Array of synergy heroes, each containing:\n"
        "            - **heroid**: Hero ID.\n"
        "            - **hero_win_rate**: Win rate of the synergy hero.\n"
        "            - **hero_appearance_rate**: Pick rate of the synergy hero.\n"
        "            - **increase_win_rate**: Positive synergy impact on win rate.\n"
        "            - **min_win_rate6–20**: Win rate breakdown across match durations.\n"
        "            - **hero**:\n"
        "                - **data**:\n"
        "                    - **hero**:\n"
        "                        - **data**:\n"
        "                            - **head**: Synergy hero portrait image URL.\n"
        "        - **sub_hero_last**: Array of negative synergy heroes, each containing:\n"
        "            - **heroid**: Hero ID.\n"
        "            - **hero_win_rate**: Win rate of the sub-hero.\n"
        "            - **hero_appearance_rate**: Pick rate of the sub-hero.\n"
        "            - **increase_win_rate**: Negative impact on win rate.\n"
        "            - **min_win_rate6–20**: Win rate breakdown across match durations.\n\n"
        "This endpoint is useful for:\n"
        "- Analyzing hero performance across different ranks.\n"
        "- Understanding meta trends.\n"
        "- Guiding players in hero selection and strategy."
    ),
)
def heroes_stats(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=(
                "Hero identifier as numeric hero ID or hero name. "
                "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Luo Yi' → `luoyi`)."
            ),
        )
    ],
    rank: Annotated[
        RankEnum,
        Query(
            title="Rank",
            description="Rank filter for hero statistics.",
        ),
    ] = RankEnum.ALL,
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "Supports query parameters for pagination and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero lane distribution data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **data**:\n"
        "        - **hero_id**: Unique hero identifier.\n"
        "        - **hero**:\n"
        "            - **data**:\n"
        "                - **roadsort**: Array of lane assignments, each containing:\n"
        "                    - **_id**: Unique record identifier.\n"
        "                    - **caption**: Localized lane caption (e.g., '打野').\n"
        "                    - **configId**: Configuration ID.\n"
        "                    - **createdAt**: Creation timestamp.\n"
        "                    - **createdUser**: Creator username.\n"
        "                    - **updatedAt**: Last update timestamp.\n"
        "                    - **updatedUser**: Last updater username.\n"
        "                    - **data**:\n"
        "                        - **road_sort_id**: Lane ID (e.g., '4').\n"
        "                        - **road_sort_title**: Lane title (e.g., 'Jungle').\n"
        "                        - **road_sort_icon**: Lane icon URL.\n\n"
        "This endpoint is useful for:\n"
        "- Analyzing hero lane preferences.\n"
        "- Understanding optimal lane assignments.\n"
        "- Guiding players in hero positioning strategies."
    ),
)
def heroes_lane(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=(
                "Hero identifier as numeric hero ID or hero name. "
                "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Luo Yi' → `luoyi`)."
            ),
        )
    ],
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
    path="/heroes/{hero_identifier}/win-rate/timeline",
    summary="Hero Lane Time-based Win Rate",
    description=(
        "Retrieve time-based win rate statistics for a specific hero in a given lane. "
        "Supports query parameters for rank, pagination, and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **lane**: Lane. Allowed values: `exp`, `mid`, `roam`, `jungle`, `gold`. from `/api/academy/heroes/{hero_identifier}/lane` \n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero lane time-based win rate data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **heroid**: Hero ID.\n"
        "        - **hero_name**: Hero name.\n"
        "        - **real_road**: Lane ID (e.g., 4 for Jungle).\n"
        "        - **total_win_rate**: Overall win rate for the hero in this lane.\n"
        "        - **time_win_rate**: Array of segmented win rates by match duration:\n"
        "            - **time_min**: Minimum time interval (minutes).\n"
        "            - **time_max**: Maximum time interval (minutes).\n"
        "            - **win_rate**: Win rate within that time range.\n\n"
        "This endpoint is useful for:\n"
        "- Analyzing hero performance progression over match duration.\n"
        "- Understanding lane-specific strengths.\n"
        "- Guiding players in timing strategies for optimal hero usage."
    ),
)
def heroes_time_win_rate(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=(
                "Hero identifier as numeric hero ID or hero name. "
                "Name matching ignores spaces/symbols and is case-insensitive (e.g., `Luo Yi` to `luoyi`)."
            ),
        )
    ],
    lane: Annotated[
        HeroLaneEnum,
        Query(
            title="Lane",
            description="Filter heroes by lane `/api/academy/heroes/{hero_identifier}/lane`.",
        )
    ],
    rank: Annotated[
        RankEnum,
        Query(
            title="Rank",
            description="Rank filter for hero statistics.",
        ),
    ] = RankEnum.ALL,
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    lane_value = validate_and_single([lane], LANE_MAP, "lane")
    
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
                "value": lane_value
            },
        ],
        "sorts": [],
    }
    return fetch_academy_post("2777027", payload, lang)


@router.get(
    path="/heroes/{hero_identifier}/builds",
    summary="Hero Recommended Builds",
    description=(
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **lane**: Lane. Allowed values: `exp`, `mid`, `roam`, `jungle`, `gold`. from `/api/academy/heroes/{hero_identifier}/lane` \n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero build data:\n"
        "- **records**: Array of build entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **heroid**: Hero ID.\n"
        "        - **hero_name**: Hero name.\n"
        "        - **real_road**: Lane assignment ID.\n"
        "        - **build**: Array of recommended builds, each containing:\n"
        "            - **equipid**: List of equipment IDs.\n"
        "            - **emblem**: Emblem configuration:\n"
        "                - **emblemid**: Emblem ID.\n"
        "                - **emblemname**: Emblem name.\n"
        "                - **emblemattr**: Emblem attributes (e.g., '+10% Spell Vamp').\n"
        "                - **attriicon**: Emblem attribute icon URL.\n"
        "            - **battleskill**: Battle spell configuration:\n"
        "                - **battleskillid**: Battle spell ID.\n"
        "                - **skillname**: Spell name (e.g., 'Retribution').\n"
        "                - **skillshortdesc**: Short description.\n"
        "                - **skilldesc**: Full description of spell effects.\n"
        "                - **skillicon**: Spell icon URL.\n"
        "            - **runeid**: Rune ID.\n"
        "            - **new_rune_skill**: Array of rune skill IDs.\n"
        "            - **build_pick_rate**: Pick rate of the build.\n"
        "            - **build_win_rate**: Win rate of the build.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying historical or community-recommended builds.\n"
        "- Providing backward compatibility for older integrations.\n"
        "- Should be replaced with newer endpoints for up-to-date build recommendations."
    ),
)
def heroes_builds(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=(
                "Hero identifier as numeric hero ID or hero name. "
                "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Luo Yi' → `luoyi`)."
            ),
        )
    ],
    lane: Annotated[
        HeroLaneEnum,
        Query(
            title="Lane",
            description="Filter heroes by lane (`/api/academy/heroes/{hero_identifier}/lane`).",
        )
    ],
    rank: Annotated[
        RankEnum,
        Query(
            title="Rank",
            description="Rank filter for hero statistics.",
        ),
    ] = RankEnum.ALL,
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    hero_id = _hero_id_or_404(hero_identifier, lang)
    lane_value = validate_and_single([lane], LANE_MAP, "lane")
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
                "value": lane_value
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
        "Supports query parameters for rank, pagination, and localization.\n\n"
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
        "        - **main_heroid**: Target hero ID.\n"
        "        - **main_hero_ban_rate**: Ban rate of the target hero.\n"
        "        - **main_hero_pick_rate**: Pick rate of the target hero.\n"
        "        - **main_hero_win_rate**: Win rate of the target hero.\n"
        "        - **sub_hero**: Array of counter heroes, each containing:\n"
        "            - **heroid**: Counter hero ID.\n"
        "            - **hero_win_rate**: Win rate of the counter hero.\n"
        "            - **increase_win_rate**: Impact value showing how much this hero improves or reduces win rate against the target.\n\n"
        "This endpoint is useful for:\n"
        "- Analyzing which heroes perform well against the target hero.\n"
        "- Understanding matchup dynamics.\n"
        "- Guiding players in drafting strategies."
    ),
)
def heroes_counters(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=(
                "Hero identifier as numeric hero ID or hero name. "
                "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Luo Yi' → `luoyi`)."
            ),
        )
    ],
    rank: Annotated[
        RankEnum,
        Query(
            title="Rank",
            description="Rank filter for hero statistics.",
        ),
    ] = RankEnum.ALL,
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "Supports query parameters for rank, pagination, and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero teammate data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **main_heroid**: Target hero ID.\n"
        "        - **main_hero_ban_rate**: Ban rate of the target hero.\n"
        "        - **main_hero_pick_rate**: Pick rate of the target hero.\n"
        "        - **main_hero_win_rate**: Win rate of the target hero.\n"
        "        - **sub_hero**: Array of teammate heroes, each containing:\n"
        "            - **heroid**: Teammate hero ID.\n"
        "            - **hero_win_rate**: Win rate of the teammate hero.\n"
        "            - **increase_win_rate**: Impact value showing how much this hero improves or reduces win rate when paired with the target.\n\n"
        "This endpoint is useful for:\n"
        "- Analyzing which heroes synergize well with the target hero.\n"
        "- Understanding team composition dynamics.\n"
        "- Guiding players in drafting strategies."
    ),
)
def heroes_teammates(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=(
                "Hero identifier as numeric hero ID or hero name. "
                "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Luo Yi' → `luoyi`)."
            ),
        )
    ],
    rank: Annotated[
        RankEnum,
        Query(
            title="Rank",
            description="Rank filter for hero statistics.",
        ),
    ] = RankEnum.ALL,
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "Supports query parameters for days, rank, pagination, and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **days**: Trend window in days. Allowed values: `7`, `15`, `30`.\n"
        "- **rank**: Rank filter. Allowed values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`.\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero performance trend data:\n"
        "- **records**: Array of hero entries, each containing:\n"
        "    - **_id**: Unique record identifier.\n"
        "    - **_createdAt**: Creation timestamp.\n"
        "    - **_updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **main_heroid**: Hero ID.\n"
        "        - **bigrank**: Rank context ID.\n"
        "        - **camp_type**: Camp type indicator.\n"
        "        - **match_type**: Match type indicator.\n"
        "        - **win_rate**: Array of daily statistics, each containing:\n"
        "            - **date**: Date of record.\n"
        "            - **app_rate**: Appearance rate.\n"
        "            - **ban_rate**: Ban rate.\n"
        "            - **win_rate**: Win rate.\n\n"
        "This endpoint is useful for:\n"
        "- Tracking hero performance changes over time.\n"
        "- Identifying meta shifts across ranks.\n"
        "- Guiding players in understanding how a hero’s effectiveness evolves across different ranks and timeframes."
    ),
)
def heroes_trends(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=(
                "Hero identifier as numeric hero ID or hero name. "
                "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Luo Yi' → `luoyi`)."
            ),
        )
    ],
    days: Annotated[
        Literal["7", "15", "30"],
        Query(
            title="Trend Window (Days)",
            description=(
                "Time window for trend data in days."
            ),

        ),
    ] = "7",
    rank: Annotated[
        RankEnum,
        Query(
            title="Rank",
            description="Rank filter for hero statistics.",
        ),
    ] = RankEnum.ALL,
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "Supports query parameters for pagination, sorting, and localization.\n\n"
        "Path parameters:\n"
        "- **hero_identifier**: Hero identifier as numeric hero ID or hero name. "
        "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Fanny' → `fanny`).\n\n"
        "Query parameters:\n"
        "- **size**: Number of items per page (minimum: 1).\n"
        "- **index**: Page index (starting from 1).\n"
        "- **order**: Sort order for recommendation hotness or creation time. Allowed values: `asc`, `desc`.\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero recommended content data:\n"
        "- **records**: Array of recommended entries, each containing:\n"
        "    - **createdAt**: Creation timestamp.\n"
        "    - **updatedAt**: Last update timestamp.\n"
        "    - **data**:\n"
        "        - **channels**: Content channels (e.g., 'UGC', 'recommend').\n"
        "        - **type**: Content type (e.g., 'ugc_hero').\n"
        "        - **state**: Content state (e.g., 'release').\n"
        "        - **data**:\n"
        "            - **hero**: Hero metadata including:\n"
        "                - **hero_id**: Hero ID.\n"
        "                - **hero_lane**: Lane assignment.\n"
        "                - **hero_tags**: Array of tag IDs.\n"
        "            - **equips**: Recommended equipment builds with IDs and descriptions.\n"
        "            - **emblems**: Recommended emblem sets with IDs and descriptions.\n"
        "            - **spell**: Recommended battle spell with ID and description.\n"
        "            - **cooperates**: Cooperative hero synergies with descriptions and rates.\n"
        "            - **counters**: Counter heroes with descriptions and rates.\n"
        "            - **dominants**: Dominant strategies or tips.\n"
        "            - **recommend**: General recommendation notes.\n"
        "            - **snapshot**: Snapshot image URL.\n"
        "            - **game_version**: Version reference.\n"
        "            - **language**: Content language.\n"
        "            - **pages**: Content sections (e.g., 'hero', 'spell', 'equip').\n"
        "            - **title**: Guide or build title.\n"
        "        - **user**: Author metadata including:\n"
        "            - **name**: Author name.\n"
        "            - **avatar**: Author avatar URL.\n"
        "            - **level**: Author level.\n"
        "            - **roleId**: Role ID.\n"
        "            - **zoneId**: Zone ID.\n"
        "        - **dynamic**: Engagement metrics:\n"
        "            - **views**: Total views.\n"
        "            - **hot**: Hotness score.\n"
        "            - **votes**: Total votes.\n"
        "            - **views_by_4h_total_24h**: Views in last 24h.\n"
        "        - **vote_all**: Voting metadata:\n"
        "            - **target**: Target content ID.\n"
        "            - **vote**: Vote ID reference.\n\n"
        "This endpoint is useful for:\n"
        "- Surfacing curated or community-recommended hero guides.\n"
        "- Providing builds, emblems, and strategies tailored to a hero.\n"
        "- Highlighting cooperative and counter hero recommendations.\n"
        "- Guiding players with contextual tips and shared experiences."
    ),
)
def heroes_recommended(
    hero_identifier: Annotated[
        str,
        Path(
            title="Hero Identifier",
            description=(
                "Hero identifier as numeric hero ID or hero name. "
                "Name matching ignores spaces/symbols and is case-insensitive (e.g., 'Luo Yi' → `luoyi`)."
            ),
        )
    ],
    size: Annotated[
        int,
        Query(
            title="Page Size",
            description="Number of items per page.",
            ge=1,
        )
    ] = 20,
    index: Annotated[
        int,
        Query(
            title="Page Index",
            description="Page index for pagination.",
            ge=1,
        )
    ] = 1,
    order: Annotated[
        SortOrderEnum,
        Query(
            title="Sort Order",
            description="Sort order for recommendation hotness and creation time.",
        ),
    ] = SortOrderEnum.DESCENDING,
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
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
        "Supports query parameter for localization.\n\n"
        "Query parameters:\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero ratings data:\n"
        "- **list**: Array of rating subjects, each containing:\n"
        "    - **subject**: Poll subject ID.\n"
        "    - **title**: Poll title (e.g., 'Vote for MLBB's Charismatic Queens!').\n"
        "    - **desc**: Poll description.\n"
        "    - **comment_count**: Number of comments.\n"
        "    - **ranking**: Array of ranked hero entries, each containing:\n"
        "        - **object**: Hero object ID.\n"
        "        - **title**: Hero name.\n"
        "        - **image**: Hero image URL.\n"
        "        - **image_big**: Larger hero image URL.\n"
        "        - **channel**: Array of channel IDs.\n"
        "        - **score**: Hero score value (e.g., '9.1').\n"
        "        - **score_total**: Total score points accumulated.\n"
        "        - **score_count**: Number of votes.\n"
        "        - **hot_comment**: Highlighted comment.\n"
        "        - **hashtags**: Optional hashtags associated with the poll.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying community-driven hero ratings.\n"
        "- Tracking popularity trends.\n"
        "- Surfacing thematic polls such as 'Most Charismatic Hero' or 'Top Jungler'."
    ),
)
def heroes_ratings(
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    return fetch_ratings_all(lang)


@router.get(
    path="/heroes/ratings/{subject}",
    summary="Hero Ratings by Subject",
    description=(
        "Retrieve hero ratings for a specific subject from the ratings index. "
        "Supports query parameter for localization.\n\n"
        "Path parameters:\n"
        "- **subject**: Rating subject key from the ratings index response (7 characters).\n\n"
        "Query parameters:\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes hero rating data for the chosen subject:\n"
        "- **list**: Array of hero entries, each containing:\n"
        "    - **object**: Hero object ID.\n"
        "    - **title**: Hero name (e.g., 'Fanny').\n"
        "    - **image**: Hero image URL.\n"
        "    - **image_big**: Larger hero image URL.\n"
        "    - **channel**: Array of channel IDs.\n"
        "    - **score**: Hero score value (e.g., '8.8').\n"
        "    - **score_total**: Total score points accumulated.\n"
        "    - **score_count**: Number of votes.\n"
        "    - **hot_comment**: Highlighted community comment.\n"
        "    - **hashtags**: Optional hashtags associated with the poll.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying detailed ratings within a chosen poll or theme.\n"
        "- Allowing players to explore community sentiment.\n"
        "- Surfacing popularity for heroes in specific categories (e.g., 'Top Jungler', 'Most Charismatic Hero')."
    ),
)
def heroes_ratings_subject(
    subject: Annotated[
        str,
        Path(
            title="Rating Subject",
            description="Rating subject ID from the ratings index response.",
            min_length=7,
            max_length=7,
        )
    ],
    lang: Annotated[
        LanguageEnum,
        Query(
            title="Language",
            description="Language code for localized content.",
        )
    ] = LanguageEnum.ENGLISH
) -> object:
    return fetch_ratings_subject(lang, subject)
