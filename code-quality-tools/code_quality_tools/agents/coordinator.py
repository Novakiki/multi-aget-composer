"""Agent coordination system."""

import asyncio
from typing import Dict, List, Optional
from termcolor import colored
from .base_agent import BaseAgent

class AgentCoordinator:
    """Coordinates communication between agents."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        print(colored("Agent Coordinator initialized", "green"))
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the coordinator."""
        self.agents[agent.name] = agent
        agent.coordinator = self
        print(colored(f"Registered agent: {agent.name}", "cyan"))
    
    async def route_message(self, sender: str, message: Dict) -> None:
        """Route a message to appropriate agents."""
        try:
            # Add sender info to message
            message['sender'] = sender
            
            # Add to queue for processing
            await self.message_queue.put(message)
            print(colored(f"Message queued from {sender}", "cyan"))
            
        except Exception as e:
            print(colored(f"Error routing message: {str(e)}", "red"))
    
    async def process_messages(self) -> None:
        """Process messages in the queue."""
        try:
            while True:
                # Get message from queue
                message = await self.message_queue.get()
                sender = message.get('sender')
                
                # Route to all other agents
                for name, agent in self.agents.items():
                    if name != sender:  # Don't send back to sender
                        try:
                            response = await agent.handle_message(message)
                            if response:
                                await self.route_message(name, response)
                        except Exception as e:
                            print(colored(f"Error processing message for {name}: {str(e)}", "red"))
                
                # Mark task as done
                self.message_queue.task_done()
                
        except asyncio.CancelledError:
            print(colored("Message processing stopped", "yellow"))
        except Exception as e:
            print(colored(f"Error in message processing: {str(e)}", "red")) 