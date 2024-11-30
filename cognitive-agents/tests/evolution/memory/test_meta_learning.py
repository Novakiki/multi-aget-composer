import pytest
from termcolor import colored
from cognitive_agents.memory.meta_learning import MetaLearning

@pytest.mark.asyncio
class TestMetaLearning:
    @pytest.fixture
    async def meta(self):
        """Create and return meta learning."""
        return MetaLearning()
        
    async def test_natural_awareness(self, meta):
        """Test how meta-awareness emerges naturally."""
        meta = await meta
        
        interaction = {
            'questions': ['How do we learn?', 'What makes learning effective?'],
            'understanding': 'Learning happens through pattern recognition and practice',
            'context': 'learning'
        }
        
        result = await meta.observe_learning(interaction)
        
        print(colored("\n🧠 Testing Meta-Awareness:", "cyan"))
        print(f"Interaction: {interaction['understanding']}")
        print(f"Patterns: {len(result.get('patterns', []))}")
        
        # Verify components exist
        insights = result.get('insights', {})
        assert 'evolution_quality' in insights, "Missing evolution quality"
        assert 'connection_strength' in insights, "Missing connection strength"
        
        # Verify meta-awareness calculation
        assert len(result.get('patterns', [])) > 0, "No patterns detected"
        assert result.get('meta_awareness', 0) > 0.5, "Insufficient meta-awareness score"