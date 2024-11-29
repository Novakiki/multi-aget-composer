"""Configuration module for cognitive agents."""

from .thresholds import CONSCIOUSNESS_THRESHOLDS
from .spawn_config import SPAWN_CONFIG
from .settings import (
    DB_SETTINGS,
    CACHE_SETTINGS,
    PATTERN_SETTINGS,
    PROCESSING_SETTINGS
)

__all__ = [
    'CONSCIOUSNESS_THRESHOLDS',
    'SPAWN_CONFIG',
    'DB_SETTINGS',
    'CACHE_SETTINGS',
    'PATTERN_SETTINGS',
    'PROCESSING_SETTINGS'
] 