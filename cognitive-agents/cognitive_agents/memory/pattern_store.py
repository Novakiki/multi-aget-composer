from typing import Dict, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from termcolor import colored
from .embeddings import EmbeddingGenerator

class PatternStore:
    """Basic pattern storage and evolution tracking."""
    
    def __init__(self, mongodb_uri: str = "mongodb://localhost:27017"):
        """Initialize with MongoDB."""
        self.client = AsyncIOMotorClient(mongodb_uri)
        self.db = self.client.evolution
        self.patterns = self.db.patterns
        self.embeddings = EmbeddingGenerator()
        
    async def store_pattern(self, pattern: Dict) -> str:
        """Store pattern with real embeddings."""
        try:
            pattern_id = f"pat_{datetime.now().isoformat()}"
            
            # Generate real embedding
            embedding = self.embeddings.generate(pattern['content'])
            
            # Store complete pattern
            await self.patterns.insert_one({
                '_id': pattern_id,
                'content': pattern['content'],
                'themes': pattern['themes'],
                'embedding': embedding,
                'metadata': {
                    'created_at': datetime.now(),
                    'type': 'question',
                    'version': '1.0'
                }
            })
            
            # Also store in Pinecone for semantic search
            await self.semantics.store_embedding(
                pattern_id, 
                embedding, 
                {'content': pattern['content'], 'themes': pattern['themes']}
            )
            
            print(colored(f"✨ Pattern {pattern_id} stored with embedding", "green"))
            return pattern_id
            
        except Exception as e:
            print(colored(f"❌ Storage error: {str(e)}", "red"))
            raise 

    async def find_patterns_by_content(self, content: str) -> List[Dict]:
        """Find patterns by content similarity."""
        try:
            # Simple text search for now
            cursor = self.patterns.find({
                'content': {'$regex': content, '$options': 'i'}
            })
            patterns = await cursor.to_list(length=5)
            
            if not patterns:
                # Return empty list if no matches
                return []
                
            return patterns
            
        except Exception as e:
            logger.error(colored(f"❌ Pattern search error: {str(e)}", "red"))
            return []

    async def get_pattern(self, pattern_id: str) -> Dict:
        """Get a pattern by ID."""
        try:
            pattern = await self.patterns.find_one({'_id': pattern_id})
            if not pattern:
                print(colored(f"Pattern not found: {pattern_id}", "yellow"))
                return {}
            return pattern
        except Exception as e:
            print(colored(f"❌ Pattern retrieval error: {str(e)}", "red"))
            return {}