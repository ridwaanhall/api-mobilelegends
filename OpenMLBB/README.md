# OpenMLBB Python SDK

OpenMLBB is the official Python SDK for `https://mlbb.rone.dev/api`.

- API base: `https://mlbb.rone.dev/api`
- Docs: `https://mlbb.rone.dev/openmlbb`
- Groups: `academy`, `mlbb`, `user`, `addon`

## Install

```bash
pip install OpenMLBB
```

## Quick Start

```python
from OpenMLBB import OpenMLBB

client = OpenMLBB()

heroes = client.mlbb.heroes(size=5, index=1, order="desc", lang="en")
academy_roles = client.academy.roles(lang="en")
win_rate = client.addon.win_rate_calculator(match_now=100, wr_now=50, wr_future=60)

print(heroes)
print(academy_roles)
print(win_rate)
```

Every SDK method returns API JSON as a Python dictionary.

## Endpoint Coverage

OpenMLBB follows the same route coverage as API routers:

- `academy`: version, heroes, roles, equipment, spells, emblems, ranks, recommendations, ratings
- `mlbb`: heroes list, rank, positions, details, stats, combos, trends, relations, counters, compatibility
- `user`: auth, profile, stats, privacy, season, matches, hero matches, friends
- `addon`: win-rate calculator, IP lookup

See the interactive SDK docs at `https://mlbb.rone.dev/openmlbb` for endpoint-by-endpoint usage examples.

## Common Examples

```python
from OpenMLBB import OpenMLBB

client = OpenMLBB()

# academy
academy_version = client.academy.meta_version(size=20, index=1, order="desc", lang="en")

# mlbb
hero_list = client.mlbb.heroes(size=10, index=1, order="desc", lang="en")

# addon
wr_calc = client.addon.win_rate_calculator(match_now=100, wr_now=50, wr_future=60)

print(academy_version)
print(hero_list)
print(wr_calc)
```

## User-Agent

The default `User-Agent` is:

`RoneAI-OpenMLBB-Python-SDK`

You can override it by passing `user_agent=` to `OpenMLBB(...)`.

## TypeScript Alternative

If your project is using TypeScript or JavaScript, an alternative SDK is available on npm:

```bash
npm install mlbb-sdk
```

Package page: `https://www.npmjs.com/package/mlbb-sdk`
