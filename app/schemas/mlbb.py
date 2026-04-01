from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class MlbbCollectionData(BaseModel):
	model_config = ConfigDict(extra="allow")

	records: list[dict[str, Any]]
	total: int


class MlbbCollectionResponse(BaseModel):
	model_config = ConfigDict(extra="allow")

	code: int
	message: str
	data: MlbbCollectionData
	traceID: str | None = None
