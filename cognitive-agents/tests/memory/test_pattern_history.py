import pytest
from termcolor import colored
from cognitive_agents.memory.evolution_store import EvolutionStore
from cognitive_agents.memory.pattern_history import PatternHistoryManager

@pytest.mark.asyncio
class TestPatternHistory:
    @pytest.fixture
    async def history(self):
        """Create and return pattern history manager."""
        store = EvolutionStore(db_path=":memory:")
        # Initialize database with tables
        with store._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evolution_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    connection_strength REAL,
                    emergence_strength REAL,
                    theme_coverage REAL,
                    depth REAL,
                    pattern_count INTEGER,
                    growth_rate REAL,
                    trend TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evolution_themes (
                    state_id INTEGER,
                    theme TEXT,
                    FOREIGN KEY(state_id) REFERENCES evolution_states(id)
                )
            """)
        return PatternHistoryManager(store)
        
    async def test_pattern_lifecycle(self, history):
        """Test pattern tracking through its lifecycle."""
        # Await the fixture
        history = await history
        
        # Initial pattern
        pattern = {
            'type': 'learning_pattern',
            'content': 'Learning happens through pattern recognition',
            'strength': 0.8,
            'depth': 0.6,
            'theme': 'learning'
        }
        
        print(colored("\n🔄 Testing Pattern Evolution:", "cyan"))
        
        # Track pattern
        state = await history.track_pattern(pattern)
        print(f"  • Initial Stage: {state['evolution']['stage']}")
        assert state['evolution']['stage'] == 'emerging'
        
        # Update with connections
        update1 = {
            'stage': 'connecting',
            'connections': ['connection1', 'connection2']
        }
        state = await history.update_pattern(state['id'], update1)
        print(f"  • Updated Stage: {state['evolution']['stage']}")
        assert state['evolution']['stage'] == 'connecting'
        
        # Update with more depth
        update2 = {
            'stage': 'developing',
            'depth': 0.8,
            'strength': 0.9
        }
        state = await history.update_pattern(state['id'], update2)
        print(f"  • Final Stage: {state['evolution']['stage']}")
        assert state['evolution']['stage'] == 'developing'
        
        # Check history
        history = await history.get_pattern_history(state['id'])
        print(f"  • History Length: {len(history)}")
        assert len(history) == 2  # Two updates 