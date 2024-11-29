"""Core settings for the cognitive agents system."""

from pathlib import Path

# Get base project directory
BASE_DIR = Path(__file__).parent.parent.parent

DB_SETTINGS = {
    'path': str(BASE_DIR / 'data' / 'patterns.db'),
    'timeout': 30,
    'check_same_thread': False,
    'isolation_level': None
}

CACHE_SETTINGS = {
    'enabled': True,
    'max_size': 1000,
    'ttl_seconds': 3600,
    'metrics_enabled': True
}

PATTERN_SETTINGS = {
    'MIN_CONFIDENCE': 0.7,
    'SEQUENCE_TYPES': {
        'emotional': ['feel', 'emotion', 'mood'],
        'behavioral': ['do', 'act', 'behave'],
        'cognitive': ['think', 'believe', 'understand'],
        'meta': ['notice', 'observe', 'realize']
    },
    'PATTERN_WEIGHTS': {
        'emotional': {
            'emotional': 1.2,
            'behavioral': 0.8,
            'surface': 0.7,
            'meta': 1.0
        }
    }
}

PROCESSING_SETTINGS = {
    'TIMEOUT': 30,  # seconds
    'MAX_RETRIES': 3,
    'BATCH_SIZE': 10
} 