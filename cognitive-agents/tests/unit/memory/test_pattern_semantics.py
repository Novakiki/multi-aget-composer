import pytest
from unittest.mock import AsyncMock, MagicMock
from cognitive_agents.memory.pattern_semantics import PatternSemantics
from termcolor import colored

pytestmark = pytest.mark.asyncio

@pytest.mark.unit
class TestPatternSemantics:
    @pytest.fixture
    async def semantics(self):
        """Create test semantics."""
        mock_network = AsyncMock()
        mock_network.store.get_pattern.return_value = {
            'content': 'Test pattern',
            'themes': ['test'],
            'embedding': [0.1] * 384
        }
        
        semantics = PatternSemantics(
            network=mock_network,
            api_key="test-key"  # This triggers test mode
        )
        
        # Mock the index
        mock_index = MagicMock()
        mock_index.upsert = AsyncMock()
        semantics.index = mock_index
        
        return semantics
        
    async def test_semantic_understanding(self, semantics):
        """Test semantic understanding."""
        semantics = await semantics
        
        print(colored("\n🧠 Testing Semantic Understanding:", "cyan"))
        result = await semantics.understand_pattern(
            "test_1",
            [0.1] * 384  # Test embedding
        )
        assert result is True
        assert semantics.index.upsert.called
        print(colored("✅ Pattern understood", "green"))