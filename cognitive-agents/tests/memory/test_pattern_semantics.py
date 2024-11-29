import os
import logging
import pytest
from termcolor import colored
from cognitive_agents.memory.pattern_store import PatternStore
from cognitive_agents.memory.pattern_network import PatternNetwork
from cognitive_agents.memory.pattern_semantics import PatternSemantics
from unittest.mock import AsyncMock, patch, MagicMock

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
class TestPatternSemantics:
    @pytest.fixture
    async def semantics(self):
        """Create test semantic understanding system."""
        # Simple mock setup
        mock_network = AsyncMock()
        mock_network.store.get_pattern.return_value = {
            'content': 'Test pattern',
            'themes': ['learning']
        }
        
        # Create test instance
        semantics = PatternSemantics(
            network=mock_network,
            api_key="test-key"
        )
        
        # Mock just what we need
        semantics.index = AsyncMock()
        semantics.index.query.return_value = {
            'matches': [{'id': 'test_1', 'score': 0.9}]
        }
        
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
            similar = await semantics.index.query(
                vector=embedding,
                top_k=5,
                include_metadata=True
            )
            print(f"  • Pattern: {pattern['content']}")
            print(f"  • Similar Patterns: {len(similar)}")
            
            assert len(similar) > 0, "Should find similar patterns" 