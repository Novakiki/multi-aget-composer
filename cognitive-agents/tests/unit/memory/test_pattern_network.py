import pytest
from unittest.mock import AsyncMock
from cognitive_agents.memory.pattern_network import PatternNetwork
from termcolor import colored

pytestmark = [
    pytest.mark.asyncio(loop_scope="function"),
    pytest.mark.unit
]

class TestPatternNetwork:
    @pytest.fixture
    async def network(self):
        """Create test network."""
        network = PatternNetwork(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="evolution"
        )
        
        # Create session with proper async context manager
        session = AsyncMock()
        session.__aenter__ = AsyncMock(return_value=session)
        session.__aexit__ = AsyncMock()
        session.run = AsyncMock(return_value=AsyncMock())
        
        # Mock the driver
        network.driver = AsyncMock()
        network.driver.session = AsyncMock(return_value=session)
        
        return network
        
    async def test_pattern_connection(self, network):
        """Test pattern connections."""
        # Await the network fixture
        network = await network
        
        pattern = {
            'content': 'Test pattern',
            'themes': ['test']
        }
        
        print(colored("\n🔄 Testing Pattern Network:", "cyan"))
        result = await network.connect_pattern("test_1", pattern)
        assert result is True
        print(colored("✅ Pattern connected", "green"))