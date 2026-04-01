from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class AcademyCollectionData(BaseModel):
	model_config = ConfigDict(extra="allow")

	records: list[dict[str, Any]]
	total: int


class AcademyCollectionResponse(BaseModel):
	model_config = ConfigDict(extra="allow")

	code: int
	message: str
	data: AcademyCollectionData
	traceID: str | None = None


class AcademyRatingsSubjectData(BaseModel):
	model_config = ConfigDict(extra="allow")

	id: str
	title: str
	desc: str


class AcademyRatingsItem(BaseModel):
	model_config = ConfigDict(extra="allow")

	subject: int | None = None
	title: str
	desc: str | None = None
	comment_count: int | None = None
	ranking: list[dict[str, Any]] | None = None


class AcademyRatingsData(BaseModel):
	model_config = ConfigDict(extra="allow")

	total: int
	list: list[AcademyRatingsItem | dict[str, Any]]
	has_more: bool | None = None
	subject: AcademyRatingsSubjectData | None = None


class AcademyRatingsResponse(BaseModel):
	model_config = ConfigDict(extra="allow")

	code: int
	message: str
	traceID: str | None = None
	data: AcademyRatingsData
