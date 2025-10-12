"""
Test API Health Endpoint

Tests for health check and basic API endpoints.
"""

import pytest
from fastapi import status


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "api_available" in data


def test_root_redirect(client):
    """Test root endpoint redirects to API."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/api/"


def test_api_root(client):
    """Test API root endpoint."""
    response = client.get("/api/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["status"] == "success"
    assert "meta" in data
    assert "services" in data
    assert "links" in data


def test_docs_endpoint(client):
    """Test Swagger UI docs endpoint."""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


def test_redoc_endpoint(client):
    """Test ReDoc endpoint."""
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK


def test_openapi_schema(client):
    """Test OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data


def test_404_handler(client):
    """Test custom 404 handler."""
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert data["error"] == "Not Found"
    assert "message" in data
