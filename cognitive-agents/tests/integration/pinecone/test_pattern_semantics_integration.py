import pytest
import os
from cognitive_agents.memory.pattern_semantics import PatternSemantics
from termcolor import colored

pytestmark = pytest.mark.integration

@pytest.mark.asyncio
class TestPatternSemanticsIntegration:
    @pytest.fixture
    async def live_semantics(self):
        """Create live semantic system."""
        # Test just Pinecone, no Neo4j dependency
        semantics = PatternSemantics(
            network=None,  # Don't need network for Pinecone test
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