# API Changelog

All notable changes to the API will be documented in this file.  
**Newest version always at the top.**  
This file now tracks **EVERY version** (v3.0.0 + full v2 history).

## [3.0.0] - 2026-03-19

**Major release** – Complete framework modernization (Django → FastAPI), documentation overhaul, and deployment readiness.

### Release Scope

- Migrated runtime from Django to FastAPI with an ASGI-first stack.
- Consolidated public APIs into two primary service groups:
  - MLBB API
  - MLBB Academy API
- **Removed**: MPL ID API (`/api/mplid/`) and all web version endpoints (legacy/non-core services no longer exposed).  
  **Now strictly API-only** for v3.0.0 and all future releases.
- Standardized endpoint behavior and error contracts for client integrations.

### Key Differences: v2.0.3 → v3.0.0

#### 1. Framework and Runtime

- Replaced Django implementation with FastAPI.
- Moved to ASGI entrypoint for serverless deployment compatibility.
- Updated dependency set for FastAPI, Pydantic v2, and Starlette ecosystem.

#### 2. API Documentation Experience

- Added interactive Swagger UI at `/docs`.
- Added ReDoc at `/redoc`.
- Added `/api/docs` redirect alias to Swagger UI.
- Improved OpenAPI parameter metadata with explicit descriptions, allowed values, and range constraints.
- Refreshed `sitemap.xml` entries to the current FastAPI endpoint paths for improved crawler discovery.
- Updated `robots.txt` to explicitly allow full crawling and expose sitemap/host hints.

#### 3. Endpoint Surface and Organization

- Preserved and exposed MLBB and MLBB Academy endpoint groups under `/api/`.
- Removed unsupported service exposure from API index (legacy/non-core service references are no longer listed).
- Removed MPL ID API and web version endpoints (now **API-only**).
- Improved API index links and service visibility for consumers.

#### 4. Validation and Error Contract

- Added centralized validation handling with consistent error payload structure.
- Expanded contract coverage with endpoint tests.

#### 5. Deployment and Operations

- Optimized for Vercel serverless deployment via ASGI entrypoint.
- Updated environment variable defaults and project configuration to align with v3 behavior.

### Compatibility Notes

- Base API paths remain under `/api/` for MLBB and Academy services **only**.
- Consumers should update any tooling or docs references to use the new interactive docs endpoints.
- Validation behavior is stricter for enum and range constrained parameters.

### Recommended Upgrade Steps

1. Pull latest code and install updated dependencies.
2. Sync environment variables using `.env.example`.
3. Validate client integrations against `/docs` OpenAPI schema.
4. Run test suite before deployment: `pytest -q`

### Versioning

- Previous: v2.0.3
- Current: v3.0.0

## [2.0.3] - 2026-03-18

**Patch release** – Final Django-era updates. All commits you sent belong here (Mar 18 down to Dec 2025). This was the last version before the v3.0.0 FastAPI migration.

### Key Changes (grouped from your git history)

#### Error Handling & Utils (Mar 18)

- 🛡️ **refactor(utils)**: Standardized error envelope and sanitized upstream failures.
- 🔧 **fix(hero)**: Changed return value from `None` to `0` in `HeroNameHelper` for consistent hero ID handling.
- ✨ **feat(utils)**: Added random user agent selection for improved request variability.
- 🔧 **fix(utils)**: Renamed `RONEHA_DEV_KEY` to `RONE_DEV_KEY` for consistency.

#### Config & Versioning (Mar 17–18)

- 🔧 **fix(config)**: Updated `API_VERSION` to 2.0.2 for version consistency.
- 🔧 **fix(config)**: Updated `IS_AVAILABLE` default value to `True` and adjusted date availability logic.
- 🔧 **fix(config)**: Updated API availability settings (default `False` → `True` in final step).

#### Maintenance & Dependencies

- 🛠️ **build(deps)**: Bumped Django to 5.2.12.
- 📝 **docs(README)**: Added Repo Stars section with embed.
- 🔧 **chore(config)**: Updated base URLs in README and API version to 2.0.1 (earlier step).

#### SEO, Templates & Meta (Feb–Jan 2026)

- 📝 **chore(api-status)**: Fixed grammar in maintenance message.
- 🐛 **fix(template)**: Prevented invalid JSON-LD from autoescaping.
- feat(meta): Enhanced meta tags for SEO + Open Graph + Twitter cards.
- feat(site): Added `SITE_TITLE` configuration and dynamic branding.
- feat(template): Added `api.html` template for REST framework with SEO enhancements.
- chore(template): Removed unused `base.html`.
- fix(settings): Updated base URLs, timezone handling, and documentation links.

#### MLBB Academy (Major Feature Addition – Jan 16–17, 2026)

- Initial MLBB Academy feature (#58).
- Added full Academy endpoints:
  - `HeroesView`, `HeroStatsView`, `HeroLaneView`, `HeroTimeWinRateView`, `HeroBuildsView`, `HeroCountersView`, `HeroTeammatesView`
  - `HeroGuideTrendsView`, `HeroGuideTimeWinRateView`, `GuideView` (with role/lane filtering)
  - `RecommendedView`, `RecommendedDetailView`
  - Roles, spells, emblems, equipment list
  - Hero ratings by subject
- feat(core): Enhanced API availability management and version endpoint.
- Added utility classes for encryption.

#### Other (Jan–Dec 2025)

- Multiple dependency bumps (urllib3, cryptography, sqlparse, pip).
- .gitignore updates.
- Base URL and settings fixes.

### Recommended Upgrade Steps (for v2.0.3)

- Update `.env` with new key name (`RONE_DEV_KEY`).
- Test hero ID endpoints and error responses.
- Check new MLBB Academy endpoints under `/api/academy/`.

## [2.0.2] and earlier

Older history preserved here in real usage – dependency bumps, initial config module, etc.
