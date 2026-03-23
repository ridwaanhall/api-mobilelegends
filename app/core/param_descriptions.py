# param_descriptions.py
"""
Centralized parameter and endpoint descriptions for FastAPI routers.
Organized by module and grouped for clarity and reuse.
"""

# =========================
# core
# =========================

## Pagination
TITLE_PAGE_SIZE = "Page Size"
DESCRIPTION_PAGE_SIZE = "Number of items per page."

TITLE_PAGE_INDEX = "Page Index"
DESCRIPTION_PAGE_INDEX = "Page index (starting from 1)."

TITLE_SORT_ORDER = "Sort Order"
DESCRIPTION_SORT_ORDER = "Sort order for results. Allowed: asc, desc."

TITLE_LANGUAGE = "Language"
DESCRIPTION_LANGUAGE = (
    "Language code for localized content."
)

TITLE_RANK = "Rank"
DESCRIPTION_RANK = "Rank filter. Allowed: all, epic, legend, mythic, honor, glory."

# =========================
# root
# =========================

SUMMARY_API_ROOT = "API Root Endpoint"
DESCRIPTION_API_ROOT = (
    "Overview of the Mobile Legends API, including status, available services, and documentation links."
)

SUMMARY_API_INDEX = "API Index and Status"
DESCRIPTION_API_INDEX = "Provides API metadata, status, and available services."

SUMMARY_API_DOCS = "API Documentation"
DESCRIPTION_API_DOCS = "Redirect to the API documentation."

SUMMARY_ROBOTS_TXT = "Robots.txt for Web Crawlers"
DESCRIPTION_ROBOTS_TXT = "Instructions for web crawlers and bots accessing the API."

# =========================
# mlbb
# =========================

## /api/hero-list
SUMMARY_HERO_LIST = "List Heroes"
DESCRIPTION_HERO_LIST = "Retrieve all heroes with basic information."

## /api/hero-rank
SUMMARY_HERO_RANK_STATS = "Hero Rank Statistics"
DESCRIPTION_HERO_RANK_STATS = "Fetch rank statistics for heroes over a specified time window."

TITLE_PAST_DAYS = "Past Days"
DESCRIPTION_PAST_DAYS = "Past day window. Allowed: 1, 3, 7, 15, 30."

TITLE_SORT_FIELD = "Sort Field"
DESCRIPTION_SORT_FIELD = "Sort field. Allowed: pick_rate, ban_rate, win_rate."

TITLE_HERO_IDENTIFIER = "Hero Identifier"
DESCRIPTION_HERO_IDENTIFIER = (
    "Hero identifier as numeric hero ID (validated dynamically) or hero name. "
    "Name matching ignores spaces/symbols and is case-insensitive."
)

## /api/hero-position
SUMMARY_HERO_POSITION = "Hero Position Filters"
DESCRIPTION_HERO_POSITION = "Filter heroes by their position on the map."

## /api/hero-detail/{hero_identifier}
SUMMARY_HERO_DETAIL = "Hero Detail"
DESCRIPTION_HERO_DETAIL = "Get detailed information for a specific hero."

## /api/hero-detail-stats/{hero_identifier}
SUMMARY_HERO_DETAIL_STATS = "Hero Detail Statistics"
DESCRIPTION_HERO_DETAIL_STATS = "Get detailed statistics for a specific hero."

## /api/hero-skill-combo/{hero_identifier}
SUMMARY_HERO_SKILL_COMBO = "Hero Skill Combo"
DESCRIPTION_HERO_SKILL_COMBO = "Get the most effective skill combo for a specific hero."

## /api/hero-rate/{hero_identifier}
SUMMARY_HERO_RATE = "Hero Rate Trends"
DESCRIPTION_HERO_RATE = "Get rate trends for a specific hero over a specified time window."

TITLE_RATE_WINDOW = "Rate Window (Days)"
DESCRIPTION_RATE_WINDOW = "Rate window in days. Allowed: 7, 15, 30."

## /api/hero-relation/{hero_identifier}
SUMMARY_HERO_RELATION = "Hero Relations"
DESCRIPTION_HERO_RELATION = "Get information about the relations of a specific hero."

## /api/hero-counter/{hero_identifier}
SUMMARY_HERO_COUNTER = "Hero Counters"
DESCRIPTION_HERO_COUNTER = "Get information about heroes that counter a specific hero."

## /api/hero-compatibility/{hero_identifier}
SUMMARY_HERO_COMPATIBILITY = "Hero Compatibility"
DESCRIPTION_HERO_COMPATIBILITY = "Get compatibility information for a specific hero."

# =========================
# academy
# =========================

## /api/academy/version
SUMMARY_ACADEMY_VERSION = "Game Version Info"
DESCRIPTION_ACADEMY_VERSION = "Fetch a list of game versions with release dates."

## /api/academy/heroes
SUMMARY_ACADEMY_HEROES = "Hero Catalog"
DESCRIPTION_ACADEMY_HEROES = "Retrieve all heroes with basic information."

## /api/academy/roles
SUMMARY_ACADEMY_ROLES = "Hero Roles"
DESCRIPTION_ACADEMY_ROLES = "List all hero roles (tank, fighter, assassin, mage, marksman, support)."

## /api/academy/equipment
SUMMARY_ACADEMY_EQUIPMENT = "Equipment (Items)"
DESCRIPTION_ACADEMY_EQUIPMENT = "List all equipment (items) with details."

## /api/academy/equipment-details
SUMMARY_ACADEMY_EQUIPMENT_DETAILS = "Equipment Details"
DESCRIPTION_ACADEMY_EQUIPMENT_DETAILS = "Get detailed information about a specific equipment item."

## /api/academy/spells
SUMMARY_ACADEMY_SPELLS = "Battle Spells"
DESCRIPTION_ACADEMY_SPELLS = "List all battle spells with details."

## /api/academy/emblems
SUMMARY_ACADEMY_EMBLEMS = "Emblems"
DESCRIPTION_ACADEMY_EMBLEMS = "List all emblems with details."

## /api/academy/recommended
SUMMARY_ACADEMY_RECOMMENDED = "Recommended Content"
DESCRIPTION_ACADEMY_RECOMMENDED = "List recommended content for players."

## /api/academy/recommended/{recommended_id}
SUMMARY_ACADEMY_RECOMMENDED_DETAIL = "Recommended Content Detail"
DESCRIPTION_ACADEMY_RECOMMENDED_DETAIL = "Get details for a specific recommended content item."

TITLE_RECOMMENDED_POST_ID = "Recommended Post ID"
DESCRIPTION_RECOMMENDED_POST_ID = "Identifier for the recommended post."

## /api/academy/guide
SUMMARY_ACADEMY_GUIDE = "Guide Hero List"
DESCRIPTION_ACADEMY_GUIDE = "List heroes with filtering options for role and lane."

TITLE_ROLE = "Role"
DESCRIPTION_ROLE = (
    "Role filter. Multi allowed: tank, fighter, assassin, mage, marksman, support. "
    "Example: role=tank&role=fighter"
)

TITLE_LANE = "Lane"
DESCRIPTION_LANE = (
    "Lane filter. Multi allowed: exp, mid, roam, jungle, gold. "
    "Example: lane=exp&lane=mid"
)

## /api/academy/guide/{hero_id}/stats
SUMMARY_ACADEMY_GUIDE_STATS = "Guide Hero Statistics"
DESCRIPTION_ACADEMY_GUIDE_STATS = "Get statistics for a specific hero by rank."

TITLE_HERO_ID = "Hero ID"
DESCRIPTION_HERO_ID = "Hero ID. Maximum is validated dynamically from current hero list."

## /api/academy/guide/{hero_id}/lane
SUMMARY_ACADEMY_GUIDE_LANE = "Guide Hero Lane Distribution"
DESCRIPTION_ACADEMY_GUIDE_LANE = "Get lane distribution for a specific hero."

## /api/academy/guide/{hero_id}/time-win-rate/{lane_id}
SUMMARY_ACADEMY_GUIDE_TIME_WIN_RATE = "Guide Hero Time-based Win Rate for Lane"
DESCRIPTION_ACADEMY_GUIDE_TIME_WIN_RATE = "Get time-based win rate for a hero in a specific lane."

## /api/academy/guide/{hero_id}/builds
SUMMARY_ACADEMY_GUIDE_BUILDS = "Guide Hero Builds (Recommended Equipment) for Lane"
DESCRIPTION_ACADEMY_GUIDE_BUILDS = "Get recommended equipment builds for a hero in a specific lane."

## /api/academy/guide/{hero_id}/counters
SUMMARY_ACADEMY_GUIDE_COUNTERS = "Guide Hero Counters"
DESCRIPTION_ACADEMY_GUIDE_COUNTERS = "Get counter information for a specific hero."

## /api/academy/guide/{hero_id}/teammates
SUMMARY_ACADEMY_GUIDE_TEAMMATES = "Guide Hero Teammates"
DESCRIPTION_ACADEMY_GUIDE_TEAMMATES = "Get teammate information for a specific hero."

## /api/academy/guide/{hero_id}/trends
SUMMARY_ACADEMY_GUIDE_TRENDS = "Guide Hero Trends"
DESCRIPTION_ACADEMY_GUIDE_TRENDS = "Get trend information for a specific hero."

TITLE_TREND_WINDOW = "Trend Window (Days)"
DESCRIPTION_TREND_WINDOW = "Trend window in days. Allowed: 7, 15, 30."

## /api/academy/guide/{hero_id}/recommended
SUMMARY_ACADEMY_GUIDE_RECOMMENDED = "Guide Hero Recommended Content"
DESCRIPTION_ACADEMY_GUIDE_RECOMMENDED = "Get recommended content for a specific hero."

## /api/academy/hero-ratings
SUMMARY_ACADEMY_HERO_RATINGS = "Hero Ratings Index"
DESCRIPTION_ACADEMY_HERO_RATINGS = "Get a list of all hero ratings."

## /api/academy/hero-ratings/{subject}
SUMMARY_ACADEMY_HERO_RATINGS_SUBJECT = "Hero Ratings by Subject"
DESCRIPTION_ACADEMY_HERO_RATINGS_SUBJECT = "Get hero ratings for a specific subject."

TITLE_RATING_SUBJECT = "Rating Subject"
DESCRIPTION_RATING_SUBJECT = "Rating subject key from the ratings index response."

# =========================
# addon
# =========================

## /api/addon/win-rate
SUMMARY_ADDON_WIN_RATE = "Win Rate Calculator for Consecutive Wins"
DESCRIPTION_ADDON_WIN_RATE = (
    "Calculate the number of consecutive wins needed to reach a target win rate "
    "based on current matches and win rate."
)

TITLE_MATCH_NOW = "Current Matches"
DESCRIPTION_MATCH_NOW = "Current total number of matches played. Must be a non-negative integer."

TITLE_WR_NOW = "Current Win Rate"
DESCRIPTION_WR_NOW = "Current win rate in percent. Range: 0-100."

TITLE_WR_FUTURE = "Target Win Rate"
DESCRIPTION_WR_FUTURE = "Target win rate in percent. Must be greater than current win rate and between 0 and 100."
