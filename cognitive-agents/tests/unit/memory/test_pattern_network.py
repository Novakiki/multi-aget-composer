import pytest
from unittest.mock import AsyncMock
from cognitive_agents.memory.pattern_network import PatternNetwork
from termcolor import colored

pytestmark = pytest.mark.asyncio

@pytest.mark.unit
class TestPatternNetwork:
    @pytest.fixture
    async def network(self):
        """Create test network."""
        mock_store = AsyncMock()
        network = PatternNetwork(
            store=mock_store,
            uri="bolt://localhost:7687",
            user="neo4j",
            password="test"
        )
        network.graph = AsyncMock()
        return network
        
    async def test_pattern_connection(self, network):
        """Test pattern connections."""
        network = await network
        
        pattern = {
            'content': 'Test pattern',
            'themes': ['test']
        }
        
        print(colored("\n🔄 Testing Pattern Network:", "cyan"))
        result = await network.connect_pattern("test_1", pattern)
        assert result is True
        print(colored("✅ Pattern connected", "green")) 