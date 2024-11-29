from typing import Dict, List
from neo4j import AsyncGraphDatabase
from termcolor import colored

class PatternNetwork:
    """Knowledge network for pattern evolution."""
    
    def __init__(self, store, uri="bolt://localhost:7687", 
                 user="neo4j", password="evolution"):
        self.store = store  # MongoDB store from Phase 1
        self.graph = AsyncGraphDatabase.driver(uri, auth=(user, password))
        
    async def connect_pattern(self, pattern_id: str, pattern: Dict):
        """Create pattern node and theme relationships."""
        async with self.graph.session() as session:
            # Create pattern node
            await session.run("""
                CREATE (p:Pattern {
                    id: $id,
                    content: $content,
                    type: $type
                })
            """, id=pattern_id, **pattern)
            
            # Create theme relationships
            for theme in pattern['themes']:
                await session.run("""
                    MATCH (p:Pattern {id: $pattern_id})
                    MERGE (t:Theme {name: $theme})
                    CREATE (p)-[:HAS_THEME]->(t)
                """, pattern_id=pattern_id, theme=theme) 