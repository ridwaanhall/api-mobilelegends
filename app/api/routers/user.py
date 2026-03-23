from fastapi import APIRouter, Body, Depends, Path, Query

from app.api.dependencies import require_api_available

from app.services.user import fetch_user_post, fetch_user_actgateway

from app.core.http import MLBBHeaderBuilder
from app.core.param_descriptions import *
from app.core.enums import LanguageEnum

from typing import Annotated

router = APIRouter(prefix="/api/user", tags=["user"], dependencies=[Depends(require_api_available)])


@router.post(
    path="/auth/send-vc",
    summary="Send Verification Code",
    description=(
        "Send an in-game verification code to the player's account. "
        "Requires a JSON body with `role_id` (player role identifier) and `zone_id` (server zone identifier). "
        "The response confirms whether the verification code was successfully dispatched. "
        "Useful for account authentication flows, linking user identity, and validating ownership of a game account."
    ),
)
def send_vc(
    role_id: Annotated[
        int,
        Body(
            title="Role ID",
            description="The unique role ID of the player's account.",
            embed=True,
        )
    ],
    zone_id: Annotated[
        int,
        Body(
            title="Zone ID",
            description="The zone ID associated with the player's server region.",
            embed=True,
        )
    ],
) -> object:
    headers = MLBBHeaderBuilder.get_user_header()
    payload = {
        "roleId": role_id,
        "zoneId": zone_id,
    }
    return fetch_user_post("base/sendVc", headers, payload)


@router.post(
    path="/auth/login",
    summary="Login with Verification Code",
    description=(
        "Authenticate the player using a verification code to obtain a JWT and session token. "
        "Requires a JSON body with `role_id` (player role identifier), `zone_id` (server zone identifier), "
        "and `vc` (verification code). "
        "The response includes authentication details such as JWT, session token, role ID, zone ID, and metadata "
        "like time and module information. "
        "Useful for completing account login flows, establishing secure sessions, and enabling authorized access "
        "to user-specific resources."
    ),
)
def login(
    role_id: Annotated[
        int,
        Body(
            title="Role ID",
            description="The unique role ID of the player's account.",
            embed=True,
        )
    ],
    zone_id: Annotated[
        int,
        Body(
            title="Zone ID",
            description="The zone ID associated with the player's server region.",
            embed=True,
        )
    ],
    vc: Annotated[
        int,
        Body(
            title="Verification Code",
            description="The 4-digit verification code received in-game via the send-vc endpoint.",
            embed=True,
        )
    ],
) -> object:
    headers = MLBBHeaderBuilder.get_user_header()
    payload = {
        "roleId": role_id,
        "zoneId": zone_id,
        "vc": vc,
        "referer": "academy",
        "type": "web",
    }
    return fetch_user_post("base/login", headers, payload)


@router.post(
    path="/auth/logout",
    summary="Logout",
    description=(
        "Invalidate the player's session using the JWT obtained from `/api/user/auth/login`. "
        "This endpoint terminates the current authenticated session, ensuring that the JWT can no longer be used "
        "for authorized requests.\n\n"
        "Request body:\n"
        "- **jwt**: JSON Web Token obtained during login.\n\n"
        "The response confirms whether the logout was successful:\n"
        "- **code**: Status code (0 indicates success).\n"
        "- **data**: Empty string (no payload returned).\n"
        "- **msg**: Message string (e.g., 'ok').\n\n"
        "Note: Although the login response also includes a `token` field, only the JWT is required for logout. "
        "The server uses the JWT to invalidate the session."
    ),
)
def logout(
    jwt: Annotated[
        str,
        Body(
            title="JWT",
            description="The JWT obtained from the /login endpoint.",
            embed=True,
        )
    ],
) -> object:
    headers = MLBBHeaderBuilder.get_user_header(
        jwt=jwt
    )
    payload = {}
    return fetch_user_post("base/logout", headers, payload)


@router.post(
    path="/info",
    summary="User Info",
    description=(
        "Retrieve the authenticated player's base profile information using a valid JWT. "
        "Supports query parameter for localization (`lang`). "
        "Requires a JSON body containing `jwt` (JSON Web Token obtained from login). "
        "The response includes player details such as avatar URL, display name, level, rank level, "
        "historical rank level, registered country, role ID, and zone ID. "
        "Useful for displaying identity card information, verifying account ownership, "
        "and populating player profile data in client applications."
    ),
)
def user_info(
    jwt: Annotated[
        str,
        Body(
            title="JWT",
            description="The JWT obtained from the /login endpoint.",
            embed=True,
        )
    ],
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH,
) -> object:
    headers = MLBBHeaderBuilder.get_user_header(
        lang=lang,
        x_actid="2728785",
        x_appid="2713644",
        jwt=jwt
    )
    payload = {}
    return fetch_user_post("base/getBaseInfo", headers, payload)


@router.post(
    path="/stats",
    summary="User Statistics",
    description=(
        "Retrieve the authenticated player's statistics information using a valid JWT. "
        "Supports query parameter for localization (`lang`). "
        "Requires a JSON body containing `jwt` (JSON Web Token obtained from login). "
        "The response includes general player stats and hero-specific highlights:\n\n"
        "- **wc**: Win Count (total matches won)\n"
        "- **tc**: Total Count (total matches played)\n"
        "- **as**: Average Score (overall performance rating)\n"
        "- **gt**: Game Time (average match duration in minutes)\n"
        "- **mvpc**: MVP Count (number of times player earned MVP)\n"
        "- **wsc**: Win Streak Count (longest consecutive wins)\n\n"
        "Hero-specific highlights:\n"
        "- **mo**: Most Often (hero most frequently used)\n"
        "- **hk**: Highest Kills (hero with the most kills)\n"
        "- **ma**: Most Assists (hero contributing the most assists)\n"
        "- **ms**: Most Score (hero with the highest accumulated score)\n"
        "- **mdt**: Most Damage Taken (hero absorbing the most damage)\n"
        "- **mg**: Most Gold (hero earning the most gold)\n"
        "- **mtd**: Most Total Damage (hero dealing the most damage overall)\n\n"
        "Each hero highlight includes metadata such as hero ID, name, images, battle ID, and timestamp. "
        "Useful for analyzing overall player performance, identifying favorite heroes, and showcasing "
        "personal achievements in MLBB."
    ),
)
def user_stats(
    jwt: Annotated[
        str,
        Body(
            title="JWT",
            description="The JWT obtained from the /login endpoint.",
            embed=True,
        )
    ],
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH,
) -> object:
    headers = MLBBHeaderBuilder.get_user_header(
        lang=lang,
        x_token=jwt,
    )
    params = {}
    return fetch_user_actgateway("battlereport/stats", headers, params)


@router.post(
    path="/season",
    summary="User Season List",
    description=(
        "Retrieve the authenticated player's season information using a valid JWT. "
        "Supports query parameter for localization (`lang`). "
        "Requires a JSON body containing `jwt` (JSON Web Token obtained from login). "
        "The response includes a list of season identifiers (`sids`) representing the seasons "
        "in which the player has participated or has tracked statistics. "
        "Useful for displaying season history, linking performance data to specific seasons, "
        "and enabling clients to fetch season-specific stats or achievements."
    ),
)
def user_season(
    jwt: Annotated[
        str,
        Body(
            title="JWT",
            description="The JWT obtained from the /login endpoint.",
            embed=True,
        )
    ],
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH,
) -> object:
    headers = MLBBHeaderBuilder.get_user_header(
        lang=lang,
        x_token=jwt,
    )
    params = {}
    return fetch_user_actgateway("battlereport/season/list", headers, params)


@router.post(
    path="/match",
    summary="User Matches",
    description=(
        "Retrieve the authenticated player's recent matches information using a valid JWT. "
        "Supports query parameters:\n"
        "- **sid**: Season ID for filtering matches (use `0` for all seasons, or specific IDs from `/api/user/season`).\n"
        "- **limit**: Maximum number of matches to retrieve (minimum 1).\n"
        "- **last_cursor**: Cursor for pagination. This value must be set to the `bid_s` of the last match "
        "from the previous page. The API response includes `pageInfo.nextCursor`, which corresponds to the `bid_s` "
        "of the last item in the current result set. Use that value as `last_cursor` in the next request to fetch "
        "the following page.\n"
        "- **lang**: Language code for localized content.\n\n"
        "Requires a JSON body containing `jwt` (JSON Web Token obtained from login).\n\n"
        "The response includes match details:\n"
        "- **sid**: Season ID.\n"
        "- **bid**: Battle ID (unique match reference).\n"
        "- **hid**: Hero ID used in the match.\n"
        "- **k**: Kills.\n"
        "- **d**: Deaths.\n"
        "- **a**: Assists.\n"
        "- **lid**: Lane ID (1 EXP, 2 Mid, 3 Roam, 4 Jungle, 5 Gold).\n"
        "- **s**: Score (performance rating for the match).\n"
        "- **mvp**: MVP flag (1 if MVP, 0 otherwise).\n"
        "- **res**: Result (1 = Win, 0 = Loss).\n"
        "- **ts**: Timestamp of the match.\n"
        "- **hid_e**: Hero entity metadata (hero ID, name, images).\n"
        "- **bid_s**: Short battle ID (used for pagination cursor).\n\n"
        "Pagination example:\n"
        "1. First request: `/api/user/match?sid=40&limit=10&lang=en` → response includes `pageInfo.nextCursor = 4139649383291049463`.\n"
        "2. Second request: `/api/user/match?sid=40&limit=10&last_cursor=4139649383291049463&lang=en` → retrieves the next page, "
        "starting from the match with `bid_s = 4139649383291049463`.\n\n"
        "This mechanism ensures reliable sequential pagination through a player's match history."
    ),
)
def user_match(
    jwt: Annotated[
        str,
        Body(
            title="JWT",
            description="The JWT obtained from the /login endpoint.",
            embed=True,
        )
    ],
    sid: Annotated[
        int,
        Query(
            title="Season ID",
            description="The season ID for filtering recent matches. Use 0 for all seasons.",
        )
    ],
    limit: Annotated[
        int,
        Query(
            title="Limit",
            description="The maximum number of recent matches to retrieve.",
            ge=1,
        )
    ] = 10,
    last_cursor: Annotated[
        int | None,
        Query(
            title="Last Cursor",
            description="The cursor for pagination to retrieve the next set of recent matches. (bid_s)",
        )
    ] = None,
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH,
) -> object:
    headers = MLBBHeaderBuilder.get_user_header(
        lang=lang,
        x_token=jwt,
    )
    params = {
        "sid": sid,
        "limit": limit,
    }
    if last_cursor is not None:
        params["last_cursor"] = last_cursor

    return fetch_user_actgateway("battlereport/matches/recent", headers, params)


@router.post(
    path="/match/{match_id}",
    summary="User Match Details",
    description=(
        "Retrieve the authenticated player's detailed match information using a valid JWT. "
        "Supports query parameters:\n"
        "- **match_id**: Unique identifier of the match (from `bid_s` in `/api/user/match`).\n"
        "- **sid**: Season ID for filtering (from `/api/user/season`).\n"
        "- **lang**: Language code for localized content.\n\n"
        "Requires a JSON body containing `jwt` (JSON Web Token obtained from login).\n\n"
        "The response includes per-player match details:\n"
        "- **f**: Team flag (1 = Team A, 2 = Team B).\n"
        "- **hid**: Hero ID used in the match.\n"
        "- **rid**: Role ID (unique player identifier).\n"
        "- **zid**: Zone ID (server region).\n"
        "- **k**: Kills.\n"
        "- **d**: Deaths.\n"
        "- **a**: Assists.\n"
        "- **tfr**: Team Fight Rate (contribution ratio in team fights).\n"
        "- **o**: Output (total damage dealt).\n"
        "- **op**: Output Percentage (damage contribution relative to team).\n"
        "- **s**: Score (performance rating).\n"
        "- **mvp**: MVP flag (1 if MVP, 0 otherwise).\n"
        "- **its**: Item IDs equipped during the match.\n"
        "- **its_e**: Item entity metadata (name, image, etc.).\n"
        "- **eq**: Equipment slot indicator.\n"
        "- **ts**: Timestamp of the match.\n"
        "- **bd**: Battle duration (seconds).\n"
        "- **fk**: First Kill flag (number of first kills).\n"
        "- **fw**: First Win flag (1 if team achieved first objective win).\n"
        "- **hid_e**: Hero entity metadata (hero ID, name, images).\n"
        "- **hlvl**: Hero level reached in the match.\n"
        "- **rname**: Role name (e.g., 'ジャングラー', 'Pertaliteee').\n\n"
        "This endpoint provides a full breakdown of each participant in the match, including "
        "their hero choice, performance stats (kills, deaths, assists, damage), items built, "
        "and role assignment. Useful for reconstructing match history, analyzing team compositions, "
        "and evaluating player performance in detail."
    ),
)
def user_match_details(
    match_id: Annotated[
        int,
        Path(
            title="Match ID",
            description="The unique identifier of the match to retrieve details for.",
        )
    ],
    jwt: Annotated[
        str,
        Body(
            title="JWT",
            description="The JWT obtained from the /login endpoint.",
            embed=True,
        )
    ],
    sid: Annotated[
        int,
        Query(
            title="Season ID",
            description="The season ID for filtering recent matches.",
        )
    ],
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH,
) -> object:
    headers = MLBBHeaderBuilder.get_user_header(
        lang=lang,
        x_token=jwt,
    )
    params = {
        "sid": sid
    }
    return fetch_user_actgateway(f"battlereport/matches/{match_id}", headers, params)


@router.post(
    path="/heros/frequent",
    summary="User Frequent Heroes",
    description=(
        "Retrieve the authenticated player's frequent heroes information using a valid JWT. "
        "Supports query parameters:\n"
        "- **sid**: Season ID for filtering frequent heroes (must be a valid season ID from `/api/user/season`).\n"
        "- **limit**: Maximum number of heroes to retrieve (minimum 1).\n"
        "- **last_cursor**: Cursor for pagination. This value must be set to the `hid` (hero_id) of the last hero "
        "from the previous page. The API response includes `pageInfo.nextCursor`, which corresponds to the hero_id "
        "of the first hero in the next page. Use that value as `last_cursor` in the next request to fetch subsequent heroes.\n"
        "- **lang**: Language code for localized content.\n\n"
        "Requires a JSON body containing `jwt` (JSON Web Token obtained from login).\n\n"
        "The response includes frequent hero usage details:\n"
        "- **hid**: Hero ID.\n"
        "- **tc**: Total Count (number of matches played with this hero).\n"
        "- **wc**: Win Count (number of matches won with this hero).\n"
        "- **bs**: Battle Score (average performance rating).\n"
        "- **mr**: Match Rating (accumulated rating points).\n"
        "- **mrp**: Match Rating Percentage (rating contribution relative to overall performance).\n"
        "- **hid_e**: Hero entity metadata (hero ID, name, images).\n"
        "- **p**: Power score (weighted performance index for ranking frequent heroes).\n\n"
        "Pagination example:\n"
        "1. First request: `/api/user/heros/frequent?sid=37&limit=5&lang=en` → response includes `pageInfo.nextCursor = 11`.\n"
        "2. Second request: `/api/user/heros/frequent?sid=37&limit=5&last_cursor=11&lang=en` → retrieves the next page, "
        "starting from the hero with `hid = 11`.\n\n"
        "This endpoint is useful for analyzing which heroes a player uses most often, their win rates, and performance scores "
        "across different seasons."
    ),
)
def user_frequent_heros(
    jwt: Annotated[
        str,
        Body(
            title="JWT",
            description="The JWT obtained from the /login endpoint.",
            embed=True,
        )
    ],
    sid: Annotated[
        int,
        Query(
            title="Season ID",
            description="The season ID for filtering frequent heroes. Use 0 for all seasons.",
        )
    ],
    limit: Annotated[
        int,
        Query(
            title="Limit",
            description="The maximum number of frequent heroes to retrieve.",
            ge=1,
        )
    ] = 5,
    last_cursor: Annotated[
        int | None,
        Query(
            title="Last Cursor",
            description="The cursor for pagination to retrieve the next set of frequent heroes. (hero_id)",
        )
    ] = None,
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH,
) -> object:
    headers = MLBBHeaderBuilder.get_user_header(
        lang=lang,
        x_token=jwt,
    )
    params = {
        "sid": sid,
        "limit": limit,
    }
    if last_cursor is not None:
        params["last_cursor"] = last_cursor

    return fetch_user_actgateway("battlereport/heros/frequent", headers, params)


@router.post(
    path="/friends",
    summary="User Friends",
    description=(
        "Retrieve the authenticated player's friends information using a valid JWT. "
        "Supports query parameters:\n"
        "- **sid**: Season ID for filtering friends (must be a valid season ID from `/api/user/season`).\n"
        "- **lang**: Language code for localized content.\n\n"
        "Requires a JSON body containing `jwt` (JSON Web Token obtained from login).\n\n"
        "The response includes friend statistics and metadata:\n"
        "- **bfs**: Best Friends (highlighted or prioritized friends list, may be null).\n"
        "- **wfs**: Weekly Friends (friends interacted with recently, may be empty).\n"
        "- **fs**: Friends list entries, each containing:\n"
        "   - **f**: Friend object with identifiers:\n"
        "       - **rid**: Role ID (unique player identifier).\n"
        "       - **zid**: Zone ID (server region).\n"
        "       - **n**: Name (may be empty if private).\n"
        "       - **ax**: Avatar URL (may be empty).\n"
        "       - **pri**: Privacy flag (true if details are hidden).\n"
        "   - **frid**: Friend Role ID (unique identifier for the friend).\n"
        "   - **fzid**: Friend Zone ID (server region for the friend).\n"
        "   - **cl**: Current Level of the friend.\n"
        "   - **l**: Level (same as cl, sometimes duplicated).\n"
        "   - **tbc**: Total Battle Count (matches played together).\n"
        "   - **twc**: Total Win Count (matches won together).\n\n"
        "This endpoint is useful for displaying a player's friend list, tracking shared match history, "
        "and analyzing cooperative performance with friends across different seasons."
    ),
)
def user_friends(
    jwt: Annotated[
        str,
        Body(
            title="JWT",
            description="The JWT obtained from the /login endpoint.",
            embed=True,
        )
    ],
    sid: Annotated[
        int,
        Query(
            title="Season ID",
            description="The season ID for filtering friends.",
        )
    ],
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH,
) -> object:
    headers = MLBBHeaderBuilder.get_user_header(
        lang=lang,
        x_token=jwt,
    )
    params = {
        "sid": sid,
    }

    return fetch_user_actgateway("battlereport/friends", headers, params)