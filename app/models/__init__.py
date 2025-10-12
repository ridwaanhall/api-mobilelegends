"""Models module initialization."""

from app.models.hero import (
    HeroBasic,
    HeroRole,
    HeroLane,
    HeroDetail,
    HeroStats,
    HeroRanking,
    HeroSkill,
    HeroSkillCombo,
    HeroRelation,
    HeroCounters,
    HeroCompatibility,
)
from app.models.response import (
    APIResponse,
    ErrorResponse,
    PaginationMeta,
    HealthCheckResponse,
    SupportInfo,
    ServiceEndpoints,
    APIMetadata,
    APIRootResponse,
    WinRateCalculation,
)

__all__ = [
    # Hero models
    "HeroBasic",
    "HeroRole",
    "HeroLane",
    "HeroDetail",
    "HeroStats",
    "HeroRanking",
    "HeroSkill",
    "HeroSkillCombo",
    "HeroRelation",
    "HeroCounters",
    "HeroCompatibility",
    # Response models
    "APIResponse",
    "ErrorResponse",
    "PaginationMeta",
    "HealthCheckResponse",
    "SupportInfo",
    "ServiceEndpoints",
    "APIMetadata",
    "APIRootResponse",
    "WinRateCalculation",
]
