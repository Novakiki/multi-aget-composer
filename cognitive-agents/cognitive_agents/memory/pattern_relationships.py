from typing import Dict, List
from termcolor import colored

class PatternRelationships:
    """Natural formation of pattern relationships."""
    
    def __init__(self, store, network, semantics):
        self.store = store
        self.network = network
        self.semantics = semantics
        
    async def discover_relationships(self, pattern_id: str) -> Dict:
        """Discover natural relationships between patterns."""
        print(colored(f"\n🔄 Discovering Relationships for: {pattern_id}", "cyan"))
        
        # 1. Get pattern
        pattern = await self.store.get_pattern(pattern_id)
        
        # 2. Find semantic relationships
        similar = await self.semantics.find_similar(pattern_id)
        
        # 3. Extract theme relationships
        theme_patterns = await self.network.find_patterns_by_themes(pattern['themes'])
        
        return {
            'semantic': similar,
            'thematic': theme_patterns,
            'strength': self._calculate_relationship_strength(similar, theme_patterns)
        }
        
    def _calculate_relationship_strength(self, semantic: List[Dict], thematic: List[Dict]) -> float:
        """Calculate natural relationship strength."""
        if not semantic or not thematic:
            return 0.0
            
        # Average semantic scores
        semantic_strength = sum(p['score'] for p in semantic) / len(semantic)
        
        # Average thematic scores
        thematic_strength = sum(p['score'] for p in thematic) / len(thematic)
        
        # Combined strength
        return (semantic_strength + thematic_strength) / 2