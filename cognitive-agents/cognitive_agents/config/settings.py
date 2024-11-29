"""Configuration settings for cognitive agents."""

# Pattern Analysis Settings
PATTERN_SETTINGS = {
    'MIN_CONFIDENCE': 0.7,  # Minimum confidence threshold
    'CONFIDENCE_LEVELS': {
        'VERY_HIGH': 0.9,
        'HIGH': 0.8,
        'MODERATE': 0.7
    },
    # Add sequence types
    'SEQUENCE_TYPES': {
        'confidence': ['confident', 'unsure', 'understanding'],
        'frustration': ['frustrat', 'problem', 'issue'],
        'excitement': ['excit', 'can\'t wait', 'incredible']
    },
    # Add pattern weights
    'PATTERN_WEIGHTS': {
        'confidence': {
            'emotional': 1.2,    # Boost emotional patterns
            'behavioral': 1.0,
            'surface': 0.9,
            'meta': 0.9
        },
        'frustration': {
            'emotional': 1.1,
            'behavioral': 1.1,   # Equal weight to emotional/behavioral
            'surface': 0.9,
            'meta': 1.0
        },
        'excitement': {
            'emotional': 1.2,
            'behavioral': 1.0,
            'surface': 0.9,
            'meta': 0.9
        }
    }
}

# Database Settings
DB_SETTINGS = {
    'PATH': 'pattern_store/patterns.db',
    'SCHEMA': 'pattern_store/schema.sql',
    'ENCODING': 'utf-8',
    'TIMEOUT': 30,  # seconds
    'RETRIES': 3    # number of connection retries
}

# Cache Settings
CACHE_SETTINGS = {
    'MAX_AGE_DAYS': 7,          # Expire patterns after 7 days
    'MIN_USE_COUNT': 2,         # Keep patterns used at least twice
    'MAX_CACHE_SIZE': 1000,     # Maximum patterns to store
    'METRICS_ENABLED': True     # Track hit/miss metrics
} 