import pytest
from termcolor import colored
from cognitive_agents.integration.meta_integration import MetaIntegration
from cognitive_agents.memory.intentional_memory import IntentionalMemory
from cognitive_agents.memory.question_evolution import QuestionEvolution
from cognitive_agents.community.community_learning import CommunityLearning

@pytest.mark.asyncio
class TestEvolutionPath:
    @pytest.fixture
    async def integration(self):
        """Create and return integration."""
        return MetaIntegration(
            memory=IntentionalMemory(),
            questions=QuestionEvolution(),
            community=CommunityLearning()
        )
        
    async def test_evolution_progression(self, integration):
        """Test how understanding evolves through multiple interactions."""
        # Await the fixture
        integration = await integration
        
        interactions = [
            {
                'type': 'question',
                'content': 'What is learning?',
                'understanding': 'Learning is acquiring knowledge'
            },
            {
                'type': 'question',
                'content': 'How do patterns help learning?',
                'understanding': 'Patterns help organize knowledge'
            },
            {
                'type': 'question',
                'content': 'How do we learn through pattern recognition?',
                'understanding': 'Pattern recognition enables deeper understanding'
            }
        ]
        
        print(colored("\n🔄 Testing Evolution Path:", "cyan"))
        
        results = []
        for interaction in interactions:
            result = await integration.integrate_meta_learning(interaction)
            results.append(result)
            
            print(f"\n📝 Interaction: {interaction['content']}")
            print(f"  Stage: {result['evolution']['stage']}")
            print(f"  Growth Rate: {result['evolution']['progression']['growth_rate']:.2f}")
            print(f"  Trend: {result['evolution']['progression']['trend']}")
            
        # Verify progression
        stages = [r['evolution']['stage'] for r in results]
        assert 'emerging' in stages, "Should start with emerging stage"
        assert stages[-1] in ['developing', 'established'], "Should progress to higher stages"
        
        # Verify growth
        growth_rates = [r['evolution']['progression']['growth_rate'] for r in results]
        assert any(rate > 0 for rate in growth_rates), "Should show positive growth"
        
        # Verify theme development
        final_themes = set(results[-1]['evolution']['themes'])
        assert len(final_themes) >= 2, "Should develop multiple themes" 