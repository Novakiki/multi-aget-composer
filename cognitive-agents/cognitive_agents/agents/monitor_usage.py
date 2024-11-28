"""Monitor API usage."""

from typing import Dict
from datetime import datetime
import json
from pathlib import Path

class APIMonitor:
    def __init__(self):
        self.calls = []
        
    async def log_call(self, 
        agent_type: str,
        depth: int,
        call_type: str,
        tokens_used: int
    ):
        """Log an API call."""
        call = {
            "timestamp": datetime.now().isoformat(),
            "agent_type": agent_type,
            "depth": depth,
            "call_type": call_type,
            "tokens": tokens_used
        }
        self.calls.append(call) 