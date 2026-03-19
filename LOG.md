# API v3.0.0 Migration Notes

## Overview

Version 3.0.0 is a major release focused on framework modernization, documentation quality, API contract clarity, and deployment readiness.

## Release Scope

- Migrated runtime from Django to FastAPI with an ASGI-first stack.
- Consolidated public APIs into two primary service groups:
  - MLBB API
  - MLBB Academy API
- Standardized endpoint behavior and error contracts for client integrations.

## Key Differences: v2.0.3 -> v3.0.0

### 1. Framework and Runtime

- Replaced Django implementation with FastAPI.
- Moved to ASGI entrypoint for serverless deployment compatibility.
- Updated dependency set for FastAPI, Pydantic v2, and Starlette ecosystem.

### 2. API Documentation Experience

- Added interactive Swagger UI at `/docs`.
- Added ReDoc at `/redoc`.
- Added `/api/docs` redirect alias to Swagger UI.
- Improved OpenAPI parameter metadata with explicit descriptions, allowed values, and range constraints.

### 3. Endpoint Surface and Organization

- Preserved and exposed MLBB and MLBB Academy endpoint groups under `/api/`.
- Removed unsupported service exposure from API index (legacy/non-core service references are no longer listed).
- Improved API index links and service visibility for consumers.

### 4. Validation and Error Contract

- Added centralized validation handling with consistent error payload structure.
- Expanded contract coverage with endpoint tests for:
  - docs availability and redirects,
  - service index exposure,
  - OpenAPI schema constraints,
  - validation failures on invalid enum/range inputs.

### 5. Deployment and Operations

- Optimized for Vercel serverless deployment via ASGI entrypoint.
- Updated environment variable defaults and project configuration to align with v3 behavior.

## Compatibility Notes

- Base API paths remain under `/api/` for MLBB and Academy services.
- Consumers should update any tooling or docs references to use the new interactive docs endpoints.
- Validation behavior is stricter for enum and range constrained parameters; invalid inputs now consistently return validation error payloads.

## Recommended Upgrade Steps

1. Pull latest code and install updated dependencies.
2. Sync environment variables using `.env.example`.
3. Validate client integrations against `/docs` OpenAPI schema.
4. Run test suite before deployment:
   - `pytest -q`

## Versioning

- Previous: v2.0.3
- Current: v3.0.0
