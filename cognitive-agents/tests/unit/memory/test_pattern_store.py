import pytest
from unittest.mock import AsyncMock
from cognitive_agents.memory.pattern_store import PatternStore
from termcolor import colored

pytestmark = [
    pytest.mark.asyncio,  # Mark all tests as async
    pytest.mark.unit      # Mark all tests as unit tests
]

class TestPatternStore:
    @pytest.fixture
    async def store(self):
        """Create test pattern store."""
        store = PatternStore("mongodb://localhost:27017")
        store.patterns = AsyncMock()
        store.patterns.insert_one.return_value = AsyncMock()
        return store
        
    async def test_pattern_storage(self, store):
        """Test pattern storage."""
        # Await the fixture
        store = await store
        
        pattern = {
            'content': 'Test pattern',
            'themes': ['test']
        }
        
        print(colored("\n🧪 Testing Pattern Storage:", "cyan"))
        print(f"Pattern: {pattern['content']}")
        
        # Store pattern
        pattern_id = await store.store_pattern(pattern)
        assert pattern_id.startswith('pat_')
        assert store.patterns.insert_one.called
        print(colored("✅ Pattern stored successfully", "green"))