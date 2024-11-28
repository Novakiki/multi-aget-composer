"""Profile management for spawn configurations."""

from typing import Dict, Optional
from .spawn_config import SPAWN_CONFIG

class ProfileManager:
    def __init__(self):
        self.active_profile = "default"
        self.custom_profiles = {}
    
    def create_profile(self, name: str, settings: Dict) -> None:
        """Create a new spawn profile."""
        self.custom_profiles[name] = {
            **SPAWN_CONFIG["thresholds"],  # Base settings
            **settings  # Custom overrides
        }
        
    def get_thresholds(self) -> Dict:
        """Get active profile thresholds."""
        if self.active_profile == "default":
            return SPAWN_CONFIG["thresholds"]
        return self.custom_profiles.get(
            self.active_profile, 
            SPAWN_CONFIG["thresholds"]
        )
    
    def set_profile(self, name: str) -> None:
        """Switch to a different profile."""
        if name in self.custom_profiles or name in SPAWN_CONFIG["specializations"]:
            self.active_profile = name 