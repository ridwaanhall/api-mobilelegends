from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class MlbbCollectionData(BaseModel):
	model_config = ConfigDict(extra="allow")

	records: list[dict[str, Any]] | None = None
	total: int | None = None


class MlbbCollectionResponse(BaseModel):
	model_config = ConfigDict(extra="allow")

	code: int
	message: str | None = None
	data: MlbbCollectionData | dict[str, Any] | None = None
	traceID: str | None = None
