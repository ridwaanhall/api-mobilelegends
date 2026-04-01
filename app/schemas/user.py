from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class UserAuthBaseResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

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


class UserDataBaseResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    code: int
    data: Any
    msg: str | None = None
    message: str | None = None
    traceID: str | None = None


class UserInfoData(BaseModel):
    model_config = ConfigDict(extra="allow")

    avatar: str
    name: str
    level: int
    rank_level: int
    history_rank_level: int
    reg_country: str
    roleId: int
    zoneId: int


class UserInfoResponse(UserDataBaseResponse):
    data: UserInfoData


class UserEntity(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int
    n: str
    ix: str
    i2x: str


class UserStatHighlight(BaseModel):
    model_config = ConfigDict(extra="allow")

    v: int | float
    ts: int
    hid: int
    bid: int
    sid: int
    hid_e: UserEntity
    bid_s: str


class UserStatsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    wc: int
    tc: int
    as_score: float | None = Field(default=None, alias="as")
    gt: float
    mvpc: int
    wsc: int
    mo: UserStatHighlight
    hk: UserStatHighlight
    ma: UserStatHighlight
    ms: UserStatHighlight
    mdt: UserStatHighlight
    mg: UserStatHighlight
    mtd: UserStatHighlight
    sids: list[int]


class UserStatsResponse(UserDataBaseResponse):
    data: UserStatsData


class UserSeasonData(BaseModel):
    model_config = ConfigDict(extra="allow")

    sids: list[int]


class UserSeasonResponse(UserDataBaseResponse):
    data: UserSeasonData


class UserPageInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    nextCursor: str | int | None
    hasNext: bool
    count: int


class UserMatchSummary(BaseModel):
    model_config = ConfigDict(extra="allow")

    sid: int
    bid: int
    hid: int
    k: int
    d: int
    a: int
    lid: int
    s: int
    mvp: int
    res: int
    ts: int
    hid_e: UserEntity
    bid_s: str


class UserMatchesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    pageInfo: UserPageInfo
    result: list[UserMatchSummary]


class UserMatchesResponse(UserDataBaseResponse):
    data: UserMatchesData


class UserItemEntity(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int
    n: str
    ix: str
    i2x: str


class UserMatchDetailEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    f: int
    hid: int
    rid: int
    zid: int
    k: int
    d: int
    a: int
    tfr: float
    o: int
    op: float
    s: int
    mvp: int
    its: list[int]
    eq: int
    ts: int
    bd: int
    fk: int
    fw: int
    hid_e: UserEntity
    its_e: list[UserItemEntity | None]
    hlvl: int
    rname: str


class UserMatchDetailsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    result: list[UserMatchDetailEntry]


class UserMatchDetailsResponse(UserDataBaseResponse):
    data: UserMatchDetailsData


class UserFrequentHeroEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    hid: int
    tc: int
    wc: int
    bs: float
    mr: int
    mrp: float
    hid_e: UserEntity
    p: int


class UserFrequentHeroesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    pageInfo: UserPageInfo
    result: list[UserFrequentHeroEntry]


class UserFrequentHeroesResponse(UserDataBaseResponse):
    data: UserFrequentHeroesData


class UserFriendProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    rid: int
    zid: int
    n: str
    ax: str
    pri: bool


class UserFriendEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    f: UserFriendProfile
    frid: int
    fzid: int
    cl: int
    l: int
    tbc: int
    twc: int


class UserFriendsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    bfs: Any | None
    wfs: list[Any]
    fs: list[UserFriendEntry]


class UserFriendsResponse(UserDataBaseResponse):
    data: UserFriendsData
