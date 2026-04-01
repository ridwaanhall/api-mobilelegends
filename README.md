# MLBB Public Data API

[![API Live](https://img.shields.io/badge/API-Live-brightgreen?logo=fastapi&logoColor=white)](https://mlbb.rone.dev/api/docs)
![Release](https://img.shields.io/github/v/release/ridwaanhall/api-mobilelegends?logo=github)
![License](https://img.shields.io/github/license/ridwaanhall/api-mobilelegends?logo=opensourceinitiative&logoColor=white)
![Stars](https://img.shields.io/github/stars/ridwaanhall/api-mobilelegends?logo=github)
![Forks](https://img.shields.io/github/forks/ridwaanhall/api-mobilelegends?logo=github)
![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-green?logo=openapiinitiative&logoColor=white)

This API provides access to hero analytics, in-game performance data, academy resources, player endpoints, and utility tools. It is designed with a consistent RESTful structure, supports flexible hero identifiers (ID or name), and delivers standardized responses for seamless integration into applications, dashboards, and analytics systems.

---

> [!IMPORTANT]
> **Built with Dedication:** This project is the result of over [![wakatime](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/07151d3c-c9e1-4f53-bb7f-f706f8261ac4.svg)](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/07151d3c-c9e1-4f53-bb7f-f706f8261ac4) of meticulous coding, architecting, and performance tuning to ensure the best developer experience.

## Features

- **Hero listings**: Rankings, positions, and detailed analytics
- **Performance trends**: Skill combos, counters, and compatibility insights
- **MLBB Academy data**: Roles, equipment, emblems, spells, builds, and ratings
- **Player endpoints**: Authentication, stats, match history, and social data
- **Utility tools**: Win rate calculator and IP lookup
- **Interactive API documentation**: Swagger & ReDoc

---

## Documentation

- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`
- OpenAPI JSON: `/api/openapi.json`

---

## Base URLs

```txt
https://mlbb.rone.dev                # root (redirects to /api/docs)
https://mlbb.rone.dev/api            # API index and status
https://mlbb.rone.dev/api/docs       # Swagger UI
https://mlbb.rone.dev/api/redoc      # ReDoc
https://mlbb.rone.dev/api/openapi.json
https://mlbb.rone.dev/robots.txt
```

---

## Quick Start

### 1. Visit [mlbb.rone.dev/api/docs](https://mlbb.rone.dev/api/docs)

### 2. Open any API (example: `/api/hero-rank`)

![Step 2](images/step-02.png)
*Note: If clicking does not work, try expanding the dropdown.*

### 3. Click *Try it out*

![Step 3](images/step-03.png)

### 4. Fill in the required data (or leave defaults if support)

![Step 4](images/step-04.png)

### 5. Click **Execute**

![Step 5](images/step-05.png)

### 6. You will see a response like this

![Step 6](images/step-06.png)

- **Red box**: `curl` code to fetch data
- **Yellow box**: Request URL to directly test the API
- **Green Box**: The actual API output

---

## API Coverage

### Root

- `GET /api` — API Index and Status
- `GET /robots.txt` — Robots.txt for Web Crawlers

### MLBB

- `GET /api/heroes` — List Heroes
- `GET /api/heroes/rank` — Hero Rank Statistics
- `GET /api/heroes/positions` — Hero Position Filters
- `GET /api/heroes/{hero_identifier}` — Hero Detail
- `GET /api/heroes/{hero_identifier}/stats` — Hero Detail Statistics
- `GET /api/heroes/{hero_identifier}/skill-combos` — Hero Skill Combos
- `GET /api/heroes/{hero_identifier}/trends` — Hero Performance Trends
- `GET /api/heroes/{hero_identifier}/relations` — Hero Relations
- `GET /api/heroes/{hero_identifier}/counters` — Hero Counters
- `GET /api/heroes/{hero_identifier}/compatibility` — Hero Compatibility

### Academy

- `GET /api/academy/meta/version` — Game Version Info
- `GET /api/academy/heroes/catalog` — Hero Catalog
- `GET /api/academy/roles` — Roles
- `GET /api/academy/equipment` — Equipment (Items)
- `GET /api/academy/equipment/expanded` — Equipment Expanded
- `GET /api/academy/spells` — Battle Spells
- `GET /api/academy/emblems` — Emblems
- `GET /api/academy/ranks` — Ranks List
- `GET /api/academy/ranks/{rank_id}` — Ranks Details
- `GET /api/academy/recommended` — Recommended Content
- `GET /api/academy/recommended/{recommended_id}` — Recommended Detail
- `GET /api/academy/heroes` — Hero Filters
- `GET /api/academy/heroes/{hero_identifier}/stats` — Hero Statistics
- `GET /api/academy/heroes/{hero_identifier}/lane` — Hero Lane Distribution
- `GET /api/academy/heroes/{hero_identifier}/win-rate/timeline` — Hero Lane Time-based Win Rate
- `GET /api/academy/heroes/{hero_identifier}/builds` — Hero Recommended Builds
- `GET /api/academy/heroes/{hero_identifier}/counters` — Hero Counters
- `GET /api/academy/heroes/{hero_identifier}/teammates` — Hero Teammates
- `GET /api/academy/heroes/{hero_identifier}/trends` — Hero Performance Trends
- `GET /api/academy/heroes/{hero_identifier}/recommended` — Hero Recommended Content
- `GET /api/academy/heroes/ratings` — Hero Ratings Index
- `GET /api/academy/heroes/ratings/{subject}` — Hero Ratings by Subject

### User

- `POST /api/user/auth/send-vc` — Send Verification Code
- `POST /api/user/auth/login` — Login with Verification Code
- `POST /api/user/auth/logout` — Logout
- `POST /api/user/info` — User Info
- `POST /api/user/stats` — User Statistics
- `POST /api/user/season` — User Season List
- `POST /api/user/matches` — User Matches
- `POST /api/user/matches/{match_id}` — User Match Details
- `POST /api/user/heroes/frequent` — User Frequent Heroes
- `POST /api/user/friends` — User Friends

### Addon

- `GET /api/addon/win-rate-calculator` — Win Rate Calculator
- `GET /api/addon/ip` — IP Address Lookup

---

## Changelog

See [Releases](https://github.com/ridwaanhall/api-mobilelegends/releases) for migration notes and updates.

---

## License

This project is licensed under the **BSD 3-Clause License**.
Attribution to **Moonton** and **ridwaanhall** must be preserved in downstream usage.

---

<details>
<summary>Local Development (internal)</summary>

### Setup

```bash
# skip this if already have
uv init # create pyproject.toml
uv add fastapi # add deps
uv add pytest --dev # add deps for dev

# use this if already have pyproject.toml and uv.lock
uv sync
cp .env.example .env
```

### Run

```bash
# for development
fastapi dev

# production
fastapi run
```

### Test

```bash
pytest
```

### Environment Variables

- `SECRET_KEY`
- `RONE_DEV_ACCESS_KEY`
- `RONE_DEV_ACCESS_KEY_V2`

See `.env.example` for full configuration.

</details>
