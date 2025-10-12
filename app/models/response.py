"""
Pydantic Models for API Responses

This module contains Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    """Standard API response model."""
    
    code: int = Field(description="HTTP status code")
    status: str = Field(description="Response status (success/error)")
    message: str = Field(description="Response message")
    data: Optional[Any] = Field(default=None, description="Response data")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details"
    )


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    
    page_index: int = Field(description="Current page index")
    page_size: int = Field(description="Page size")
    total_pages: Optional[int] = Field(
        default=None,
        description="Total number of pages"
    )
    total_items: Optional[int] = Field(
        default=None,
        description="Total number of items"
    )


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(description="Service status")
    version: str = Field(description="API version")
    api_available: bool = Field(description="API availability status")


class SupportInfo(BaseModel):
    """Support information model."""
    
    status: str = Field(description="API status")
    message: str = Field(description="Status message")
    support_message: str = Field(description="Support message")
    donation_link: str = Field(description="Donation link")


class ServiceEndpoints(BaseModel):
    """Service endpoints model."""
    
    status: str = Field(description="Service status")
    message: str = Field(description="Service message")
    endpoints: Dict[str, str] = Field(description="Available endpoints")


class APIMetadata(BaseModel):
    """API metadata model."""
    
    version: str = Field(description="API version")
    author: str = Field(description="API author")
    support: SupportInfo = Field(description="Support information")
    available_endpoints: List[str] = Field(
        description="List of available endpoints"
    )


class APIRootResponse(BaseModel):
    """Root API endpoint response model."""
    
    code: int = Field(description="HTTP status code")
    status: str = Field(description="Response status")
    message: str = Field(description="Response message")
    meta: APIMetadata = Field(description="API metadata")
    services: Dict[str, ServiceEndpoints] = Field(
        description="Available services"
    )
    links: Dict[str, str] = Field(description="Important links")


class WinRateCalculation(BaseModel):
    """Win rate calculation model."""
    
    status: str = Field(description="Calculation status")
    match_now: int = Field(description="Current number of matches")
    wr_now: float = Field(description="Current win rate percentage")
    wr_future: float = Field(description="Target win rate percentage")
    required_no_lose_matches: Optional[int] = Field(
        default=None,
        description="Required consecutive wins"
    )
    message: str = Field(description="Calculation message")
