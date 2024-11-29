import pytest
from termcolor import colored
from cognitive_agents.memory.pattern_store import PatternStore
from cognitive_agents.memory.pattern_network import PatternNetwork

@pytest.mark.asyncio
class TestPatternNetwork:
    @pytest.fixture
    async def network(self):
        """Create test network with store."""
        store = PatternStore("mongodb://localhost:27017")
        store.db = store.client.test_evolution
        await store.patterns.delete_many({})
        
        network = PatternNetwork(
            store=store,
            uri="bolt://localhost:7687",
            user="neo4j",
            password="evolution"
        )
        return network
        
    async def test_pattern_connections(self, network):
        """Test pattern connection and theme relationships."""
        network = await network  # Await fixture
        
        # Create test pattern
        pattern = {
            'content': 'Patterns connect naturally',
            'type': 'insight',
            'themes': ['connection', 'evolution']
        }
        
        # Store in MongoDB first
        pattern_id = await network.store.store_pattern(pattern)
        
        # Create network connections
        await network.connect_pattern(pattern_id, pattern)
        
        # Verify theme relationships
        async with network.graph.session() as session:
            result = await session.run("""
                MATCH (p:Pattern {id: $id})-[:HAS_THEME]->(t:Theme)
                RETURN collect(t.name) as themes
            """, id=pattern_id)
            themes = (await result.single())['themes']
            assert set(themes) == set(['connection', 'evolution'])
            
        print(colored(f"\n🔄 Pattern Network Created", "cyan"))
        print(f"  • Pattern: {pattern_id}")
        print(f"  • Themes: {', '.join(themes)}") 