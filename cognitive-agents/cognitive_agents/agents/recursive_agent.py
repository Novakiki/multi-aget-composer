"""Base class for recursive cognitive agents."""

import asyncio
from typing import Dict, List, Optional
from termcolor import colored

class RecursiveAgent:
    def __init__(self, role: str, depth: int = 0, max_depth: int = 3):
        self.role = role
        self.depth = depth
        self.max_depth = max_depth
        self.sub_agents: List[RecursiveAgent] = []
        self.thoughts: List[Dict] = []
        self.state: Dict = {"active": True}
        
    async def process_thought(self, thought: str) -> Dict:
        """Process a thought and potentially spawn sub-thoughts."""
        try:
            print(colored(f"\n[{self.role} thinking at depth {self.depth}]", "cyan"))
            
            # Record thought
            self.thoughts.append({
                "content": thought,
                "depth": self.depth,
                "timestamp": asyncio.get_event_loop().time()
            })
            
            # Spawn sub-agents if needed
            if self.depth < self.max_depth and self._should_spawn_sub_agent(thought):
                sub_agent = self._create_sub_agent(thought)
                self.sub_agents.append(sub_agent)
                
                # Get sub-agent's perspective
                sub_response = await sub_agent.process_thought(
                    f"Considering from {sub_agent.role}'s perspective: {thought}"
                )
                
                return {
                    "original_thought": thought,
                    "perspective": self.role,
                    "sub_thoughts": sub_response
                }
                
            return {
                "thought": thought,
                "perspective": self.role,
                "depth": self.depth
            }
            
        except Exception as e:
            print(colored(f"Error in {self.role}: {str(e)}", "red"))
            return {"error": str(e)}
    
    def _should_spawn_sub_agent(self, thought: str) -> bool:
        """Determine if thought needs deeper exploration."""
        # Add logic for when to create sub-agents
        return len(thought.split()) > 10  # Simple example
    
    def _create_sub_agent(self, context: str) -> 'RecursiveAgent':
        """Create a new sub-agent."""
        return RecursiveAgent(
            role=f"{self.role}_sub_{len(self.sub_agents)}",
            depth=self.depth + 1,
            max_depth=self.max_depth
        ) 