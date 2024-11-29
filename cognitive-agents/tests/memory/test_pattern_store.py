import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from cognitive_agents.memory.pattern_store import PatternStore
from termcolor import colored

@pytest.mark.asyncio
class TestPatternStore:
    @pytest.fixture
    async def store(self):
        """Create test pattern store."""
        # Use test database
        store = PatternStore("mongodb://localhost:27017")
        store.db = store.client.test_evolution
        
        # Clean before test
        await store.patterns.delete_many({})
        return store
        
    async def test_pattern_emergence(self, store):
        """Test natural pattern emergence."""
        # Await the fixture
        store = await store
        
        pattern = {
            'content': 'Learning happens naturally',
            'type': 'insight',
            'themes': ['learning', 'evolution']
        }
        
        # Store pattern
        pattern_id = await store.store_pattern(pattern)
        assert pattern_id.startswith('pat_')
        
        # Verify storage
        stored = await store.patterns.find_one({'_id': pattern_id})
        assert stored['evolution']['stage'] == 'emerging'
        print(colored(f"\n✨ Pattern emerged: {pattern_id}", "cyan"))
        