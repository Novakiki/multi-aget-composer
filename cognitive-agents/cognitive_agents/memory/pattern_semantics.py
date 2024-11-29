from typing import Dict, List
import pinecone
from termcolor import colored

class PatternSemantics:
    """Semantic understanding for patterns."""
    
    def __init__(self, network, api_key: str, environment: str = "gcp-starter"):
        self.network = network  # Pattern network from Phase 2
        pinecone.init(api_key=api_key, environment=environment)
        self.index = pinecone.Index('pattern-evolution')
        
    async def understand_pattern(self, pattern_id: str, embedding: List[float]):
        """Build semantic understanding of pattern."""
        try:
            # Store embedding
            pattern = await self.network.store.get_pattern(pattern_id)
            self.index.upsert([
                (pattern_id, embedding, {
                    'content': pattern['content'],
                    'themes': pattern['themes']
                })
            ])
            
            # Find similar patterns
            similar = self.index.query(
                vector=embedding,
                top_k=5,
                include_metadata=True
            )
            
            # Update network with semantic relationships
            await self._create_semantic_connections(pattern_id, similar.matches)
            
            return similar.matches
            
        except Exception as e:
            print(colored(f"❌ Semantic error: {str(e)}", "red"))
            return [] 