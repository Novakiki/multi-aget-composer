import logging
from typing import Dict, List
from pinecone import Pinecone, ServerlessSpec
from termcolor import colored

logger = logging.getLogger(__name__)

class PatternSemantics:
    """Semantic understanding for patterns."""
    
    def __init__(self, network, api_key: str, environment: str = "us-central1"):
        self.network = network
        
        # For testing - don't create real client
        if api_key == "test-key":
            self.pc = None
            self.index = None
            return
        
        # Real initialization
        try:
            self.pc = Pinecone(api_key=api_key)
            self.index = self.pc.Index('virtual-limit-interactions')
            print(colored("✓ Pinecone Serverless Connected", "green"))
        except Exception as e:
            logger.error(colored(f"❌ Pinecone Error: {str(e)}", "red"))
            raise
        
    async def understand_pattern(self, pattern_id: str, embedding: List[float]):
        """Build semantic understanding of pattern."""
        try:
            pattern = await self.network.store.get_pattern(pattern_id)
            self.index.upsert([
                (pattern_id, embedding, {
                    'content': pattern['content'],
                    'themes': pattern['themes']
                })
            ])
            return True
        except Exception as e:
            print(colored(f"❌ Semantic error: {str(e)}", "red"))
            return False

    async def find_similar(self, pattern_id: str) -> List[Dict]:
        """Find semantically similar patterns."""
        try:
            pattern = await self.network.store.get_pattern(pattern_id)
            if not pattern or 'embedding' not in pattern:
                return []
                
            # Query with actual embedding
            results = self.index.query(
                vector=pattern['embedding'],
                top_k=5,
                include_metadata=True,
                filter={'id': {'$ne': pattern_id}}  # Exclude self
            )
            
            return results.matches if results else []
            
        except Exception as e:
            logger.error(colored(f"❌ Similarity search error: {str(e)}", "red"))
            return [] 

    async def _create_semantic_connections(self, pattern_id: str, similar_patterns: List[Dict]):
        """Create semantic connections between patterns."""
        try:
            for pattern in similar_patterns:
                await self.network.connect_patterns(
                    pattern_id,
                    pattern['id'],
                    {'similarity': pattern['score']}
                )
        except Exception as e:
            logger.error(f"Failed to create connections: {e}")