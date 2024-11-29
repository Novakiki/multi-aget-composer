import logging
from typing import Dict, List
from pinecone import Pinecone, ServerlessSpec
from termcolor import colored

logger = logging.getLogger(__name__)

class PatternSemantics:
    """Semantic understanding for patterns."""
    
    def __init__(self, network, api_key: str, environment: str = "gcp-starter"):
        self.network = network
        # Don't create real Pinecone client in tests
        if api_key == "test-key":
            self.pc = None
            self.index = None
            return
            
        try:
            self.pc = Pinecone(api_key=api_key)
            evolution_index = 'pattern-evolution'
            if evolution_index not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=evolution_index,
                    dimension=384,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='gcp',
                        region='asia-southeast1-gcp'
                    )
                )
            self.index = self.pc.Index(evolution_index)
        except Exception as e:
            logger.error(colored(f"❌ Initialization error: {str(e)}", "red"))
            raise
        
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