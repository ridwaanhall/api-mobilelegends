"""Package version for OpenMLBB."""
from __future__ import annotations
from typing import Final

from app.core import config

__version__: Final[str] = config.API_VERSION
