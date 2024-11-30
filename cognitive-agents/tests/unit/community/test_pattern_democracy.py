import pytest
from termcolor import colored
from cognitive_agents.memory.evolution_store import EvolutionStore
from cognitive_agents.community.pattern_democracy import PatternDemocracy

@pytest.mark.asyncio
class TestPatternDemocracy:
    @pytest.fixture
    async def democracy(self):
        """Create and return pattern democracy."""
        store = EvolutionStore(db_path=":memory:")  # Use in-memory DB for tests
        return PatternDemocracy(store)
        
    async def test_pattern_proposal(self, democracy):
        """Test pattern proposal process."""
        democracy = await democracy
        
        pattern = {
            'type': 'learning_pattern',
            'content': 'Learning happens through pattern recognition',
            'strength': 0.8,
            'theme': 'learning'
        }
        
        result = await democracy.propose_pattern(pattern)
        
        print(colored("\n🗳️ Testing Pattern Democracy:", "cyan"))
        print(f"  • Pattern: {pattern['content']}")
        print(f"  • Status: {result['status']}")
        
        assert result['id'].startswith('val_'), "Should have validation ID"
        assert result['pattern'] == pattern, "Should store original pattern"
        assert result['status'] == 'proposed', "Should start as proposed"
        assert len(result['votes']) == 0, "Should start with no votes" 