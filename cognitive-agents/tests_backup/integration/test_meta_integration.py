import pytest
from termcolor import colored
from cognitive_agents.memory.meta_learning import MetaLearning
from cognitive_agents.memory.intentional_memory import IntentionalMemory
from cognitive_agents.memory.question_evolution import QuestionEvolution
from cognitive_agents.community.community_learning import CommunityLearning
from cognitive_agents.integration.meta_integration import MetaIntegration

@pytest.mark.asyncio
class TestMetaIntegration:
    @pytest.fixture
    async def integration(self):
        """Create and return integration."""
        return MetaIntegration(
            memory=IntentionalMemory(),
            questions=QuestionEvolution(),
            community=CommunityLearning()
        )
        
    async def test_natural_integration(self, integration):
        """Test how meta-learning integrates naturally."""
        integration = await integration
        
        interaction = {
            'type': 'question',
            'content': 'How do we learn through pattern recognition and practice?',
            'context': 'learning',
            'understanding': 'Learning involves recognizing patterns and applying them'
        }
        
        result = await integration.integrate_meta_learning(interaction)
        
        print(colored("\n🔄 Testing Meta Integration:", "cyan"))
        print(f"Interaction: {interaction['content']}")
        print(f"Integration Points: {len(result.get('natural_connections', []))}")
        
        # Verify integration components
        assert 'natural_connections' in result, "Missing natural connections"
        assert 'evolution' in result, "Missing evolution data"
        assert 'integration_quality' in result, "Missing quality score"
        
        # Verify evolution data
        evolution = result.get('evolution', {})
        assert 'stage' in evolution, "Missing evolution stage"
        assert 'connection_strength' in evolution, "Missing connection strength"
        assert 'emergence_strength' in evolution, "Missing emergence strength"
        
        # Verify quality
        quality = result.get('integration_quality', 0)
        assert quality > 0, "Integration quality should be positive"