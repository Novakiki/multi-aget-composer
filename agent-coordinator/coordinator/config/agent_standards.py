"""Agent configuration standards."""

AGENT_CONFIG = {
    "setup": {
        "required_dirs": [
            "monitor_config",
            "agents",
            "shared"
        ],
        "required_files": [
            "requirements.txt"
        ]
    },
    "monitor": {
        "check_interval": 1.0,  # seconds
        "ignore_patterns": [
            "*.pyc",
            "__pycache__",
            "*.json"
        ]
    }
}
