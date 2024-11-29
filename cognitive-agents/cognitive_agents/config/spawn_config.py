"""Configuration for agent spawning behavior."""

SPAWN_CONFIG = {
    'thresholds': {
        'depth_limit': 3,
        'complexity': {
            'min_length': 30,
            'min_words': 5
        },
        'context': {
            'min_size': 2,
            'min_patterns': 5
        }
    },
    'spawn_rules': {
        'max_agents': 5,
        'cooldown_seconds': 1,
        'resource_limit': 0.8
    }
} 