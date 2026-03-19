# API Mobile Legends (FastAPI)

Production-ready FastAPI migration of the MLBB analytics API, structured for maintainability and optimized for Vercel serverless deployment.

## What This Project Provides

- Full FastAPI implementation of all previous Django endpoints under `/api/`
- Modular architecture with clear separation of routers, services, and core utilities
- Standardized error responses for upstream failures and API validation errors
- Secure encrypted/decrypted base-path handling for external API access via `.env`
- Serverless-compatible deployment configuration for Vercel

## Architecture

```txt
app/
  api/
    dependencies.py
    routers/
      root.py
      mlbb.py
      academy.py
  core/
    config.py
    errors.py
    http.py
    security.py
  services/
    mlbb.py
    academy.py
  main.py
api/
  index.py
```

## Base URLs

```txt
https://mlbb-stats.rone.dev/                # root (redirects to /api/)
https://mlbb-stats.rone.dev/api/            # API index and endpoint map
https://mlbb-stats.rone.dev/docs            # Swagger UI (try API directly)
https://mlbb-stats.rone.dev/redoc           # ReDoc documentation
https://mlbb-stats.rone.dev/api/docs/       # same API index response
https://mlbb-stats.rone.dev/robots.txt
https://mlbb-stats.rone.dev/sitemap.xml
```

## Implemented Endpoints

### MLBB

- `GET /api/hero-list/`
- `GET /api/hero-rank/`
- `GET /api/hero-position/`
- `GET /api/hero-detail/{hero_id_or_name}/`
- `GET /api/hero-detail-stats/{hero_id_or_name}/`
- `GET /api/hero-skill-combo/{hero_id_or_name}/`
- `GET /api/hero-rate/{hero_id_or_name}/`
- `GET /api/hero-relation/{hero_id_or_name}/`
- `GET /api/hero-counter/{hero_id_or_name}/`
- `GET /api/hero-compatibility/{hero_id_or_name}/`
- `GET /api/win-rate/?match-now=&wr-now=&wr-future=`

### Academy

- `GET /api/academy/version/`
- `GET /api/academy/heroes/`
- `GET /api/academy/roles/`
- `GET /api/academy/equipment/`
- `GET /api/academy/equipment-details/`
- `GET /api/academy/spells/`
- `GET /api/academy/emblems/`
- `GET /api/academy/recommended/`
- `GET /api/academy/recommended/{recommended_id}/`
- `GET /api/academy/guide/`
- `GET /api/academy/guide/{hero_id}/stats/`
- `GET /api/academy/guide/{hero_id}/lane/`
- `GET /api/academy/guide/{hero_id}/time-win-rate/{lane_id}/`
- `GET /api/academy/guide/{hero_id}/builds/`
- `GET /api/academy/guide/{hero_id}/counters/`
- `GET /api/academy/guide/{hero_id}/teammates/`
- `GET /api/academy/guide/{hero_id}/trends/`
- `GET /api/academy/guide/{hero_id}/recommended/`
- `GET /api/academy/hero-ratings/`
- `GET /api/academy/hero-ratings/{subject}/`

## Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Create environment file:

```bash
cp .env.example .env
```

1. Run FastAPI:

```bash
uvicorn app.main:app --reload
```

## Environment Variables

Minimum required:

- `SECRET_KEY`
- `MLBB_URL`
- `MLBB_URL_V2`

See `.env.example` for full optional settings.

## Vercel Deployment

This repository is configured for serverless deployment through:

- `api/index.py` as the ASGI entrypoint
- `vercel.json` routing all requests to `api/index.py`

Deploy normally with Vercel CLI or Git integration.

## Notes

- If `IS_AVAILABLE=False`, API endpoints return a maintenance/service-unavailable response.
- Upstream MLBB path segments are decrypted at runtime using `SECRET_KEY`.

## License and Attribution

This project is released under the BSD 3-Clause License. Attribution to Moonton and ridwaanhall should be preserved in downstream usage.
