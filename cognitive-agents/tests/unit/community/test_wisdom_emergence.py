import pytest
from termcolor import colored
from cognitive_agents.memory.evolution_store import EvolutionStore
from cognitive_agents.community.pattern_democracy import PatternDemocracy
from cognitive_agents.community.wisdom_emergence import CommunityWisdom

@pytest.mark.asyncio
class TestWisdomEmergence:
    @pytest.fixture
    async def wisdom(self):
        """Create and return community wisdom."""
        store = EvolutionStore(db_path=":memory:")
        democracy = PatternDemocracy(store)
        return CommunityWisdom(democracy)
        
    async def test_pattern_observation(self, wisdom):
        """Test community pattern observation."""
        # Await the fixture
        wisdom = await wisdom
        
        patterns = [
            {
                'type': 'learning_pattern',
                'content': 'Learning happens through pattern recognition',
                'strength': 0.8,
                'theme': 'learning'
            },
            {
                'type': 'understanding_pattern',
                'content': 'Understanding emerges from connections',
                'strength': 0.7,
                'theme': 'understanding'
            }
        ]
        
        result = await wisdom.observe_patterns(patterns)
        
        print(colored("\n🌱 Testing Wisdom Emergence:", "cyan"))
        print(f"  • Patterns: {len(patterns)}")
        print(f"  • Themes: {', '.join(result['themes'])}")
        
        assert result['proposals'] == len(patterns), "Should propose all patterns"
        assert len(result['themes']) > 0, "Should identify themes"
        assert 'emergence_strength' in result, "Should calculate emergence" 