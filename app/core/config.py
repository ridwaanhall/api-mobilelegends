"""
Core Configuration Module

This module handles all application configuration including:
- Environment variables
- API settings
- Security settings
- CORS configuration
"""

from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # API Configuration
    API_VERSION: str = Field(default="2.0.0", description="API version")
    API_TITLE: str = Field(
        default="Mobile Legends API",
        description="API title"
    )
    API_DESCRIPTION: str = Field(
        default="Mobile Legends Bang Bang API for hero data and statistics",
        description="API description"
    )
    
    # API Availability
    IS_AVAILABLE: bool = Field(
        default=True,
        description="Controls API endpoint availability"
    )
    
    # Support Information
    SUPPORT_MESSAGE: str = Field(
        default="You can support us by donating from $1 USD (target: $500 USD) "
                "to help enhance API performance and handle high request volumes.",
        description="Support message for users"
    )
    DONATION_LINK: str = Field(
        default="https://github.com/sponsors/ridwaanhall",
        description="Donation link"
    )
    
    # Security
    SECRET_KEY: str = Field(
        ...,
        description="Secret key for encryption (required)"
    )
    
    # External Services
    MLBB_URL: str = Field(
        ...,
        description="MLBB API base URL (required)"
    )
    
    # Environment
    DEBUG: bool = Field(
        default=False,
        description="Debug mode"
    )
    ENVIRONMENT: str = Field(
        default="production",
        description="Environment (development/staging/production)"
    )
    
    # Production URL
    PROD_URL: str = Field(
        default="http://127.0.0.1:8000/api/",
        description="Production URL"
    )
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=[
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:8000",
            "https://mlbb-stats.ridwaanhall.com",
            "https://mlbb-stats-docs.ridwaanhall.com",
        ],
        description="Allowed CORS origins"
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60,
        description="Rate limit per minute"
    )
    
    # Logging
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = ["development", "staging", "production"]
        if v.lower() not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v.lower()
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of {allowed}")
        return v.upper()
    
    @property
    def support_details(self) -> Dict[str, str]:
        """Get support details."""
        return {
            "support_message": self.SUPPORT_MESSAGE,
            "donation_link": self.DONATION_LINK
        }
    
    @property
    def api_status_messages(self) -> Dict[str, Dict[str, Any]]:
        """Get API status messages."""
        return {
            "limited": {
                "status": "limited",
                "message": "API is currently in maintenance mode. Will be available soon.",
                "available_endpoints": ["Base API"]
            },
            "available": {
                "status": "available",
                "message": "All API endpoints are fully operational.",
                "available_endpoints": ["All endpoints"]
            }
        }
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.DEBUG or self.ENVIRONMENT == "development"
    
    @property
    def base_url(self) -> str:
        """Get base URL based on environment."""
        if self.is_development:
            return "http://127.0.0.1:8000/api/"
        return self.PROD_URL


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()


# Create settings instance
settings = get_settings()
