"""Communication system for agent coordination."""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from termcolor import colored
from datetime import datetime

from .patterns import AgentStatus, AgentPatterns

class AgentCommunication:
    """Handles inter-agent communication and coordination."""
    
    def __init__(self):
        self.message_file = Path("monitor_config/messages.json")
        self.status_file = Path("monitor_config/status.json")
        self.last_message = None  # Track last message
        self._initialize_files()
        print(colored("Communication system initialized", "green"))
    
    def notify_agents(self, message: str, sender: str, priority: str = "normal") -> None:
        """Send a message to all agents."""
        try:
            # Deduplicate messages
            message_key = f"{sender}:{message}"
            if message_key == self.last_message:
                return
            self.last_message = message_key
            
            timestamp = datetime.now().isoformat()
            new_message = {
                "timestamp": timestamp,
                "sender": sender,
                "message": message,
                "priority": priority
            }
            
            messages = self._read_messages()
            messages.append(new_message)
            
            with open(self.message_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, indent=2)
                
            print(colored(f"📢 {sender}: {message}", "cyan"))
            
        except Exception as e:
            print(colored(f"Communication error: {str(e)}", "red"))
    
    def wait_for_signal(self, pattern: str, timeout: float = 5.0) -> bool:
        """Wait for a specific message pattern."""
        try:
            start_time = datetime.now()
            while (datetime.now() - start_time).total_seconds() < timeout:
                messages = self._read_messages()
                for msg in messages:
                    if pattern in msg["message"]:
                        return True
            return False
            
        except Exception as e:
            print(colored(f"Signal wait error: {str(e)}", "red"))
            return False
    
    def broadcast_status(self, agent_name: str, status: AgentStatus) -> None:
        """Update and broadcast agent status."""
        try:
            statuses = self._read_status()
            statuses[agent_name] = {
                "status": status.value,
                "updated": datetime.now().isoformat()
            }
            
            with open(self.status_file, "w", encoding="utf-8") as f:
                json.dump(statuses, f, indent=2)
                
        except Exception as e:
            print(colored(f"Status broadcast error: {str(e)}", "red"))
    
    def _initialize_files(self) -> None:
        """Create communication files if they don't exist."""
        self.message_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.message_file.exists():
            with open(self.message_file, "w", encoding="utf-8") as f:
                json.dump([], f)
                
        if not self.status_file.exists():
            with open(self.status_file, "w", encoding="utf-8") as f:
                json.dump({}, f)
    
    def _read_messages(self) -> List[Dict]:
        """Read message history."""
        try:
            with open(self.message_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    
    def _read_status(self) -> Dict:
        """Read current agent statuses."""
        try:
            with open(self.status_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
