from typing import Dict, List
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.evolution_store import EvolutionStore
from cognitive_agents.community.wisdom_emergence import CommunityWisdom
from cognitive_agents.community.pattern_democracy import PatternDemocracy

class CollectiveLearning:
    """Enables community-driven learning evolution."""
    
    def __init__(self, wisdom: CommunityWisdom, store: EvolutionStore):
        self.wisdom = wisdom
        self.store = store
        self.democracy = PatternDemocracy(store)
        
    async def integrate_community_patterns(self, individual_patterns: List[Dict]) -> Dict:
        """Integrate individual and community patterns."""
        try:
            # Submit patterns for community validation
            community_results = await self.wisdom.observe_patterns(individual_patterns)
            
            # Get validated patterns from history
            history = self.store.get_evolution_history(limit=10)
            validated_patterns = self._extract_validated_patterns(history)
            
            # Track evolution of individual patterns
            tracked_patterns = []
            for pattern in individual_patterns:
                state = await self.democracy.history.track_pattern(pattern)
                tracked_patterns.append(state['pattern'])
            
            # Combine individual and community insights
            integration = {
                'individual_count': len(tracked_patterns),
                'community_count': len(validated_patterns),
                'themes': community_results['themes'],
                'emergence_strength': community_results['emergence_strength'],
                'collective_patterns': self._merge_patterns(
                    tracked_patterns,
                    validated_patterns
                )
            }
            
            return integration
            
        except Exception as e:
            print(colored(f"❌ Community integration error: {str(e)}", "red"))
            return {} 
        
    def _extract_validated_patterns(self, history: List[Dict]) -> List[Dict]:
        """Extract validated patterns from evolution history."""
        try:
            validated = []
            seen_patterns = set()  # Track unique patterns
            
            for state in history:
                # Get patterns that have evolved
                if state.get('stage') in ['established', 'evolving']:
                    for pattern in state.get('patterns', []):
                        # Use content as unique identifier
                        content = pattern.get('content', '')
                        if content and content not in seen_patterns:
                            seen_patterns.add(content)
                            validated.append(pattern)
            
            return validated
            
        except Exception as e:
            print(colored(f"❌ Pattern extraction error: {str(e)}", "red"))
            return []
            
    def _merge_patterns(self, individual: List[Dict], community: List[Dict]) -> List[Dict]:
        """Merge individual and community patterns."""
        try:
            merged = []
            seen_patterns = set()
            
            # Process individual patterns first
            for pattern in individual:
                content = pattern.get('content', '')
                if content:
                    seen_patterns.add(content)
                    merged.append({
                        **pattern,
                        'source': 'individual',
                        'timestamp': datetime.now().isoformat()
                    })
            
            # Add unique community patterns
            for pattern in community:
                content = pattern.get('content', '')
                if content and content not in seen_patterns:
                    seen_patterns.add(content)
                    merged.append({
                        **pattern,
                        'source': 'community',
                        'timestamp': datetime.now().isoformat()
                    })
            
            return merged
            
        except Exception as e:
            print(colored(f"❌ Pattern merge error: {str(e)}", "red"))
            return []