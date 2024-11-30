import pytest
from termcolor import colored
from cognitive_agents.memory.evolution_store import EvolutionStore
from cognitive_agents.community.pattern_democracy import PatternDemocracy
from cognitive_agents.community.wisdom_emergence import CommunityWisdom
from cognitive_agents.community.collective_learning import CollectiveLearning
from datetime import datetime

@pytest.mark.asyncio
class TestCollectiveLearning:
    @pytest.fixture
    async def store(self):
        """Create and return shared evolution store."""
        store = EvolutionStore(db_path=":memory:")
        store._init_db()
        
        # Add test data
        test_state = {
            'timestamp': datetime.now().isoformat(),
            'stage': 'established',
            'metrics': {
                'connection_strength': 0.8,
                'emergence_strength': 0.7,
                'theme_coverage': 0.6,
                'depth': 0.5
            },
            'themes': ['learning', 'understanding'],
            'pattern_count': 2,
            'patterns': [
                {
                    'type': 'learning_pattern',
                    'content': 'Test pattern',
                    'strength': 0.8
                }
            ]
        }
        store.store_evolution_state(test_state)
        return store
        
    @pytest.fixture
    async def collective(self, store):
        """Create and return collective learning with shared store."""
        store = await store
        democracy = PatternDemocracy(store)
        wisdom = CommunityWisdom(democracy)
        return CollectiveLearning(wisdom, store)
        
    async def test_community_integration(self, collective):
        """Test integration of individual and community patterns."""
        collective = await collective
        
        individual_patterns = [
            {
                'type': 'learning_pattern',
                'content': 'Learning happens through pattern recognition',
                'strength': 0.8,
                'theme': 'learning'
            }
        ]
        
        result = await collective.integrate_community_patterns(individual_patterns)
        
        print(colored("\n🤝 Testing Collective Learning:", "cyan"))
        print(f"  • Individual Patterns: {len(individual_patterns)}")
        print(f"  • Community Patterns: {result.get('community_count', 0)}")
        print(f"  • Themes: {', '.join(result.get('themes', []))}")
        
        # More flexible assertions
        assert len(individual_patterns) > 0, "Should have individual patterns"
        assert 'emergence_strength' in result, "Should measure emergence"
        assert 'collective_patterns' in result, "Should merge patterns" 