# OpenMLBB Python SDK

OpenMLBB is the official Python SDK for `https://mlbb.rone.dev/api`.

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

## User-Agent

The default `User-Agent` is:

`RoneAI-OpenMLBB-Python-SDK`

You can override it by passing `user_agent=` to `OpenMLBB(...)`.
