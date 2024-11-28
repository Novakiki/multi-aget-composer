"""Test suite for specialized cognitive agents."""
import pytest
from typing import Dict, List
from cognitive_agents.agents.specialized_agents import (
    PatternAnalyst,
    EmotionalExplorer,
    IntegrationSynthesizer
)
from termcolor import colored

@pytest.mark.asyncio
async def test_agent_collaboration():
    """Test how specialized agents work together."""
    # Setup
    pattern_analyst = PatternAnalyst()
    emotional_explorer = EmotionalExplorer()
    integrator = IntegrationSynthesizer()
    
    thoughts = [
        "I feel excited about this project",
        "The patterns are starting to make sense",
        "I'm seeing deeper connections now"
    ]
    
    results = []
    for thought in thoughts:
        print(f"\n{'='*50}")
        print(f"Processing: {thought}")
        
        # Get different perspectives
        patterns = await pattern_analyst._find_new_patterns(thought)
        emotions = await emotional_explorer._explore_emotional_depth(thought)
        
        # Basic checks
        assert isinstance(patterns, list), "Patterns should be a list"
        assert isinstance(emotions, dict), "Emotions should be a dict"
        
        # Integrate
        synthesis = await integrator.integrate(patterns, emotions)
        results.append(synthesis)
        
        # Verify synthesis
        assert synthesis is not None, "Synthesis should not be None"
        assert 'meta_understanding' in synthesis, "Should have meta understanding"
        
        # Check evolution
        if len(results) > 1:
            assert len(integrator.insight_patterns['evolution']) > 0, "Should track evolution"
    
    # Verify progression
    assert len(results) == len(thoughts), "Should process all thoughts"
    assert len(pattern_analyst.pattern_history) > 0, "Should build pattern history"
    assert len(emotional_explorer.emotional_context['history']) > 0, "Should build emotional context"

@pytest.mark.asyncio
class TestPatternAnalysis:
    @pytest.fixture
    async def analyst(self):
        """Create and return a PatternAnalyst instance."""
        return PatternAnalyst()
    
    @pytest.mark.parametrize("minimal_input", [
        "Ok", "Yes", "Hmm", "...", "?", "Fine"
    ])
    async def test_minimal_inputs(self, analyst, minimal_input):
        """Test handling of minimal inputs."""
        try:
            analyst = await analyst
            print(colored(f"\nTesting minimal input: {minimal_input}", "cyan"))
            result = await analyst._find_new_patterns(minimal_input)
            
            # Assertions with better error messages
            assert isinstance(result, list), f"Expected list, got {type(result)}"
            assert len(result) <= 2, f"Got {len(result)} patterns, expected <= 2"
            
            if result:
                pattern = result[0]
                assert isinstance(pattern, dict), f"Expected dict, got {type(pattern)}"
                assert "category" in pattern, f"Missing 'category' in pattern: {pattern}"
                assert "confidence" in pattern, f"Missing 'confidence' in pattern: {pattern}"
                assert pattern["category"] == "surface", f"Expected 'surface', got {pattern['category']}"
                assert pattern["confidence"] >= 0.7, f"Confidence {pattern['confidence']} below threshold"
                
        except Exception as e:
            print(colored(f"Test failed for input '{minimal_input}': {str(e)}", "red"))
            raise
    
    @pytest.mark.parametrize("complexity,expected_range", [
        ("simple", (1, 2)),
        ("medium", (1, 3))
    ])
    async def test_pattern_stability(self, analyst, complexity, expected_range):
        """Test basic pattern recognition stability."""
        try:
            analyst = await analyst
            
            thoughts = {
                "simple": "I am happy",
                "medium": "I feel good about this project"
            }
            
            results = []
            for _ in range(3):
                patterns = await analyst._find_new_patterns(thoughts[complexity])
                results.append(len(patterns))
                
            min_patterns, max_patterns = expected_range
            assert min_patterns <= min(results) <= max_patterns
            
        except Exception as e:
            print(colored(f"Test failed for {complexity}: {str(e)}", "red"))
            raise

@pytest.mark.asyncio
class TestEmotionalAnalysis:
    """Test emotional analysis capabilities."""
    
    @pytest.fixture
    async def explorer(self):
        return EmotionalExplorer()
    
    @pytest.mark.parametrize("emotion_input", [
        "I am happy",
        "I feel sad",
        "This makes me angry",
        "I'm not sure how I feel"
    ])
    async def test_emotional_recognition(self, explorer, emotion_input):
        """Test basic emotion recognition."""
        explorer = await explorer
        result = await explorer._explore_emotional_depth(emotion_input)
        
        assert result.get('primary_emotion') is not None
        assert result.get('emotional_context') is not None

    async def test_emotional_transitions(self, explorer):
        """Test tracking of emotional transitions."""
        explorer = await explorer
        
        # Process sequence of emotions
        thoughts = [
            "I feel nervous about this",
            "Actually, I'm getting excited",
            "Now I feel confident"
        ]
        
        for thought in thoughts:
            await explorer._explore_emotional_depth(thought)
        
        # Check transitions
        assert len(explorer.emotional_context['transitions']) == 2