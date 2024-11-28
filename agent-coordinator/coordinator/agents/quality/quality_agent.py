"""Quality Agent - Monitors and reports on code quality."""

import os
import sys
from pathlib import Path
from termcolor import colored
from typing import Dict, Optional

# Add code-quality-tools to path
REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent
QUALITY_TOOLS_PATH = REPO_ROOT / 'code-quality-tools'
sys.path.append(str(QUALITY_TOOLS_PATH))

from ...shared.patterns import AgentStatus, AgentPatterns
from ...shared.communication import AgentCommunication
from quality_monitor.quality_monitor import QualityMonitor
from ...config.quality_standards import QUALITY_CHECKS, FILE_TYPES

class QualityAgent:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.status = AgentStatus.IDLE
            self.comm = AgentCommunication()
            self.monitor = QualityMonitor()
            print(colored("Quality Agent initialized", "green"))
            self._initialized = True
    
    def check_file(self, file_path: str) -> None:
        """Check quality of a specific file."""
        try:
            self.status = AgentStatus.WORKING
            self.comm.broadcast_status("quality", self.status)
            
            # Get file type and priority
            ext = Path(file_path).suffix
            file_type = next(
                (t for t, cfg in FILE_TYPES.items() 
                 if ext in cfg["extensions"]), 
                "unknown"
            )
            priority = FILE_TYPES.get(file_type, {}).get("priority", "low")
            
            # Run checks
            rel_path = os.path.relpath(file_path)
            self.monitor.check_file(file_path)
            report = self.monitor.generate_report()
            
            # Get learning stats
            confidence = self.monitor.learning_system._calculate_learning_confidence()
            checks = FILE_TYPES.get(file_type, {}).get("checks", [])
            
            formatted_report = (
                f"Quality Report for {rel_path} ({file_type})\n"
                f"{'=' * 50}\n\n"
                f"Running Checks: {', '.join(checks)}\n\n"
                f"{report}\n\n"
                f"Learning Status:\n"
                f"- Confidence: {confidence:.2f}\n"
                f"- Priority: {priority}\n"
            )
            
            self.comm.notify_agents(
                formatted_report,
                "QualityAgent",
                priority=priority
            )
            
            self.status = AgentStatus.IDLE
            self.comm.broadcast_status("quality", self.status)
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.comm.broadcast_status("quality", self.status)
            print(colored(f"Quality check failed: {str(e)}", "red"))
