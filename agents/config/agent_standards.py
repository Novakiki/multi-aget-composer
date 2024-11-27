"""Standards and thresholds for agent behavior."""

from typing import Dict

AGENT_CONFIG = {
    "setup": {
        "required_dirs": [
            "modules/",
            "monitor_config/",
            "agents/",
            "shared/"
        ],
        "required_files": [
            "default.json",
            "create_project.sh",
            "requirements.txt"
        ]
    },
    "monitor": {
        "check_interval": 1.0,  # seconds
        "max_retries": 3,
        "timeout": 5.0
    }
}
