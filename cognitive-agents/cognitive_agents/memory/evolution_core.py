from typing import Dict, List
import os
from neo4j import AsyncGraphDatabase
from motor.motor_asyncio import AsyncIOMotorClient
import pinecone
from termcolor import colored
from datetime import datetime

class EvolutionCore:
    """Core evolution engine using tri-database architecture."""
    
    def __init__(self):
        # Semantic Patterns (Pinecone)
        pinecone.init(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment=os.getenv('PINECONE_ENV')
        )
        self.pattern_index = pinecone.Index('pattern-evolution')
        
        # Knowledge Networks (Neo4j)
        self.graph_db = AsyncGraphDatabase.driver(
            os.getenv('NEO4J_URI'),
            auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
        )
        
        # Rich Context (MongoDB)
        self.context_db = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
        self.context = self.context_db.evolution.patterns 
        
    async def store_semantic_pattern(self, pattern_id: str, embedding: List[float], pattern: Dict):
        """Store semantic pattern in Pinecone."""
        metadata = {
            'content': pattern.get('content'),
            'type': pattern.get('type'),
            'themes': [t['name'] for t in pattern.get('themes', [])]
        }
        self.pattern_index.upsert([(pattern_id, embedding, metadata)])
        
    async def create_pattern_node(self, pattern_id: str, pattern: Dict):
        """Create pattern node in knowledge network."""
        async with self.graph_db.session() as session:
            # Create pattern node
            await session.run("""
                CREATE (p:Pattern {
                    id: $id,
                    content: $content,
                    type: $type
                })
            """, id=pattern_id, **pattern)
            
            # Create theme relationships
            for theme in pattern.get('themes', []):
                await session.run("""
                    MATCH (p:Pattern {id: $pattern_id})
                    MERGE (t:Theme {name: $theme})
                    CREATE (p)-[:HAS_THEME {strength: $strength}]->(t)
                """, pattern_id=pattern_id, **theme)
                
    async def store_pattern_context(self, pattern_id: str, pattern: Dict):
        """Store rich pattern context."""
        await self.context.insert_one({
            '_id': pattern_id,
            'pattern': pattern,
            'evolution': {
                'stage': 'emerging',
                'history': [],
                'connections': []
            },
            'metadata': {
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        })