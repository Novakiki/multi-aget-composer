from typing import Dict, List, Optional
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.evolution_services import EvolutionServices

class EvolutionCore:
    """Core evolution engine using service locator pattern."""
    
    def __init__(self, services: Optional[EvolutionServices] = None):
        self.services = services or EvolutionServices()
        self._ensure_evolution_index()
        
    def _ensure_evolution_index(self):
        """Ensure evolution index exists."""
        if self.services.is_available('pinecone'):
            pc = self.services.get_service('pinecone')
            evolution_index = 'pattern-evolution'
            
            if evolution_index not in pc.list_indexes().names():
                pc.create_index(
                    name=evolution_index,
                    dimension=384,
                    metric='cosine'
                )
            self.pattern_index = pc.Index(evolution_index)
        
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
        
    async def track_pattern(self, pattern: Dict, embedding: List[float]) -> str:
        """Track pattern across all dimensions."""
        try:
            pattern_id = f"pat_{datetime.now().isoformat()}"
            
            # 1. Store semantic pattern
            if self.services.is_available('pinecone'):
                pc = self.services.get_service('pinecone')
                pc.Index('pattern-evolution').upsert([
                    (pattern_id, embedding, {
                        'content': pattern['content'],
                        'type': pattern['type'],
                        'themes': pattern['themes']
                    })
                ])
            
            # 2. Create knowledge graph
            if self.services.is_available('neo4j'):
                async with self.services.get_service('neo4j').session() as session:
                    await session.run("""
                        CREATE (p:Pattern {
                            id: $id, content: $content, type: $type
                        })
                    """, id=pattern_id, **pattern)
                    
                    for theme in pattern['themes']:
                        await session.run("""
                            MATCH (p:Pattern {id: $pattern_id})
                            MERGE (t:Theme {name: $theme})
                            CREATE (p)-[:HAS_THEME]->(t)
                        """, pattern_id=pattern_id, theme=theme)
            
            # 3. Store evolution context
            if self.services.is_available('mongodb'):
                await self.services.get_service('mongodb').evolution.patterns.insert_one({
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
            
            return pattern_id
            
        except Exception as e:
            print(colored(f"❌ Pattern tracking error: {str(e)}", "red"))
            raise
            
    async def find_similar_patterns(self, embedding: List[float], top_k: int = 5) -> List[Dict]:
        """Find semantically similar patterns."""
        if self.services.is_available('pinecone'):
            pc = self.services.get_service('pinecone')
            results = pc.Index('pattern-evolution').query(
                vector=embedding,
                top_k=top_k,
                include_metadata=True
            )
            return results.matches
        return []
        
    async def get_pattern_state(self, pattern_id: str) -> Dict:
        """Get pattern's evolution state."""
        if self.services.is_available('mongodb'):
            mongo = self.services.get_service('mongodb')
            state = await mongo.evolution.patterns.find_one({'_id': pattern_id})
            return state['evolution'] if state else {'stage': 'unknown'}
        return {'stage': 'unknown'}