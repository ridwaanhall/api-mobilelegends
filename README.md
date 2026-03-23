# Mobile Legends: Bang Bang (MLBB) Public Data API (MLBB + Academy)

Production API service that provides Mobile Legends data endpoints for analytics, hero insights, and academy content.

## What The API Can Do

- Provide MLBB hero listings, rank performance, role/lane filters, matchup data, and win-rate utilities.
- Provide MLBB Academy resources including heroes, roles, equipment, emblems, spells, guides, trends, and ratings.
- Expose interactive API documentation for direct request testing in browser.
- Return standardized error payloads for validation and service-level failures.

## Documentation

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- Swagger alias: `/api/docs`

## Available URLs

```txt
https://mlbb-stats.rone.dev                # root (redirects to /docs)
https://mlbb-stats.rone.dev/api            # API index and endpoint map
https://mlbb-stats.rone.dev/docs           # Swagger UI
https://mlbb-stats.rone.dev/redoc          # ReDoc
https://mlbb-stats.rone.dev/api/docs       # Swagger alias (redirects to /docs)
https://mlbb-stats.rone.dev/robots.txt
```

## Example Usage in FastAPI

1. Visit [mlbb-stats.rone.dev/docs](https://mlbb-stats.rone.dev/docs)

2. Open any API (example: `/api/hero-rank`)
   ![Step 2](images/step-02.png)
   *Note: If clicking does not work, try expanding the dropdown.*

3. Click **Try it out**
   ![Step 3](images/step-03.png)

4. Fill in the required data (or leave defaults if support)
   ![Step 4](images/step-04.png)

5. Click **Execute**
   ![Step 5](images/step-05.png)

6. You will see a response like this:
   ![Step 6](images/step-06.png)
   - **Red box**: `curl` code to fetch data
   - **Yellow box**: Request URL to directly test the API
   - **Green Box**: The actual API output

## API Coverage

### Root API

- `GET /api` — API Index and Status
- `GET /robots.txt` — Robots.txt for Web Crawlers

### MLBB Game Data API

- `GET /api/hero-list` — List Heroes
- `GET /api/hero-rank` — Hero Rank Statistics
- `GET /api/hero-position` — Hero Position Filters
- `GET /api/hero-detail/{hero_identifier}` — Hero Detail
- `GET /api/hero-detail-stats/{hero_identifier}` — Hero Detail Statistics
- `GET /api/hero-skill-combo/{hero_identifier}` — Hero Skill Combo
- `GET /api/hero-rate/{hero_identifier}` — Hero Rate Trends
- `GET /api/hero-relation/{hero_identifier}` — Hero Relations
- `GET /api/hero-counter/{hero_identifier}` — Hero Counters
- `GET /api/hero-compatibility/{hero_identifier}` — Hero Compatibility

### MLBB Academy API

- `GET /api/academy/version` — Game Version Info
- `GET /api/academy/heroes/old` — Hero Catalog
- `GET /api/academy/roles` — Roles
- `GET /api/academy/equipment` — Equipment (Items)
- `GET /api/academy/equipment-details` — Equipment Details
- `GET /api/academy/spells` — Battle Spells
- `GET /api/academy/emblems` — Emblems
- `GET /api/academy/rank` — Rank List
- `GET /api/academy/rank/{rank_id}` — Rank Details
- `GET /api/academy/recommended` — Recommended Content
- `GET /api/academy/recommended/{recommended_id}` — Recommended Detail
- `GET /api/academy/heroes` — Hero Filters
- `GET /api/academy/heroes/{hero_id}/stats` — Hero Statistics
- `GET /api/academy/heroes/{hero_id}/lane` — Hero Lane Distribution
- `GET /api/academy/heroes/{hero_id}/time-win-rate/{lane_id}` — Hero Lane Time-based Win Rate
- `GET /api/academy/heroes/{hero_id}/builds` — Hero Recommended Builds
- `GET /api/academy/heroes/{hero_id}/counters` — Hero Counters
- `GET /api/academy/heroes/{hero_id}/teammates` — Hero Teammates
- `GET /api/academy/heroes/{hero_id}/trends` — Hero Performance Trends
- `GET /api/academy/heroes/{hero_id}/recommended` — Hero Recommended Content
- `GET /api/academy/heroes/ratings` — Hero Ratings Index
- `GET /api/academy/heroes/ratings/{subject}` — Hero Ratings by Subject

### User API

- `POST /api/user/auth/send-vc` — Send Verification Code
- `POST /api/user/auth/login` — Login with Verification Code
- `POST /api/user/auth/logout` — Logout
- `POST /api/user/info` — User Info
- `POST /api/user/stats` — User Statistics
- `POST /api/user/season` — User Season List
- `POST /api/user/match` — User Matches
- `POST /api/user/match/{match_id}` — User Match Details
- `POST /api/user/heros/frequent` — User Frequent Heroes
- `POST /api/user/friends` — User Friends

### Addon API

- `GET /api/addon/win-rate` — Win Rate Calculator for Consecutive Wins
- `GET /api/addon/check-ip` — Check IP Address Location Details

## Changelog

Migration notes are documented in [Releases](https://github.com/ridwaanhall/api-mobilelegends/releases).

## License

This project is released under the **BSD 3-Clause License**. Attribution to **Moonton** and **ridwaanhall** should be preserved in downstream usage.

---

<details>
   <summary>Local Development (for ridwaanhall only)</summary>

   1. **Create virtual environment**

      ```bash
      python -m venv .venv
      ```

   2. **Activate virtual environment**

      - On Linux/macOS:

      ```bash
      source .venv/bin/activate
      ```

      - On Windows (PowerShell):

      ```bash
      .venv\Scripts\Activate.ps1
      ```

   3. **Install dependencies**

      ```bash
      pip install -r requirements.txt
      ```

   4. **Create environment file**

      ```bash
      cp .env.example .env
      ```

   5. **Run tests**

      ```bash
      pytest
      ```

   6. **Start FastAPI server**

      ```bash
      uvicorn app.main:app --reload
      ```

   Configuration

   Required variables:
      - `SECRET_KEY`
      - `RONE_DEV_ACCESS_KEY`
      - `RONE_DEV_ACCESS_KEY_V2`

   See `.env.example` for full environment options.
   </details>
