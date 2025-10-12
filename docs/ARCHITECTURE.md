"""
Documentation

Additional documentation files for the API.
"""

# API Architecture

## Overview

This document describes the architecture of the Mobile Legends API.

## Components

### Core Layer
- **config.py**: Configuration management using Pydantic Settings
- **logging.py**: Structured logging setup
- **security.py**: Cryptographic utilities

### Service Layer
- **mlbb_service.py**: Business logic for MLBB API integration
- **calculation_service.py**: Game-related calculations

### API Layer
- **endpoints/**: FastAPI route handlers
- **api.py**: Router aggregation

### Models
- **hero.py**: Hero-related Pydantic models
- **response.py**: Response models for API

### Utils
- **http_client.py**: HTTP client wrapper with error handling

## Request Flow

```
Client Request
    ↓
FastAPI Application (main.py)
    ↓
API Router (api.py)
    ↓
Endpoint Handler (endpoints/*.py)
    ↓
Service Layer (services/*.py)
    ↓
HTTP Client (utils/http_client.py)
    ↓
External MLBB API
```

## Error Handling

- Service layer catches `RequestException`
- Endpoints convert to appropriate HTTP exceptions
- Custom error handlers in main.py

## Testing Strategy

- Unit tests for services
- Integration tests for API endpoints
- Mock external API calls

## Deployment

- Vercel serverless deployment
- Environment-based configuration
- Health check endpoint for monitoring
