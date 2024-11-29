"""Configuration module for cognitive agents.

See docs/technical/ARCHITECTURE.md for system design
See docs/development/PROCESS_GUIDE.md for implementation details
"""

from .settings import (
    PATTERN_SETTINGS,
    CACHE_SETTINGS,
    DB_SETTINGS,
    PROCESSING_SETTINGS
)

__all__ = [
    'PATTERN_SETTINGS',
    'CACHE_SETTINGS',
    'DB_SETTINGS',
    'PROCESSING_SETTINGS'
] 