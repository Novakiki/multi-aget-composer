import pytest
from unittest.mock import AsyncMock
from cognitive_agents.memory.pattern_relationships import PatternRelationships
from termcolor import colored

@pytest.mark.asyncio
class TestPatternRelationships:
    @pytest.fixture
    async def relationships(self):
        """Create test relationship discoverer."""
        mock_store = AsyncMock()
        mock_store.get_pattern.return_value = {
            'content': 'Test pattern',
            'themes': ['learning', 'evolution']
        }
        
        mock_network = AsyncMock()
        mock_network.find_patterns_by_themes.return_value = [
            {'id': 'theme_1', 'score': 0.8}
        ]
        
        mock_semantics = AsyncMock()
        mock_semantics.find_similar.return_value = [
            {'id': 'similar_1', 'score': 0.9}
        ]
        
        return PatternRelationships(
            store=mock_store,
            network=mock_network,
            semantics=mock_semantics
        )
        
    async def test_relationship_discovery(self, relationships):
        """Test natural relationship discovery."""
        # Await fixture
        relationships = await relationships
        
        # Test pattern
        pattern_id = "test_pattern_1"
        
        print(colored("\n🔍 Testing Pattern Relationships:", "cyan"))
        print(f"Pattern: {pattern_id}")
        
        # Discover relationships
        result = await relationships.discover_relationships(pattern_id)
        
        # Verify relationships
        assert len(result['semantic']) > 0
        assert len(result['thematic']) > 0
        
        # Print results
        print(f"Semantic Relations: {len(result['semantic'])}")
        print(f"Thematic Relations: {len(result['thematic'])}") 