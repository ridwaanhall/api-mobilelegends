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
    description="Send an in-game verification code to the player's account.",
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
    description="Authenticate the player using a verification code to obtain a JWT and session token.",
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
    description="Invalidate the player's session using the JWT and session token obtained from /login.",
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
    token: Annotated[
        str,
        Body(
            title="Session Token",
            description="The session token obtained from the /login endpoint.",
            embed=True,
        )
    ],
) -> object:
    headers = MLBBHeaderBuilder.get_user_header(
        jwt=jwt
    )
    payload = {
        "token": token,
    }
    return fetch_user_post("base/logout", headers, payload)


@router.post(
    path="/info",
    summary="User Info",
    description="Retrieve the authenticated player's base profile information using a valid JWT.",
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
    description="Retrieve the authenticated player's statistics information using a valid X-Token.",
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
    description="Retrieve the authenticated player's season information using a valid X-Token.",
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
    description="Retrieve the authenticated player's matches information using a valid X-Token.",
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
    description="Retrieve the authenticated player's match details using a valid X-Token.",
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
    description="Retrieve the authenticated player's frequent heroes information using a valid X-Token.",
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
