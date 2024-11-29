import pytest
from unittest.mock import AsyncMock, patch
from cognitive_agents.scripts.validate_evolution_services import validate_evolution_stack

@pytest.mark.asyncio
class TestEvolutionStack:
    @pytest.fixture
    async def mock_services(self):
        """Mock all evolution services."""
        # Mock Pinecone
        mock_pc = AsyncMock()
        mock_pc.list_indexes.return_value.names.return_value = ['pattern-evolution']
        
        # Mock Neo4j
        mock_neo4j = AsyncMock()
        mock_neo4j.session.return_value.__aenter__.return_value.run.return_value.single.return_value = 1
        
        # Mock MongoDB
        mock_mongo = AsyncMock()
        mock_mongo.admin.command.return_value = True
        
        return {
            'pinecone': mock_pc,
            'neo4j': mock_neo4j,
            'mongo': mock_mongo
        }
        
    async def test_full_stack_validation(self, mock_services, monkeypatch):
        """Test validation with all services available."""
        services = await mock_services  # Await the fixture
        
        monkeypatch.setenv('PINECONE_API_KEY', 'test-key')
        monkeypatch.setenv('NEO4J_URI', 'neo4j://localhost')
        monkeypatch.setenv('NEO4J_USER', 'neo4j')
        monkeypatch.setenv('NEO4J_PASSWORD', 'test')
        monkeypatch.setenv('MONGODB_URI', 'mongodb://localhost')
        
        with patch('pinecone.Pinecone', return_value=services['pinecone']), \
             patch('neo4j.AsyncGraphDatabase.driver', return_value=services['neo4j']), \
             patch('motor.motor_asyncio.AsyncIOMotorClient', return_value=services['mongo']):
            
            result = await validate_evolution_stack()
            assert result is True 