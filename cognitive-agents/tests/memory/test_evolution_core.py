import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.evolution_core import EvolutionCore
from cognitive_agents.memory.pattern_evolution import PatternEvolution

@pytest.mark.asyncio
class TestEvolutionCore:
    @pytest.fixture
    async def mock_stores(self):
        """Create mock stores with realistic responses."""
        # Mock Pinecone
        with patch('pinecone.init'), \
             patch('pinecone.Index') as mock_index:
            
            # Simulate semantic matches
            mock_index.query.return_value.matches = [
                {
                    'id': 'pat_1',
                    'score': 0.85,
                    'metadata': {
                        'content': 'Learning through patterns',
                        'themes': ['learning', 'patterns']
                    }
                }
            ]
            
            # Mock Neo4j
            mock_session = AsyncMock()
            mock_session.run.return_value.single.return_value = {
                'p': {'id': 'pat_1', 'content': 'Test pattern'},
                'connections': [
                    {
                        'type': 'HAS_THEME',
                        'node': {'name': 'learning'}
                    }
                ]
            }
            
            mock_graph = AsyncMock()
            mock_graph.session.return_value.__aenter__.return_value = mock_session
            
            # Mock MongoDB
            mock_mongo = AsyncMock()
            mock_mongo.evolution.patterns = AsyncMock()
            
            return {
                'pinecone': mock_index,
                'neo4j': mock_graph,
                'mongo': mock_mongo
            }
            
    @pytest.fixture
    async def evolution(self, mock_stores):
        """Create evolution system with mocked stores."""
        core = EvolutionCore()
        core.pattern_index = mock_stores['pinecone']
        core.graph_db = mock_stores['neo4j']
        core.context = mock_stores['mongo'].evolution.patterns
        return PatternEvolution(core)
        
    async def test_natural_evolution(self, evolution):
        """Test natural pattern evolution across dimensions."""
        # Initial pattern
        pattern = {
            'content': 'Learning happens through pattern recognition',
            'type': 'insight',
            'themes': [
                {'name': 'learning', 'strength': 0.8},
                {'name': 'patterns', 'strength': 0.7}
            ]
        }
        embedding = [0.1] * 384
        
        print(colored("\n🧬 Testing Natural Evolution:", "cyan"))
        
        # 1. Track new pattern
        result = await evolution.track_pattern(pattern, embedding)
        print(f"  • Pattern Created: {result['id']}")
        assert 'semantic' in result['dimensions']
        
        # 2. Find similar patterns
        similar = await evolution.find_similar_patterns(embedding)
        print(f"  • Similar Patterns: {len(similar)}")
        assert len(similar) > 0
        
        # 3. Get knowledge network
        network = await evolution.get_pattern_network(result['id'])
        print(f"  • Network Connections: {len(network['connections'])}")
        assert len(network['connections']) > 0
        
        # 4. Update evolution state
        await evolution.update_pattern_evolution(
            result['id'],
            {
                'stage': 'developing',
                'insight': 'Pattern shows learning progression'
            }
        )
        
        print("  • Evolution: ✅ Semantic  ✅ Network  ✅ Context") 