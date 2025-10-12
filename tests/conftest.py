"""
Pytest Configuration

This file contains pytest fixtures and configuration.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI application.
    
    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(app)


@pytest.fixture
def test_settings():
    """
    Get test settings.
    
    Returns:
        Settings: Application settings
    """
    return settings


@pytest.fixture
def mock_mlbb_response():
    """
    Mock MLBB API response.
    
    Returns:
        dict: Mock response data
    """
    return {
        "code": 200,
        "data": {
            "list": [
                {
                    "hero_id": 1,
                    "hero": {
                        "data": {
                            "name": "Test Hero",
                            "head": "https://example.com/hero.jpg",
                            "smallmap": "https://example.com/small.jpg"
                        }
                    }
                }
            ]
        }
    }
