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
        # Await the fixture first
        enhancer = await enhancer
        
        # Store some thoughts first
        thoughts = [
            "Starting to learn Python",
            "Making progress with coding",
            "Understanding programming patterns"
        ]
        
        print(colored("\n📚 Storing Test Thoughts:", "cyan"))
        for thought in thoughts:
            print(f"  • {thought}")
            await enhancer.memory.store_thought(thought, intent="learning")
        
        # Test enhancement
        new_thought = "Learning Python syntax"
        print(colored("\n🔍 Testing Enhancement:", "cyan"))
        print(f"New thought: {new_thought}")
        
        result = await enhancer.enhance_thought(new_thought, intent="learning")
        
        # Debug output
        print(colored("\n📊 Results:", "green"))
        print(f"Historical context items: {len(result['context']['historical'])}")
        for item in result['context']['historical']:
            print(f"  • {item['thought']} (similarity: {item['similarity']:.2f})")
        
        assert len(result['context']['historical']) > 0
        
    async def test_relevance_scoring(self, enhancer):
        """Test enhanced relevance scoring."""
        enhancer = await enhancer
        
        # Store thoughts with timestamps
        thoughts = [
            ("Learning Python basics", "2 hours ago"),
            ("Understanding programming concepts", "1 day ago"),
            ("Starting to code in Python", "just now")
        ]
        
        print(colored("\n📚 Storing Test Thoughts:", "cyan"))
        for thought, _ in thoughts:
            await enhancer.memory.store_thought(thought, intent="learning")
        
        # Test enhancement
        new_thought = "Learning Python fundamentals"
        result = await enhancer.enhance_thought(new_thought, intent="learning")
        
        print(colored("\n📊 Relevance Analysis:", "green"))
        for item in result['context']['historical']:
            print(f"Thought: {item['thought']}")
            print(f"  Combined Score: {item['combined_score']:.2f}")
            print(f"  Relevance: {item['relevance_level']}")
            print(f"  Recency Score: {item['recency_score']:.2f}")
        
    async def test_relevance_quality(self, enhancer):
        """Test quality of relevance scoring."""
        enhancer = await enhancer
        
        # Store a sequence of related thoughts
        thoughts = [
            "Learning Python basics",
            "Python programming fundamentals",
            "Starting with Python"
        ]
        
        print(colored("\n📚 Storing Test Thoughts:", "cyan"))
        for thought in thoughts:
            await enhancer.memory.store_thought(thought, intent="learning")
        
        # Test with very similar thought
        test_thought = "Learning Python programming"
        print(colored(f"\n🔍 Testing relevance for: {test_thought}", "cyan"))
        
        result = await enhancer.enhance_thought(test_thought, intent="learning")
        
        # Debug output
        print(colored("\n📊 Relevance Results:", "green"))
        for item in result['context']['historical']:
            print(f"Thought: {item['thought']}")
            print(f"  Score: {item['combined_score']:.2f}")
            print(f"  Level: {item['relevance_level']}")
        
        # Verify high relevance match exists
        high_relevance_matches = [
            item for item in result['context']['historical']
            if item['relevance_level'] == 'high'
        ]
        
        assert len(high_relevance_matches) > 0, "Should find at least one high relevance match"
        assert high_relevance_matches[0]['combined_score'] > 0.8, "High relevance match should have high score"
        
    async def test_contrast_relevance(self, enhancer):
        """Test relevance scoring with contrasting thoughts."""
        enhancer = await enhancer
        
        # Store mixed thoughts
        thoughts = [
            ("Learning Python basics", "learning"),
            ("Had coffee this morning", "insight"),  # Unrelated
            ("Python functions tutorial", "learning"),
            ("Weather is nice today", "insight"),    # Unrelated
            ("Python class inheritance", "learning")
        ]
        
        print(colored("\n📚 Storing Mixed Thoughts:", "cyan"))
        for thought, intent in thoughts:
            await enhancer.memory.store_thought(thought, intent=intent)
        
        test_thought = "Learning Python classes"
        result = await enhancer.enhance_thought(test_thought, intent="learning")
        
        # Verify scoring discrimination
        scores = [(item['thought'], item['combined_score']) 
                 for item in result['context']['historical']]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        print(colored("\n📊 Relevance Discrimination:", "green"))
        for thought, score in scores:
            print(f"{thought}: {score:.2f}")
        
        # Python-related thoughts should score higher
        python_scores = [s for t, s in scores if 'python' in t.lower()]
        other_scores = [s for t, s in scores if 'python' not in t.lower()]
        
        assert min(python_scores) > max(other_scores, default=0)
        
    async def test_conceptual_patterns(self, enhancer):
        """Test conceptual pattern recognition."""
        enhancer = await enhancer
        
        # Store thoughts with conceptual relationships
        thoughts = [
            ("Learning Python variables", "learning"),
            ("Understanding variable scope", "learning"),
            ("Variables in programming", "learning"),
            ("Python functions use variables", "learning")
        ]
        
        print(colored("\n📚 Storing Related Thoughts:", "cyan"))
        for thought, intent in thoughts:
            await enhancer.memory.store_thought(thought, intent=intent)
        
        # Test conceptual pattern recognition
        test_thought = "How variables work in Python"
        result = await enhancer.enhance_thought(test_thought, intent="learning")
        
        print(colored("\n🧩 Conceptual Patterns:", "green"))
        for pattern in result['context']['conceptual']:
            print(f"\nConcept: {pattern['concept']['name']}")
            print("Related Thoughts:")
            for thought in pattern['related_thoughts']:
                print(f"  • {thought['content']}")
            print(f"Confidence: {pattern['confidence']:.2f}")
        
        # Verify conceptual patterns
        assert len(result['context']['conceptual']) > 0
        assert any('variable' in p['concept']['name'].lower() 
                  for p in result['context']['conceptual'])