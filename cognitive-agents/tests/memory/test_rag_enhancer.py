import pytest
from cognitive_agents.memory.rag_enhancer import RAGEnhancer
from cognitive_agents.memory.intentional_memory import IntentionalMemory
from termcolor import colored

@pytest.mark.asyncio
class TestRAGEnhancer:
    @pytest.fixture
    async def enhancer(self):
        """Create and return RAG enhancer."""
        memory = IntentionalMemory()
        return RAGEnhancer(memory)
        
    async def test_basic_enhancement(self, enhancer):
        """Test basic thought enhancement."""
        # Await the fixture first
        enhancer = await enhancer
        
        thought = "Learning to code is a journey"
        result = await enhancer.enhance_thought(thought, intent="learning")
        
        print(colored("\n🔍 Enhancement Result:", "cyan"))
        print(f"Thought: {thought}")
        print(f"Context Items: {len(result['context']['historical'])}")
        
        assert result is not None
        assert 'context' in result
        assert 'enhancement' in result
        
    async def test_context_retrieval(self, enhancer):
        """Test context retrieval functionality."""
        # Store some thoughts first
        thoughts = [
            "Starting to learn Python",
            "Making progress with coding",
            "Understanding programming patterns"
        ]
        
        # Store thoughts in memory
        memory = enhancer.memory
        for thought in thoughts:
            await memory.store_thought(thought, intent="learning")
            
        # Test enhancement
        new_thought = "Learning Python syntax"
        result = await enhancer.enhance_thought(new_thought, intent="learning")
        
        assert len(result['context']['historical']) > 0 