from fastapi import APIRouter, Body, Depends, Query

from app.api.dependencies import require_api_available

from app.services.identity import fetch_identity_post, fetch_identity_actgateway

from app.core.http import MLBBHeaderBuilder
from app.core.param_descriptions import *
from app.core.enums import LanguageEnum

from typing import Annotated

router = APIRouter(prefix="/api/identity", tags=["identity"], dependencies=[Depends(require_api_available)])


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
    payload = {
        "roleId": role_id,
        "zoneId": zone_id,
    }
    headers = MLBBHeaderBuilder.get_identity_header()
    return fetch_identity_post("base/sendVc", payload, headers)


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
    payload = {
        "roleId": role_id,
        "zoneId": zone_id,
        "vc": vc,
        "referer": "academy",
        "type": "web",
    }
    headers = MLBBHeaderBuilder.get_identity_header()
    return fetch_identity_post("base/login", payload, headers)


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
    payload = {
        "token": token,
    }
    headers = MLBBHeaderBuilder.get_identity_header(
        jwt=jwt
    )
    return fetch_identity_post("base/logout", payload, headers)


@router.post(
    path="/user-info",
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
    payload = {}
    headers = MLBBHeaderBuilder.get_identity_header(
        lang=lang,
        x_actid="2728785",
        x_appid="2713644",
        jwt=jwt
    )
    return fetch_identity_post("base/getBaseInfo", payload, headers)


@router.post(
    path="/user-stats",
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
    headers = MLBBHeaderBuilder.get_identity_header(
        lang=lang,
        x_token=jwt,
    )
    payload = {}
    params = {}
    return fetch_identity_actgateway("battlereport/stats", headers, payload, params)


@router.post(
    path="/user-season",
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
    headers = MLBBHeaderBuilder.get_identity_header(
        lang=lang,
        x_token=jwt,
    )
    payload = {}
    params = {}
    return fetch_identity_actgateway("battlereport/season/list", headers, payload, params)


@router.post(
    path="/user-matches-recent",
    summary="User Recent Matches",
    description="Retrieve the authenticated player's recent matches information using a valid X-Token.",
)
def user_recent_matches(
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
    lang: Annotated[
        LanguageEnum,
        Query(
            title=TITLE_LANGUAGE,
            description=DESCRIPTION_LANGUAGE,
        )
    ] = LanguageEnum.ENGLISH,
) -> object:
    headers = MLBBHeaderBuilder.get_identity_header(
        lang=lang,
        x_token=jwt,
    )
    payload = {}
    params = {
        "sid": sid,
        "limit": limit,
    }
    return fetch_identity_actgateway("battlereport/matches/recent", headers, payload, params)