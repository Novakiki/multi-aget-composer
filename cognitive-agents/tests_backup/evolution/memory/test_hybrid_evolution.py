import pytest
from unittest.mock import Mock, patch, AsyncMock
from contextlib import asynccontextmanager
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.evolution_store import EvolutionStore
from cognitive_agents.memory.pattern_evolution import PatternEvolution
from cognitive_agents.memory.evolution_core import EvolutionCore, EvolutionServices

@pytest.mark.asyncio
class TestHybridEvolution:
    @pytest.fixture
    async def evolution_services(self):
        """Create test services."""
        config = {
            'pinecone': {'api_key': 'test-key', 'environment': 'test'},
            'neo4j': {'uri': 'test', 'user': 'test', 'password': 'test'},
            'mongodb': {'uri': 'test'}
        }
        
        # Configure mock responses
        mock_pc = AsyncMock()
        mock_index_list = Mock()
        mock_index_list.names = Mock(return_value=['pattern-evolution'])
        mock_pc.list_indexes = Mock(return_value=mock_index_list)
        
        mock_pc.Index.return_value.query.return_value.matches = [
            {'id': 'test_1', 'score': 0.9, 'metadata': {'themes': ['learning']}}
        ]
        
        mock_neo4j = AsyncMock()
        mock_neo4j.session.return_value.__aenter__.return_value.run.return_value = [
            {'pattern': {'id': 'test_1'}, 'themes': ['learning']}
        ]
        
        mock_mongo = AsyncMock()
        mock_mongo.evolution.patterns.find_one.return_value = {
            'stage': 'emerging',
            'history': []
        }
        
        services = EvolutionServices(config)
        services._services = {
            'pinecone': mock_pc,
            'neo4j': mock_neo4j,
            'mongodb': mock_mongo
        }
        return services
        
    async def test_natural_evolution(self, evolution_services):
        """Test natural pattern evolution."""
        services = await evolution_services  # Await the fixture
        core = EvolutionCore(services)
        
        # Test pattern creation
        pattern = {
            'content': 'Learning happens naturally',
            'type': 'insight',
            'themes': ['learning', 'evolution']
        }
        embedding = [0.1] * 384
        
        # Track pattern
        pattern_id = await core.track_pattern(pattern, embedding)
        assert pattern_id.startswith('pat_')
        
        # Test pattern retrieval
        similar = await core.find_similar_patterns(embedding)
        assert len(similar) > 0
        assert similar[0]['score'] > 0.8
        
        # Test evolution state
        state = await core.get_pattern_state(pattern_id)
        assert state['stage'] == 'emerging'
        
    async def test_partial_availability(self, evolution_services):
        """Test with only some services available."""
        services = await evolution_services  # Await the fixture
        services._services.pop('mongodb')
        core = EvolutionCore(services)
        
        pattern = {
            'content': 'Learning with partial services',
            'type': 'insight',
            'themes': ['learning']
        }
        embedding = [0.1] * 384
        
        # Should still work with available services
        pattern_id = await core.track_pattern(pattern, embedding)
        assert pattern_id.startswith('pat_')
        
        # MongoDB operations should gracefully handle unavailability
        state = await core.get_pattern_state(pattern_id)
        assert state['stage'] == 'unknown'