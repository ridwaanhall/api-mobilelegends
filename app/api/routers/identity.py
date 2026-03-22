

from fastapi import APIRouter, Body, Depends, Query
from app.api.dependencies import require_api_available
from app.services.identity import (
	fetch_login_service,
	fetch_vc_service,
	fetch_user_service,
	fetch_logout_service,
)
from app.core.param_descriptions import *

from typing import Annotated

from app.core.enums import LanguageEnum

router = APIRouter(prefix="/api/identity", tags=["identity"], dependencies=[Depends(require_api_available)])

@router.post(
    path="/send-vc",
    summary="Send verification Code",
    description="Verification code will be sent in-game.",
)
def send_vc(
	role_id: Annotated[
		int,
		Body(
			title="Role ID",
			description="The role ID of the player",
			embed=True
		)
	],
	zone_id: Annotated[
		int,
		Body(
			title="Zone ID",
			description="The zone ID of the player",
			embed=True
		)
	],
) -> object:
	return fetch_vc_service("base/sendVc", role_id, zone_id)

@router.post(
    path="/login",
    summary="Login with verification code",
    description="Login to get JWT and token.",
)
def login(
	role_id: Annotated[
		int,
		Body(
			title="Role ID",
			description="The role ID of the player",
			embed=True
		)
	],
	zone_id: Annotated[
		int,
		Body(
			title="Zone ID",
			description="The zone ID of the player",
			embed=True
		)
	],
	vc: Annotated[
        int,
        Body(
            title="Verification Code",
            description="The verification code sent in-game",
            embed=True,
            min_length=4,
            max_length=4,
        )
    ],
) -> object:
	return fetch_login_service("base/login", role_id, zone_id, vc)

@router.post(
    path="/get-user-info", 
    summary="Get user info (needs JWT)",
    description="Get user info using JWT from /login response.",
)
def get_user_info(
    jwt: Annotated[
        str,
        Body(
            title="Authorization",
            description="JWT from /login response",
            embed=True
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
    return fetch_user_service("base/getBaseInfo", jwt, lang)

@router.post(
    path="/logout",
    summary="Logout (needs token)",
    description="Logout using JWT and token from /login response.",
)
def logout(
    jwt: Annotated[
        str,
        Body(
            title="Authorization",
            description="JWT from /login response",
            embed=True
        )
    ],
	token: Annotated[
        str,
        Body(
            title="Token",
            description="Token from /login response",
            embed=True
        )
    ]
) -> object:
	return fetch_logout_service("base/logout", jwt, token)
