"""Monitor Agent - Watches project and coordinates agent activities."""

import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from termcolor import colored
from typing import Dict, Set, Optional
from datetime import datetime
import time

from ...shared.patterns import AgentStatus, AgentPatterns
from ...shared.communication import AgentCommunication
from ...config.agent_standards import AGENT_CONFIG
from ..quality.quality_agent import QualityAgent

class MonitorAgent(FileSystemEventHandler):
    """Agent that monitors project and coordinates other agents."""
    
    def __init__(self):
        self.status = AgentStatus.IDLE
        self.config = AGENT_CONFIG["monitor"]
        self.active_files: Set[str] = set()
        self.last_check = datetime.now()
        
        # Initialize once
        self.comm = AgentCommunication()
        time.sleep(0.1)  # Prevent race condition
        self.quality = QualityAgent()  # Share communication
        
        print(colored("Monitor Agent initialized", "green"))
    
    def start(self, path: str = ".") -> None:
        """Start monitoring the project."""
        try:
            self.status = AgentStatus.WORKING
            self.comm.broadcast_status("monitor", self.status)
            
            print(colored(f"\nStarting project monitor {self.status.value}", "cyan"))
            self.comm.notify_agents("Monitor starting up", "MonitorAgent")
            
            # Set up watchdog
            observer = Observer()
            observer.schedule(self, path, recursive=True)
            observer.start()
            
            # Wait for setup agent
            print(colored("\nWaiting for setup completion...", "cyan"))
            if self.comm.wait_for_signal(AgentPatterns.SETUP_COMPLETE):
                self.status = AgentStatus.IDLE
                self.comm.broadcast_status("monitor", self.status)
                self.comm.notify_agents(AgentPatterns.MONITOR_READY, "MonitorAgent")
            else:
                raise TimeoutError("Setup agent not ready")
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.comm.broadcast_status("monitor", self.status)
            print(colored(f"Monitor failed: {str(e)}", "red"))
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
            
        file_path = event.src_path
        
        # Skip monitoring files and duplicates
        if (file_path.endswith('.json') and 'monitor_config' in file_path) or \
           file_path in self.active_files:
            return
        
        try:
            # Add to active files first
            self.active_files.add(file_path)
            
            # Use relative path for reporting
            rel_path = os.path.basename(file_path)
            
            # Check timing and wait for file system
            now = datetime.now()
            if (now - self.last_check).total_seconds() < self.config["check_interval"]:
                return
                
            time.sleep(1)  # Wait for file system
            if not os.path.exists(file_path):
                return
                
            self.last_check = now
            self.status = AgentStatus.WORKING
            self.comm.broadcast_status("monitor", self.status)
            
            # Notify about change
            self.comm.notify_agents(
                f"File changed: {rel_path}",
                "MonitorAgent",
                priority="high"
            )
            
            # Run quality check
            self.quality.check_file(file_path)
            
            self.status = AgentStatus.IDLE
            self.comm.broadcast_status("monitor", self.status)
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.comm.broadcast_status("monitor", self.status)
            print(colored(f"Error processing {file_path}: {str(e)}", "red"))
            
        finally:
            # Remove from active after processing
            self.active_files.remove(file_path)
