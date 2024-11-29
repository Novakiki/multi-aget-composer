from typing import Dict, List
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.evolution_store import EvolutionStore
from cognitive_agents.memory.pattern_history import PatternHistoryManager

class PatternDemocracy:
    """Enables democratic pattern validation and evolution."""
    
    def __init__(self, store: EvolutionStore):
        self.store = store
        self.history = PatternHistoryManager(store)
        self.active_validations = {}  # Track ongoing validations
        
    async def propose_pattern(self, pattern: Dict) -> Dict:
        """Submit a pattern for community validation."""
        try:
            # Track pattern evolution
            pattern_state = await self.history.track_pattern(pattern)
            
            validation_id = pattern_state['id']
            proposal = {
                'id': validation_id,
                'pattern': pattern,
                'votes': [],
                'comments': [],
                'status': 'proposed',
                'timestamp': datetime.now().isoformat()
            }
            
            self.active_validations[validation_id] = proposal
            return proposal
            
        except Exception as e:
            print(colored(f"❌ Pattern proposal error: {str(e)}", "red"))
            return {} 