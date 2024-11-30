import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from cognitive_agents.memory.pattern_store import PatternStore
from termcolor import colored

@pytest.mark.asyncio
class TestPatternStore:
    @pytest.fixture
    async def store(self):
        """Create test store with mocked dependencies."""
        store = PatternStore("mongodb://localhost:27017")
        
        # Mock MongoDB
        store.patterns.insert_one = AsyncMock()
        store.patterns.find_one = AsyncMock(return_value={
            'content': 'Test pattern',
            'themes': ['test']
        })
        
        # Mock embeddings
        store.embeddings.generate = MagicMock(return_value=[0.1] * 384)
        
        # Mock semantics
        store.semantics = AsyncMock()
        store.semantics.store_embedding = AsyncMock()
        
        return store
        
    async def test_pattern_storage(self, store):
        """Test storing pattern with embedding."""
        # Await the fixture first
        store = await store
        
        # Test pattern
        pattern = {
            'content': 'How do patterns emerge?',
            'themes': ['patterns', 'evolution']
        }
        
        print(colored("\n🧪 Testing Pattern Storage:", "cyan"))
        print(f"Pattern: {pattern['content']}")
        
        # Store pattern
        pattern_id = await store.store_pattern(pattern)
        
        # Verify storage
        assert pattern_id.startswith('pat_')
        assert store.patterns.insert_one.called
        assert store.semantics.store_embedding.called
        
        print(colored("✅ Pattern stored with embedding", "green"))
        