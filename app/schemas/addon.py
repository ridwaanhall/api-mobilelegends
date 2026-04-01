from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class AddonWinRateResponse(BaseModel):
	model_config = ConfigDict(extra="allow")

	status: str
	match_now: int
	wr_now: float
	wr_future: float
	required_no_lose_matches: int
	message: str


class AddonIpData(BaseModel):
	model_config = ConfigDict(extra="allow")

	city: str
	state: str
	country: str
	lang: str


class AddonIpResponse(BaseModel):
	model_config = ConfigDict(extra="allow")

	code: int
	msg: str
	data: AddonIpData
