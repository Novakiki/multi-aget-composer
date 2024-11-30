import pytest
from cognitive_agents.memory.intentional_memory import IntentionalMemory
from termcolor import colored

@pytest.mark.asyncio
class TestIntentionalMemory:
    @pytest.fixture
    async def memory(self):
        """Create and return memory system."""
        return IntentionalMemory()
        
    async def test_basic_storage(self, memory):
        """Test basic thought storage with intent."""
        # Await the fixture first
        memory = await memory
        
        thought = "I want to learn Python programming"
        result = await memory.store_thought(thought, intent="learning")
        
        assert result is not None
        assert 'timestamp' in result
        assert result['intent'] == 'learning'
        
    async def test_intent_classification(self, memory):
        """Test automatic intent classification."""
        # Await the fixture first
        memory = await memory
        
        thoughts = [
            ("I'm studying new concepts", "learning"),
            ("Growing through challenges", "growth"),
            ("Noticing patterns in my behavior", "insight")
        ]
        
        for thought, expected_intent in thoughts:
            result = await memory.store_thought(thought)
            assert result['intent'] == expected_intent
            
        # Add debug output
        print(colored("\n🧠 Intent Classification Results:", "cyan"))
        for thought, expected in thoughts:
            print(f"Thought: {thought}")
            print(f"Expected: {expected}")
            print(f"Actual: {memory.categories[expected].name}")