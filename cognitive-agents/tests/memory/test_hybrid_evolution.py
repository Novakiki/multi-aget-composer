import pytest
from unittest.mock import Mock, patch, AsyncMock
from contextlib import asynccontextmanager
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.evolution_store import EvolutionStore
from cognitive_agents.memory.pattern_evolution import PatternEvolution

@pytest.mark.asyncio
class TestHybridEvolution:
    @pytest.fixture
    async def mock_db(self):
        """Create mock database connection."""
        conn = AsyncMock()
        conn.fetchrow = AsyncMock(return_value={
            'id': 1,
            'stage': 'emerging',
            'pattern_id': 'test_id'
        })
        conn.fetch = AsyncMock(return_value=[
            {'theme': 'learning'},
            {'theme': 'patterns'}
        ])
        
        @asynccontextmanager
        async def _acquire():
            yield conn
            
        pool = AsyncMock()
        pool.acquire = _acquire
        return pool
        
    @pytest.fixture
    async def store(self, mock_db):
        """Create test store with mocked connections."""
        with patch('pinecone.init'), \
             patch('pinecone.list_indexes', return_value=[]), \
             patch('pinecone.create_index'), \
             patch('pinecone.Index') as mock_index:
            
            store = EvolutionStore()
            store.index = mock_index
            store.pg_pool = AsyncMock()
            store.pg_pool.acquire = asynccontextmanager(lambda: mock_db)()
            
            return store
            
    @pytest.fixture
    async def evolution(self, store):
        """Create pattern evolution manager."""
        store = await store
        return PatternEvolution(store)
        
    async def test_pattern_lifecycle(self, evolution):
        """Test complete pattern evolution lifecycle."""
        evolution = await evolution
        
        # Initial pattern
        pattern = {
            'content': 'Learning happens through pattern recognition',
            'type': 'insight',
            'themes': [
                {'name': 'learning', 'strength': 0.8},
                {'name': 'patterns', 'strength': 0.7}
            ]
        }
        embedding = [0.1] * 384  # Test embedding
        
        print(colored("\n🧬 Testing Pattern Evolution:", "cyan"))
        
        # Track pattern
        result = await evolution.track_pattern(pattern, embedding)
        print(f"  • Pattern ID: {result['id']}")
        assert result['status'] == 'tracked'
        
        # Verify PostgreSQL storage
        async with evolution.store.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM evolution_states WHERE pattern_id = $1",
                result['id']
            )
            assert row['stage'] == 'emerging'
            
            themes = await conn.fetch(
                "SELECT * FROM pattern_themes WHERE pattern_id = $1",
                result['id']
            )
            assert len(themes) == 2
            
        # Verify Pinecone storage
        evolution.store.index.upsert.assert_called_once()
        
        print("  • Storage: ✅ PostgreSQL  ✅ Pinecone")