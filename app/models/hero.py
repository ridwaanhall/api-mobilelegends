"""
Hero Data Models

This module contains Pydantic models for hero-related data.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class HeroBasic(BaseModel):
    """Basic hero information."""
    
    hero_id: int = Field(description="Unique hero identifier")
    name: str = Field(description="Hero name")
    smallmap: Optional[str] = Field(
        default=None,
        description="Small map icon URL"
    )
    head: Optional[str] = Field(
        default=None,
        description="Hero head icon URL"
    )


class HeroRole(BaseModel):
    """Hero role information."""
    
    role_id: int = Field(description="Role identifier")
    role_name: str = Field(description="Role name")


class HeroLane(BaseModel):
    """Hero lane information."""
    
    lane_id: int = Field(description="Lane identifier")
    lane_name: str = Field(description="Lane name")


class HeroDetail(BaseModel):
    """Detailed hero information."""
    
    hero_id: int = Field(description="Unique hero identifier")
    name: str = Field(description="Hero name")
    description: Optional[str] = Field(
        default=None,
        description="Hero description"
    )
    roles: List[HeroRole] = Field(
        default_factory=list,
        description="Hero roles"
    )
    lanes: List[HeroLane] = Field(
        default_factory=list,
        description="Hero preferred lanes"
    )
    attributes: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Hero attributes and stats"
    )


class HeroStats(BaseModel):
    """Hero statistics."""
    
    hero_id: int = Field(description="Unique hero identifier")
    win_rate: float = Field(description="Win rate percentage")
    pick_rate: float = Field(description="Pick rate percentage")
    ban_rate: float = Field(description="Ban rate percentage")
    appearance_rate: Optional[float] = Field(
        default=None,
        description="Appearance rate percentage"
    )
    matches: Optional[int] = Field(
        default=None,
        description="Total matches"
    )


class HeroRanking(BaseModel):
    """Hero ranking information."""
    
    rank: int = Field(description="Current rank position")
    hero: HeroBasic = Field(description="Hero information")
    stats: HeroStats = Field(description="Hero statistics")


class HeroSkill(BaseModel):
    """Hero skill information."""
    
    skill_id: int = Field(description="Skill identifier")
    name: str = Field(description="Skill name")
    description: str = Field(description="Skill description")
    icon: Optional[str] = Field(
        default=None,
        description="Skill icon URL"
    )


class HeroSkillCombo(BaseModel):
    """Hero skill combo information."""
    
    hero_id: int = Field(description="Unique hero identifier")
    combos: List[List[int]] = Field(
        description="List of skill combo sequences"
    )
    skills: List[HeroSkill] = Field(description="Available skills")


class HeroRelation(BaseModel):
    """Hero relationship information (counters/synergies)."""
    
    hero_id: int = Field(description="Related hero identifier")
    relation_type: str = Field(
        description="Relationship type (counter/synergy)"
    )
    effectiveness: float = Field(
        description="Effectiveness rating (0-100)"
    )


class HeroCounters(BaseModel):
    """Hero counter information."""
    
    hero_id: int = Field(description="Unique hero identifier")
    counters: List[HeroRelation] = Field(
        description="Heroes that counter this hero"
    )
    countered_by: List[HeroRelation] = Field(
        description="Heroes countered by this hero"
    )


class HeroCompatibility(BaseModel):
    """Hero compatibility/synergy information."""
    
    hero_id: int = Field(description="Unique hero identifier")
    synergies: List[HeroRelation] = Field(
        description="Heroes with good synergy"
    )
