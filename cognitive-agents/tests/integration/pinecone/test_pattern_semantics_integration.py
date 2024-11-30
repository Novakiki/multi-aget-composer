import pytest
import os
from cognitive_agents.memory.pattern_semantics import PatternSemantics
from termcolor import colored
from cognitive_agents.memory.pattern_network import PatternNetwork
from unittest.mock import AsyncMock

pytestmark = pytest.mark.integration

@pytest.mark.asyncio
class TestPatternSemanticsIntegration:
    @pytest.fixture
    async def live_semantics(self):
        """Create live semantic system."""
        # Create mock store for network
        mock_store = AsyncMock()
        mock_store.get_pattern.return_value = {
            'content': 'Test pattern',
            'themes': ['test']
        }
        
        network = PatternNetwork(
            store=mock_store,  # Add mock store
            uri="bolt://localhost:7687",
            user="neo4j",
            password="evolution"
        )
        
        semantics = PatternSemantics(
            network=network,  # Pass network with store
            api_key=os.getenv('PINECONE_API_KEY')
        )
        return semantics
        
    async def test_live_understanding(self, live_semantics):
        """Test real semantic understanding."""
        semantics = await live_semantics
        
        print(colored("\n🌐 Testing Live Semantic Understanding:", "cyan"))
        result = await semantics.understand_pattern(
            "test_live_1",
            [0.1] * 384
        )
        assert result is True
        print(colored("✅ Live pattern understood", "green")) 