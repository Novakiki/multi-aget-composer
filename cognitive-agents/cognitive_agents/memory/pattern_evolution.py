from typing import Dict, List, Optional
from datetime import datetime
import asyncpg
import pinecone
from termcolor import colored
import os

class EvolutionStore:
    """Manages pattern evolution across PostgreSQL and Pinecone."""
    
    def __init__(self):
        """Initialize store connections."""
        # PostgreSQL pool
        self.pg_pool = None
        
        # Pinecone initialization
        pinecone.init(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment=os.getenv('PINECONE_ENV')
        )
        self.index_name = 'pattern-evolution'
        self.vector_dim = 384  # OpenAI ada-2 dimension
        
    async def initialize(self):
        """Initialize connections and schemas."""
        try:
            # Initialize PostgreSQL
            self.pg_pool = await asyncpg.create_pool(
                user=os.getenv('PG_USER', 'evolution_user'),
                password=os.getenv('PG_PASSWORD'),
                database=os.getenv('PG_DB', 'evolution_db'),
                host=os.getenv('PG_HOST', 'localhost')
            )
            
            # Create PostgreSQL schema
            async with self.pg_pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS evolution_states (
                        id SERIAL PRIMARY KEY,
                        pattern_id TEXT NOT NULL,
                        timestamp TIMESTAMPTZ NOT NULL,
                        stage TEXT NOT NULL,
                        metrics JSONB,
                        metadata JSONB
                    )
                """)
                
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS pattern_themes (
                        pattern_id TEXT NOT NULL,
                        theme TEXT NOT NULL,
                        strength FLOAT,
                        timestamp TIMESTAMPTZ NOT NULL,
                        PRIMARY KEY (pattern_id, theme)
                    )
                """)
            
            # Initialize Pinecone
            if self.index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=self.index_name,
                    dimension=self.vector_dim,
                    metric='cosine'
                )
            self.index = pinecone.Index(self.index_name)
            
            print(colored("✅ Evolution store initialized", "green"))
            
        except Exception as e:
            print(colored(f"❌ Store initialization error: {str(e)}", "red"))
            raise

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