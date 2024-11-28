"""Spawn configuration settings."""

SPAWN_CONFIG = {
    "thresholds": {
        "pattern_weight": 0.2,
        "pattern_cap": 0.4,
        "depth_chars": 200,
        "depth_score": 0.3,
        "meta_chars": 150,
        "meta_score": 0.3,
        "total_required": 0.7
    },
    
    "specializations": {
        "therapy": {
            "pattern_weight": 0.3,  # More pattern sensitive
            "depth_chars": 150,     # Lower depth requirement
            "total_required": 0.6   # Easier spawning
        },
        "analysis": {
            "pattern_weight": 0.1,  # Less pattern sensitive
            "depth_chars": 250,     # Higher depth requirement
            "total_required": 0.8   # Harder spawning
        }
    }
} 