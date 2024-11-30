import pytest
from unittest.mock import AsyncMock, MagicMock
from cognitive_agents.memory.pattern_semantics import PatternSemantics
from termcolor import colored
import os

@pytest.mark.asyncio
class TestPatternSemantics:
    @pytest.fixture
    async def semantics(self):
        """Create test semantic understanding system with real Pinecone."""
        mock_network = AsyncMock()
        mock_network.store.get_pattern.return_value = {
            'content': 'Test pattern',
            'themes': ['test'],
            'embedding': [0.1] * 384
        }
        
        # Use real Pinecone
        semantics = PatternSemantics(
            network=mock_network,
            api_key=os.getenv('PINECONE_API_KEY'),
            environment=os.getenv('PINECONE_ENV')
        )
        
        # Store test data first
        await semantics.understand_pattern(
            "test_pat_1",
            [0.1] * 384  # Test embedding
        )
        
        return semantics
        
    async def test_similarity_search(self, semantics):
        """Test semantic similarity search."""
        semantics = await semantics
        
        # Test pattern
        pattern_id = "test_pat_1"
        
        print(colored("\n🔍 Testing Similarity Search:", "cyan"))
        print(f"Pattern: {pattern_id}")
        
        # Find similar patterns
        similar = await semantics.find_similar(pattern_id)
        
        # Verify results
        assert len(similar) > 0
        print(f"Found {len(similar)} similar patterns")