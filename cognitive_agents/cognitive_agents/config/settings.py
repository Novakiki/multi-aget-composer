"""Configuration settings for cognitive agents."""

# Pattern Analysis Settings
PATTERN_SETTINGS = {
    'MIN_CONFIDENCE': 0.7,
    'CONFIDENCE_LEVELS': {
        'VERY_HIGH': 0.9,
        'HIGH': 0.8,
        'MODERATE': 0.7
    }
}

# Database Settings
DB_SETTINGS = {
    'PATH': 'patterns.db',
    'SCHEMA': 'schema.sql'
} 