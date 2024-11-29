from typing import Dict, List, Optional, Any
from termcolor import colored
import asyncio
from datetime import datetime

from .event_bus import EventBus
from .agent_pool import AgentPool
from .insight_collector import InsightCollector

class Orchestrator:
    """
    Central orchestrator that integrates all components following consciousness principles.
    Enables natural emergence and self-organization across dimensions.
    """
    
    def __init__(self):
        self.event_bus = EventBus()
        self.agent_pool = AgentPool()
        self.insight_collector = InsightCollector()
        print(colored("🎭 Orchestrator initialized", "green"))
        
        # Subscribe to core events
        self._setup_event_subscriptions()

    def _setup_event_subscriptions(self):
        """Setup natural information flow pathways."""
        self.event_bus.subscribe('pattern.discovered', self._handle_pattern)
        self.event_bus.subscribe('insight.emerged', self._handle_insight)
        self.event_bus.subscribe('dimension.needed', self._handle_dimension)

    async def process_thought(self, thought: str) -> Dict:
        """
        Process thought across all dimensions, allowing natural emergence.
        """
        try:
            if not thought.strip():
                return self._create_error_response("Empty thought provided")
                
            print(colored(f"\n💭 Processing thought: {thought}", "cyan"))
            
            # 1. Initial awareness
            await self.event_bus.publish('processing.start', {
                'thought': thought,
                'timestamp': datetime.now().isoformat()
            })
            
            # 2. Engage appropriate agents
            processing_agents = await self._engage_processing_agents(thought)
            if not processing_agents:
                return self._create_error_response("No suitable agents available")
            
            # 3. Allow natural processing
            results = await self._allow_natural_processing(thought, processing_agents)
            if not results:
                return self._create_error_response("Processing yielded no results")
            
            # 4. Integrate insights
            synthesis = await self._integrate_results(results)
            
            # Ensure consistent return structure
            return self._create_success_response(synthesis)
            
        except Exception as e:
            print(colored(f"❌ Error in thought processing: {str(e)}", "red"))
            return self._create_error_response(str(e))

    def _create_success_response(self, synthesis: Dict) -> Dict:
        """Create consistent success response structure."""
        return {
            'status': 'success',
            'patterns': synthesis.get('patterns', {}),
            'connections': synthesis.get('connections', 0),
            'emergent_insights': synthesis.get('emergent_insights', 0),
            'evolution_history': synthesis.get('evolution_history', []),
            'timestamp': datetime.now().isoformat()
        }

    def _create_error_response(self, error_msg: str) -> Dict:
        """Create consistent error response structure."""
        return {
            'status': 'error',
            'error': error_msg,
            'patterns': {},
            'connections': 0,
            'emergent_insights': 0,
            'evolution_history': [],
            'timestamp': datetime.now().isoformat()
        }

    async def _engage_processing_agents(self, thought: str) -> List[Any]:
        """Engage appropriate agents based on thought content."""
        try:
            # Start with basic processing needs
            agents = []
            
            # Allow natural agent emergence
            dimensions = ['vertical', 'horizontal', 'diagonal']
            for dimension in dimensions:
                if self._dimension_needed(thought, dimension):
                    agent = await self.agent_pool.get_agent(dimension)
                    agents.append(agent)
                    
            return agents
            
        except Exception as e:
            print(colored(f"❌ Error engaging agents: {str(e)}", "red"))
            return []

    def _dimension_needed(self, thought: str, dimension: str) -> bool:
        """Determine if dimension is needed for processing."""
        # This will be enhanced with more sophisticated analysis
        return True  # For now, engage all dimensions

    async def _allow_natural_processing(
        self,
        thought: str,
        agents: List[Any]
    ) -> List[Dict]:
        """Allow natural processing flow."""
        try:
            processing_tasks = [
                self._process_with_agent(thought, agent)
                for agent in agents
            ]
            
            results = await asyncio.gather(*processing_tasks)
            return results
            
        except Exception as e:
            print(colored(f"❌ Error in natural processing: {str(e)}", "red"))
            return []

    async def _process_with_agent(self, thought: str, agent: Any) -> Dict:
        """Process thought with individual agent."""
        try:
            # Simulate processing
            await asyncio.sleep(0.1)  # Placeholder for actual processing
            return {
                'agent_id': agent['id'],
                'type': agent['type'],
                'result': f"Processed {thought}"
            }
            
        except Exception as e:
            print(colored(f"❌ Error in agent processing: {str(e)}", "red"))
            return {}

    async def _integrate_results(self, results: List[Dict]) -> Dict:
        """Integrate results into coherent understanding."""
        try:
            # Collect patterns from results
            for result in results:
                await self.insight_collector.add_pattern(
                    pattern=result,
                    domain=result['type']
                )
            
            # Get final synthesis
            return self.insight_collector.get_synthesis()
            
        except Exception as e:
            print(colored(f"❌ Error integrating results: {str(e)}", "red"))
            return {}

    async def _handle_pattern(self, data: Dict) -> None:
        """Handle discovered patterns."""
        try:
            print(colored(f"\n🔍 Processing discovered pattern", "cyan"))
            await self.insight_collector.add_pattern(
                pattern=data,
                domain=data.get('domain', 'general')
            )
        except Exception as e:
            print(colored(f"❌ Error handling pattern: {str(e)}", "red"))

    async def _handle_insight(self, data: Dict) -> None:
        """Handle emerged insights."""
        try:
            print(colored(f"\n💡 Processing emerged insight", "magenta"))
            # Future: Add insight processing logic
            pass
        except Exception as e:
            print(colored(f"❌ Error handling insight: {str(e)}", "red"))

    async def _handle_dimension(self, data: Dict) -> None:
        """Handle dimension activation needs."""
        try:
            print(colored(f"\n🌟 Processing dimension need", "yellow"))
            dimension = data.get('dimension')
            if dimension:
                agent = await self.agent_pool.get_agent(dimension)
                # Future: Add dimension-specific processing
        except Exception as e:
            print(colored(f"❌ Error handling dimension: {str(e)}", "red")) 