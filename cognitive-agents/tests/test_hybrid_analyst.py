import pytest
from cognitive_agents.agents.specialized_agents import HybridPatternAnalyst
from termcolor import colored

@pytest.mark.asyncio
class TestHybridAnalysis:
    """Test hybrid symbolic-vector pattern analysis."""
    
    @pytest.fixture
    async def analyst(self):
        return HybridPatternAnalyst()
    
    async def test_basic_analysis(self, analyst):
        """Test basic hybrid analysis functionality."""
        thought = "I feel anxious about change"
        result = await analyst.analyze_thought(thought)
        
        # Verify structure
        assert 'patterns' in result
        assert 'similar_thoughts' in result
        assert 'synthesis' in result
        
        # Check both analysis types
        assert len(result['patterns']) > 0  # Symbolic patterns
        assert 'interpretable_insights' in result['synthesis']
        
    async def test_vector_similarity(self, analyst):
        """Test vector similarity matching."""
        # Await the analyst fixture first
        analyst = await analyst
        
        # Process related thoughts
        thoughts = [
            "I feel nervous about change",
            "Change makes me anxious",
            "I'm worried about changing things"
        ]
        
        # Add thoughts to memory
        results = []
        for thought in thoughts:
            result = await analyst.analyze_thought(thought)
            results.append(result)
            
            # Add debug output
            print(colored(f"\n🔄 Processing: {thought}", "cyan"))
            print(colored("Similar thoughts found:", "yellow"))
            for similar in result['similar_thoughts']:
                print(f"  • {similar['thought']} (score: {similar['score']:.2f})")
        
        # Check similar thoughts
        last_result = results[-1]
        assert len(last_result['similar_thoughts']) > 0
        
        # Verify similarity scores
        for similar in last_result['similar_thoughts']:
            assert 'score' in similar
            assert similar['score'] > 0.7  # Minimum similarity threshold
            
    async def test_explanation_quality(self, analyst):
        """Test quality of explanations."""
        thought = "I'm learning to handle change better"
        result = await analyst.analyze_thought(thought)
        
        # Check explanation structure
        synthesis = result['synthesis']
        assert 'explanation' in synthesis
        assert len(synthesis['explanation']) > 0
        
        # Verify insight explanations
        for insight in synthesis['interpretable_insights']:
            assert 'explanation' in insight
            assert len(insight['explanation']) > 0
            
        # Verify semantic explanations
        for connection in synthesis['semantic_connections']:
            assert 'explanation' in connection
            assert len(connection['explanation']) > 0 