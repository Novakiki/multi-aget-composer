"""Setup Agent - Creates and validates project structure."""

import os
from pathlib import Path
from termcolor import colored
from typing import Dict, List, Optional

from ...shared.patterns import AgentStatus, AgentPatterns
from ...shared.communication import AgentCommunication
from ...config.agent_standards import AGENT_CONFIG

class SetupAgent:
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
            print(colored("Setup Agent initialized", "green"))
            self._initialized = True
    
    def create_structure(self) -> bool:
        """Create required directories and files."""
        try:
            self.status = AgentStatus.WORKING
            self.comm.broadcast_status("setup", self.status)
            self.comm.notify_agents("Creating project structure", "SetupAgent")
            
            # Create directories
            for dir_path in self.config["required_dirs"]:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                self.comm.notify_agents(f"Created directory: {dir_path}", "SetupAgent")
            
            # Create files
            for file_path in self.config["required_files"]:
                Path(file_path).touch()
                self.comm.notify_agents(f"Created file: {file_path}", "SetupAgent")
            
            # Signal completion
            self.status = AgentStatus.IDLE
            self.comm.broadcast_status("setup", self.status)
            self.comm.notify_agents(AgentPatterns.SETUP_COMPLETE, "SetupAgent")
            return True
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.comm.broadcast_status("setup", self.status)
            print(colored(f"Setup failed: {str(e)}", "red"))
            return False
