from typing import Dict, List, Optional, Any
from termcolor import colored
import asyncio
from datetime import datetime

class AgentPool:
    """
    Dynamic agent pool for efficient resource management.
    Enables agent reuse and optimal resource allocation.
    """
    
    def __init__(self):
        self.available_agents: Dict[str, List[Any]] = {}  # Type -> [agents]
        self.active_agents: Dict[str, Any] = {}  # ID -> agent
        self.performance_metrics: Dict[str, Dict] = {}
        print(colored("🏊 Agent Pool initialized", "green"))

    async def get_agent(self, agent_type: str, requirements: Optional[Dict] = None) -> Any:
        """
        Get an agent of specified type, reusing if available.
        
        Args:
            agent_type: Type of agent needed
            requirements: Optional specific requirements
        """
        try:
            print(colored(f"\n🔍 Requesting agent: {agent_type}", "cyan"))
            
            # Check for available agent
            if self._has_available_agent(agent_type, requirements):
                agent = self._get_available_agent(agent_type, requirements)
                print(colored("♻️  Reusing existing agent", "green"))
            else:
                agent = await self._create_new_agent(agent_type, requirements)
                print(colored("🆕 Created new agent", "yellow"))
            
            # Track activation
            self._activate_agent(agent)
            return agent
            
        except Exception as e:
            print(colored(f"❌ Error getting agent: {str(e)}", "red"))
            return None

    async def release_agent(self, agent_id: str) -> None:
        """
        Release an agent back to the pool.
        
        Args:
            agent_id: ID of agent to release
        """
        try:
            if agent_id in self.active_agents:
                agent = self.active_agents[agent_id]
                agent_type = self._get_agent_type(agent)
                
                # Return to available pool
                if agent_type not in self.available_agents:
                    self.available_agents[agent_type] = []
                self.available_agents[agent_type].append(agent)
                
                # Remove from active
                del self.active_agents[agent_id]
                print(colored(f"♻️  Agent {agent_id} returned to pool", "green"))
                
        except Exception as e:
            print(colored(f"❌ Error releasing agent: {str(e)}", "red"))

    def _has_available_agent(self, agent_type: str, requirements: Optional[Dict]) -> bool:
        """Check if suitable agent is available."""
        if agent_type not in self.available_agents:
            return False
        return len(self.available_agents[agent_type]) > 0

    def _get_available_agent(self, agent_type: str, requirements: Optional[Dict]) -> Any:
        """Get an available agent matching requirements."""
        agents = self.available_agents[agent_type]
        agent = agents.pop()  # Get last agent
        return agent

    async def _create_new_agent(self, agent_type: str, requirements: Optional[Dict]) -> Any:
        """Create a new agent of specified type."""
        # This will be expanded based on agent types
        # For now, return placeholder
        return {
            'id': f"{agent_type}_{datetime.now().timestamp()}",
            'type': agent_type,
            'requirements': requirements
        }

    def _activate_agent(self, agent: Any) -> None:
        """Track agent activation and metrics."""
        agent_id = agent['id']
        self.active_agents[agent_id] = agent
        
        # Initialize metrics
        self.performance_metrics[agent_id] = {
            'activated_at': datetime.now().isoformat(),
            'reuse_count': 0,
            'processing_time': []
        }

    def _get_agent_type(self, agent: Any) -> str:
        """Get type of agent."""
        return agent['type']

    def get_pool_stats(self) -> Dict:
        """Get current pool statistics."""
        # Initialize available dict if empty
        if not self.available_agents:
            self.available_agents = {
                agent_type: [] for agent_type in set(
                    self._get_agent_type(agent) for agent in self.active_agents.values()
                )
            }
        
        return {
            'available': {
                agent_type: len(agents)
                for agent_type, agents in self.available_agents.items()
            },
            'active': len(self.active_agents),
            'metrics': self.performance_metrics
        } 