import pytest
from termcolor import colored
from cognitive_agents.memory.pattern_store import PatternStore
from cognitive_agents.memory.pattern_network import PatternNetwork
from cognitive_agents.memory.pattern_semantics import PatternSemantics

@pytest.mark.asyncio
class TestPatternSemantics:
    @pytest.fixture
    async def semantics(self):
        """Create test semantic understanding system."""
        # Create store and network first
        store = PatternStore("mongodb://localhost:27017")
        store.db = store.client.test_evolution
        await store.patterns.delete_many({})
        
        network = PatternNetwork(
            store=store,
            uri="bolt://localhost:7687",
            user="neo4j",
            password="evolution"
        )
        
        # Create semantics layer
        semantics = PatternSemantics(
            network=network,
            api_key=os.getenv('PINECONE_API_KEY'),
            environment=os.getenv('PINECONE_ENV', 'gcp-starter')
        )
        return semantics
        
    async def test_semantic_understanding(self, semantics):
        """Test semantic pattern understanding."""
        semantics = await semantics  # Await fixture
        
        # Create test patterns
        patterns = [
            {
                'content': 'Learning emerges naturally',
                'type': 'insight',
                'themes': ['learning', 'emergence']
            },
            {
                'content': 'Understanding develops through connections',
                'type': 'insight',
                'themes': ['understanding', 'connection']
            }
        ]
        embeddings = [[0.1] * 384, [0.2] * 384]  # Test embeddings
        
        print(colored("\n🧠 Testing Semantic Understanding:", "cyan"))
        
        # Store and understand patterns
        for pattern, embedding in zip(patterns, embeddings):
            # Store in MongoDB and Neo4j
            pattern_id = await semantics.network.store.store_pattern(pattern)
            await semantics.network.connect_pattern(pattern_id, pattern)
            
            # Build semantic understanding
            similar = await semantics.understand_pattern(pattern_id, embedding)
            print(f"  • Pattern: {pattern['content']}")
            print(f"  • Similar Patterns: {len(similar)}")
            
            assert len(similar) > 0, "Should find similar patterns" 