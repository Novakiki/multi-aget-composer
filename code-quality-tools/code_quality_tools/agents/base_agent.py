"""Base class for all agents."""

import asyncio
from typing import Dict, Optional
from termcolor import colored

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.status = "idle"
        self.coordinator = None
        print(colored(f"Agent {name} initialized", "green"))
    
    async def handle_message(self, message: Dict) -> Optional[Dict]:
        """Handle incoming messages."""
        raise NotImplementedError("Agents must implement handle_message")
    
    async def send_message(self, message: Dict) -> None:
        """Send message through coordinator."""
        if self.coordinator:
            await self.coordinator.route_message(self.name, message) 