from fastapi import APIRouter, Body, Depends, Path, Query

from app.api.dependencies import require_api_available

from app.services.user import fetch_user_post, fetch_user_actgateway

from app.core.http import MLBBHeaderBuilder
from app.core.enums import LanguageEnum

from typing import Annotated

router = APIRouter(prefix="/api/user", tags=["user"], dependencies=[Depends(require_api_available)])


@router.post(
    path="/auth/send-vc",
    name="api.user.send_verification_code",
    summary="Send Verification Code",
    description=(
        "Send an in-game verification code to the player's account, valid for 5 mins. "
        "This endpoint is part of the authentication flow and is used to validate ownership of a game account.\n\n"
        "Request body:\n"
        "- **role_id**: Player role identifier (Game ID).\n"
        "- **zone_id**: Server zone identifier (Server ID).\n\n"
        "The response confirms whether the verification code was successfully dispatched:\n"
        "- **code**: Status code (0 indicates success).\n"
        "- **data**: Empty string (no payload returned).\n"
        "- **msg**: Message string (e.g., 'ok').\n\n"
        "Useful for account authentication flows, linking user identity, and validating account ownership."
    ),
)
def send_vc(
    role_id: Annotated[
        int,
        Body(
            title="Role ID",
            description="The unique role ID of the player's account. (Game ID)",
            embed=True,
        )
    ],
    zone_id: Annotated[
        int,
        Body(
            title="Zone ID",
            description="The zone ID associated with the player's server region. (Server ID)",
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
    name="api.user.login",
    summary="Login with Verification Code",
    description=(
        "Authenticate the player using a verification code to obtain a JWT and session token. "
        "This endpoint completes the account login flow, establishes a secure session, and enables authorized access "
        "to user-specific resources.\n\n"
        "Request body:\n"
        "- **role_id**: Player role identifier.\n"
        "- **zone_id**: Server zone identifier.\n"
        "- **vc**: Verification code sent to the player via in-game mail, valid 5 mins.\n\n"
        "The response includes authentication details:\n"
        "- **code**: Status code (0 indicates success).\n"
        "- **data.jwt**: JSON Web Token used for subsequent authenticated requests.\n"
        "- **data.token**: Session token string.\n"
        "- **data.roleid**: Player role ID.\n"
        "- **data.zoneid**: Player zone ID.\n"
        "- **data.time**: Timestamp of login.\n"
        "- **data.module, name, email, mobile, open_id**: Metadata fields (may be empty depending on account).\n\n"
        "The response confirms successful login and provides the credentials required for accessing other user endpoints."
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
            description="The 4-digit verification code, obtained through in-game mail via the send-vc endpoint, remains valid for 5 minutes.",
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
    name="api.user.logout",
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
    name="api.user.info",
    summary="User Info",
    description=(
        "Retrieve the authenticated player's base profile information using a valid JWT. "
        "Supports query parameter for localization (`lang`). Requires a JSON body containing `jwt` "
        "(JSON Web Token obtained from login).\n\n"
        "Request body:\n"
        "- **jwt**: JSON Web Token obtained during login.\n\n"
        "Query parameters:\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes player details:\n"
        "- **avatar**: Avatar image URL.\n"
        "- **name**: Display name.\n"
        "- **level**: Current player level.\n"
        "- **rank_level**: Current rank level.\n"
        "- **history_rank_level**: Highest historical rank level.\n"
        "- **reg_country**: Registered country code.\n"
        "- **roleId**: Player role identifier.\n"
        "- **zoneId**: Server zone identifier.\n\n"
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
            title="Language",
            description="Language code for localized content.",
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
    name="api.user.stats",
    summary="User Statistics",
    description=(
        "Retrieve the authenticated player's overall statistics using a valid JWT. "
        "Supports query parameter for localization (`lang`). Requires a JSON body containing `jwt` "
        "(JSON Web Token obtained from login).\n\n"
        "Request body:\n"
        "- **jwt**: JSON Web Token obtained during login.\n\n"
        "Query parameters:\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes general player statistics:\n"
        "- **wc**: Win Count (total matches won).\n"
        "- **tc**: Total Count (total matches played).\n"
        "- **as**: Average Score (overall performance rating).\n"
        "- **gt**: Game Time (average match duration in minutes).\n"
        "- **mvpc**: MVP Count (number of times player earned MVP).\n"
        "- **wsc**: Win Streak Count (longest consecutive wins).\n\n"
        "Hero-specific highlights:\n"
        "- **mo**: Most Often (hero most frequently used).\n"
        "- **hk**: Highest Kills (hero with the most kills).\n"
        "- **ma**: Most Assists (hero contributing the most assists).\n"
        "- **ms**: Most Score (hero with the highest accumulated score).\n"
        "- **mdt**: Most Damage Taken (hero absorbing the most damage).\n"
        "- **mg**: Most Gold (hero earning the most gold).\n"
        "- **mtd**: Most Total Damage (hero dealing the most damage overall).\n\n"
        "Each hero highlight includes metadata such as:\n"
        "    - **hid**: Hero ID.\n"
        "    - **n**: Hero name.\n"
        "    - **ix**: Hero image URL.\n"
        "    - **i2x**: Alternate hero image URL.\n"
        "    - **bid**: Battle ID reference.\n"
        "    - **ts**: Timestamp of the highlight.\n\n"
        "This endpoint is useful for:\n"
        "- Analyzing overall player performance.\n"
        "- Identifying favorite heroes.\n"
        "- Showcasing personal achievements in MLBB."
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
            title="Language",
            description="Language code for localized content.",
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
    name="api.user.season",
    summary="User Season List",
    description=(
        "Retrieve the authenticated player's season information using a valid JWT. "
        "Supports query parameter for localization (`lang`). Requires a JSON body containing `jwt` "
        "(JSON Web Token obtained from login).\n\n"
        "Request body:\n"
        "- **jwt**: JSON Web Token obtained during login.\n\n"
        "Query parameters:\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes:\n"
        "- **sids**: List of season identifiers representing the seasons in which the player has participated "
        "or has tracked statistics.\n\n"
        "This endpoint is useful for:\n"
        "- Displaying season history.\n"
        "- Linking performance data to specific seasons.\n"
        "- Enabling clients to fetch season-specific stats or achievements."
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
            title="Language",
            description="Language code for localized content.",
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
    path="/matches",
    name="api.user.matches",
    summary="User Matches",
    description=(
        "Retrieve the authenticated player's recent matches information using a valid JWT. "
        "Supports query parameters for season filtering, pagination, and localization. Requires a JSON body containing `jwt` "
        "(JSON Web Token obtained from login).\n\n"
        "Request body:\n"
        "- **jwt**: JSON Web Token obtained during login.\n\n"
        "Query parameters:\n"
        "- **sid**: Season ID for filtering matches (must be a valid season ID from `/api/user/season`).\n"
        "- **limit**: Maximum number of matches to retrieve (minimum: 1).\n"
        "- **last_cursor**: Cursor for pagination. Must be set to the `bid_s` of the last match from the previous page. "
        "The API response includes `pageInfo.nextCursor`, which corresponds to the `bid_s` of the last item in the current result set. "
        "Use that value as `last_cursor` in the next request to fetch the following page.\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
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
        "    First request: `/api/user/matches?sid=40&limit=10&lang=en` → response includes `pageInfo.nextCursor = 4139649383291049463`.\n"
        "    Second request: `/api/user/matches?sid=40&limit=10&last_cursor=4139649383291049463&lang=en` → retrieves the next page, "
        "starting from the match with `bid_s = 4139649383291049463`.\n\n"
        "The response also includes pagination metadata:\n"
        "- **pageInfo.nextCursor**: Cursor value for the next page.\n"
        "- **pageInfo.hasNext**: Boolean flag indicating if more results are available.\n"
        "- **pageInfo.count**: Number of results returned in the current page.\n\n"
        "This endpoint is useful for:\n"
        "- Reconstructing match history.\n"
        "- Analyzing player performance.\n"
        "- Enabling clients to paginate reliably through a player's matches."
    ),
)
def user_matches(
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
            title="Language",
            description="Language code for localized content.",
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
    path="/matches/{match_id}",
    name="api.user.match_details",
    summary="User Match Details",
    description=(
        "Retrieve the authenticated player's detailed match information using a valid JWT. "
        "Supports query parameters for season filtering and localization. Requires a JSON body containing `jwt` "
        "(JSON Web Token obtained from login).\n\n"
        "Request body:\n"
        "- **jwt**: JSON Web Token obtained during login.\n\n"
        "Path parameters:\n"
        "- **match_id**: Unique identifier of the match (from `bid_s` in `/api/user/matches`).\n\n"
        "Query parameters:\n"
        "- **sid**: Season ID for filtering (must be a valid season ID from `/api/user/season`).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
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
        "- **its_e**: Item entity metadata:\n"
        "    - **id**: Item ID.\n"
        "    - **n**: Item name.\n"
        "    - **ix**: Item image URL.\n"
        "    - **i2x**: Alternate item image URL.\n"
        "- **eq**: Equipment slot indicator.\n"
        "- **ts**: Timestamp of the match.\n"
        "- **bd**: Battle duration (seconds).\n"
        "- **fk**: First Kill flag (number of first kills).\n"
        "- **fw**: First Win flag (1 if team achieved first objective win).\n"
        "- **hid_e**: Hero entity metadata:\n"
        "    - **id**: Hero ID.\n"
        "    - **n**: Hero name.\n"
        "    - **ix**: Hero image URL.\n"
        "    - **i2x**: Alternate hero image URL.\n"
        "- **hlvl**: Hero level reached in the match.\n"
        "- **rname**: Role name (localized string, e.g., 'ジャングラー').\n\n"
        "This endpoint provides a full breakdown of each participant in the match, including:\n"
        "    - Hero choice.\n"
        "    - Performance stats (kills, deaths, assists, damage).\n"
        "    - Items built with metadata.\n"
        "    - Role assignment and team contribution.\n\n"
        "It is useful for:\n"
        "    - Reconstructing match history.\n"
        "    - Analyzing team compositions.\n"
        "    - Evaluating player performance in detail."
    ),
)
def user_matches_details(
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
            title="Language",
            description="Language code for localized content.",
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
    path="/heroes/frequent",
    name="api.user.frequent_heroes",
    summary="User Frequent Heroes",
    description=(
        "Retrieve the authenticated player's frequent heroes information using a valid JWT. "
        "Supports query parameters for season filtering, pagination, and localization. Requires a JSON body containing `jwt` "
        "(JSON Web Token obtained from login).\n\n"
        "Request body:\n"
        "- **jwt**: JSON Web Token obtained during login.\n\n"
        "Query parameters:\n"
        "- **sid**: Season ID for filtering frequent heroes (must be a valid season ID from `/api/user/season`).\n"
        "- **limit**: Maximum number of heroes to retrieve (minimum: 1).\n"
        "- **last_cursor**: Cursor for pagination. Must be set to the `hid` (hero_id) of the last hero from the previous page. "
        "The API response includes `pageInfo.nextCursor`, which corresponds to the hero_id of the first hero in the next page. "
        "Use that value as `last_cursor` in the next request to fetch subsequent heroes.\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes frequent hero usage details:\n"
        "- **hid**: Hero ID.\n"
        "- **tc**: Total Count (number of matches played with this hero).\n"
        "- **wc**: Win Count (number of matches won with this hero).\n"
        "- **bs**: Battle Score (average performance rating).\n"
        "- **mr**: Match Rating (accumulated rating points).\n"
        "- **mrp**: Match Rating Percentage (rating contribution relative to overall performance).\n"
        "- **hid_e**: Hero entity metadata:\n"
        "    - **id**: Hero ID.\n"
        "    - **n**: Hero name.\n"
        "    - **ix**: Hero image URL.\n"
        "    - **i2x**: Alternate hero image URL.\n"
        "- **p**: Power score (weighted performance index for ranking frequent heroes).\n\n"
        "Pagination example:\n"
        "    First request: `/api/user/heroes/frequent?sid=37&limit=5&lang=en` → response includes `pageInfo.nextCursor = 11`.\n"
        "    Second request: `/api/user/heroes/frequent?sid=37&limit=5&last_cursor=11&lang=en` → retrieves the next page, "
        "starting from the hero with `hid = 11`.\n\n"
        "The response also includes pagination metadata:\n"
        "- **pageInfo.nextCursor**: Cursor value for the next page.\n"
        "- **pageInfo.hasNext**: Boolean flag indicating if more results are available.\n"
        "- **pageInfo.count**: Number of results returned in the current page.\n\n"
        "This endpoint is useful for:\n"
        "- Analyzing which heroes a player uses most often.\n"
        "- Tracking win rates and performance scores.\n"
        "- Comparing hero usage across different seasons."
    ),
)
def user_frequent_heroes(
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
            title="Language",
            description="Language code for localized content.",
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
    name="api.user.friends",
    summary="User Friends",
    description=(
        "Retrieve the authenticated player's friends information using a valid JWT. "
        "Supports query parameters for season filtering and localization. Requires a JSON body containing `jwt` "
        "(JSON Web Token obtained from login).\n\n"
        "Request body:\n"
        "- **jwt**: JSON Web Token obtained during login.\n\n"
        "Query parameters:\n"
        "- **sid**: Season ID for filtering friends (must be a valid season ID from `/api/user/season`).\n"
        "- **lang**: Language code for localized content (default: `en`).\n\n"
        "The response includes friend statistics and metadata:\n"
        "- **bfs**: Best Friends (highlighted or prioritized friends list, may be null).\n"
        "- **wfs**: Weekly Friends (friends interacted with recently, may be empty).\n"
        "- **fs**: Friends list entries, each containing:\n"
        "    - **f**: Friend object with identifiers:\n"
        "        - **rid**: Role ID (unique player identifier).\n"
        "        - **zid**: Zone ID (server region).\n"
        "        - **n**: Name (may be empty if private).\n"
        "        - **ax**: Avatar URL (may be empty).\n"
        "        - **pri**: Privacy flag (true if details are hidden).\n"
        "    - **frid**: Friend Role ID (unique identifier for the friend).\n"
        "    - **fzid**: Friend Zone ID (server region for the friend).\n"
        "    - **cl**: Current Level of the friend.\n"
        "    - **l**: Level (same as cl, sometimes duplicated).\n"
        "    - **tbc**: Total Battle Count (matches played together).\n"
        "    - **twc**: Total Win Count (matches won together).\n\n"
        "This endpoint is useful for:\n"
        "- Displaying a player's friend list.\n"
        "- Tracking shared match history.\n"
        "- Analyzing cooperative performance with friends across different seasons."
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
            title="Language",
            description="Language code for localized content.",
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