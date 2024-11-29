from typing import Dict, List, Optional
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.evolution_store import EvolutionStore

class PatternHistoryManager:
    """Manages pattern evolution and history across the system."""
    
    def __init__(self, store: EvolutionStore):
        self.store = store
        self.active_patterns = {}  # Track currently evolving patterns
        
    async def track_pattern(self, pattern: Dict) -> Dict:
        """Track a pattern's evolution through the system."""
        try:
            # Generate tracking ID
            tracking_id = f"pat_{datetime.now().isoformat()}"
            
            # Initialize pattern state
            pattern_state = {
                'id': tracking_id,
                'pattern': pattern,
                'evolution': {
                    'stage': 'emerging',
                    'strength': pattern.get('strength', 0.0),
                    'depth': pattern.get('depth', 0.0),
                    'themes': [pattern.get('theme', 'general')],
                    'connections': []
                },
                'history': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # Store initial state
            self.active_patterns[tracking_id] = pattern_state
            await self._persist_state(pattern_state)
            
            return pattern_state
            
        except Exception as e:
            print(colored(f"❌ Pattern tracking error: {str(e)}", "red"))
            return {}
            
    async def update_pattern(self, pattern_id: str, updates: Dict) -> Dict:
        """Update a pattern's evolution state."""
        try:
            if pattern_id not in self.active_patterns:
                print(colored(f"❌ Pattern {pattern_id} not found", "yellow"))
                return {}
                
            current = self.active_patterns[pattern_id]
            
            # Archive current state
            current['history'].append({
                'stage': current['evolution']['stage'],
                'strength': current['evolution']['strength'],
                'depth': current['evolution']['depth'],
                'timestamp': current['timestamp']
            })
            
            # Update evolution state
            current['evolution'].update(updates)
            current['timestamp'] = datetime.now().isoformat()
            
            # Persist changes
            await self._persist_state(current)
            
            return current
            
        except Exception as e:
            print(colored(f"❌ Pattern update error: {str(e)}", "red"))
            return {}
            
    async def get_pattern_history(self, pattern_id: str) -> List[Dict]:
        """Get a pattern's evolution history."""
        try:
            if pattern_id not in self.active_patterns:
                return []
                
            pattern = self.active_patterns[pattern_id]
            return pattern['history']
            
        except Exception as e:
            print(colored(f"❌ History retrieval error: {str(e)}", "red"))
            return []
            
    async def _persist_state(self, pattern_state: Dict) -> bool:
        """Persist pattern state to storage."""
        try:
            # Convert to evolution state format
            evolution_state = {
                'timestamp': pattern_state['timestamp'],
                'stage': pattern_state['evolution']['stage'],
                'metrics': {
                    'connection_strength': len(pattern_state['evolution']['connections']) / 5.0,
                    'emergence_strength': pattern_state['evolution']['strength'],
                    'theme_coverage': len(pattern_state['evolution']['themes']) / 4.0,
                    'depth': pattern_state['evolution']['depth']
                },
                'themes': pattern_state['evolution']['themes'],
                'pattern_count': 1,
                'patterns': [pattern_state['pattern']]
            }
            
            return self.store.store_evolution_state(evolution_state)
            
        except Exception as e:
            print(colored(f"❌ Persistence error: {str(e)}", "red"))
            return False 