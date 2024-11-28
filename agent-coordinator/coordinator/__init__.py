"""Agent coordinator package."""

from .agents.setup.setup_agent import SetupAgent
from .agents.monitor.monitor_agent import MonitorAgent
from .agents.quality.quality_agent import QualityAgent

__version__ = "0.1.0"
__all__ = ['SetupAgent', 'MonitorAgent', 'QualityAgent']
