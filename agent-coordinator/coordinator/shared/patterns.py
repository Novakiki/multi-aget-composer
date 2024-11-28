"""Shared patterns and constants for agent coordination."""

from enum import Enum
from typing import Dict, List

class AgentStatus(Enum):
    IDLE = "🔵"
    WORKING = "🟡"
    ERROR = "🔴"

class AgentPatterns:
    """Common patterns for agent coordination."""
    
    SETUP_COMPLETE = "# Setup Agent complete"
    MONITOR_READY = "# Monitor Agent ready"
    QUALITY_CHECK = "# Quality check complete"
    IMPL_DONE = "# Implementation complete"
