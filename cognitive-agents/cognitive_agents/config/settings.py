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
    }
}

# Database Settings
DB_SETTINGS = {
    'PATH': 'patterns.db',
    'SCHEMA': 'schema.sql'
} 