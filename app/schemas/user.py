from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UserAuthBaseResponse(BaseModel):
    code: int
    msg: str


class UserAuthSimpleResponse(UserAuthBaseResponse):
    data: str


class UserLoginData(BaseModel):
    model_config = ConfigDict(extra="allow")

    jwt: str
    token: str
    roleid: int
    zoneid: int
    time: int


class UserLoginResponse(UserAuthBaseResponse):
    data: UserLoginData
