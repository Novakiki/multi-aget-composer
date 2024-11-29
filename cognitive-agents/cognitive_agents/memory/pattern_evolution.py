from typing import Dict, List
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.evolution_core import EvolutionCore
from cognitive_agents.memory.evolution_services import EvolutionServices

class PatternEvolution:
    """Enhanced pattern evolution using tri-database architecture."""
    
    def __init__(self, core: EvolutionCore):
        self.core = core
        
    async def track_pattern(self, pattern: Dict, embedding: List[float]) -> Dict:
        """Track pattern across all dimensions."""
        try:
            # Generate ID
            pattern_id = f"pat_{datetime.now().isoformat()}"
            
            # Store semantic pattern
            await self.core.store_semantic_pattern(
                pattern_id, embedding, pattern
            )
            
            # Create knowledge network
            await self.core.create_pattern_node(
                pattern_id, pattern
            )
            
            # Store rich context
            await self.core.store_pattern_context(
                pattern_id, pattern
            )
            
            return {
                'id': pattern_id,
                'status': 'tracked',
                'dimensions': ['semantic', 'network', 'context']
            }
            
        except Exception as e:
            print(colored(f"❌ Pattern evolution error: {str(e)}", "red"))
            return {}
        
    async def find_similar_patterns(self, embedding: List[float], top_k: int = 5) -> List[Dict]:
        """Find semantically similar patterns."""
        results = self.core.pattern_index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )
        return results.matches
        
    async def get_pattern_network(self, pattern_id: str) -> Dict:
        """Get pattern's knowledge network."""
        async with self.core.graph_db.session() as session:
            result = await session.run("""
                MATCH (p:Pattern {id: $id})-[r]-(n)
                RETURN p, collect({type: type(r), node: n}) as connections
            """, id=pattern_id)
            return await result.single()
            
    async def update_pattern_evolution(self, pattern_id: str, updates: Dict):
        """Update pattern's evolution state."""
        await self.core.context.update_one(
            {'_id': pattern_id},
            {
                '$push': {'evolution.history': updates},
                '$set': {
                    'evolution.stage': updates['stage'],
                    'metadata.updated_at': datetime.now()
                }
            }
        )