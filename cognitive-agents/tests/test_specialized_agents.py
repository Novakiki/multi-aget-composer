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

    @pytest.mark.parametrize("complex_emotion", [
        "I'm happy but also nervous about this change",
        "Part of me is excited, but I'm also scared",
        "I feel proud yet humbled by this experience",
        "I'm frustrated with the situation but hopeful things will improve",
        "There's a mix of relief and anxiety as I move forward"
    ])
    async def test_complex_emotional_patterns(self, explorer, complex_emotion):
        """Test recognition of complex, mixed emotional patterns."""
        try:
            explorer = await explorer
            result = await explorer._explore_emotional_depth(complex_emotion)
            
            # Verify structure
            assert isinstance(result, dict), "Should return dict"
            assert 'primary_emotion' in result, "Should identify primary emotion"
            assert 'secondary_emotions' in result, "Should identify secondary emotions"
            assert 'emotional_context' in result, "Should provide context"
            
            # Verify complex emotion handling
            assert len(result.get('secondary_emotions', [])) > 0, "Should identify secondary emotions"
            assert result['emotional_context'].get('intensity') is not None, "Should assess emotional intensity"
            
            # Check context building
            context_entry = explorer.emotional_context['history'][-1]
            assert context_entry['thought'] == complex_emotion, "Should store original thought"
            assert context_entry['analysis'] == result, "Should store full analysis"
            
            print(colored("\n🎭 Complex Emotion Analysis:", "blue"))
            print(f"  Primary: {result.get('primary_emotion')}")
            print(f"  Secondary: {', '.join(result.get('secondary_emotions', []))}")
            print(f"  Context: {result['emotional_context'].get('situation')}")
            
        except Exception as e:
            print(colored(f"Complex emotion test failed for: {complex_emotion}", "red"))
            print(colored(f"Error: {str(e)}", "red"))
            raise

    async def test_emotional_journey(self, explorer):
        """Test extended emotional progression and pattern recognition."""
        try:
            explorer = await explorer
            journey = [
                "Starting this new project, feeling optimistic but a bit nervous",
                "Running into some unexpected challenges, getting frustrated",
                "Made a small breakthrough, feeling slightly more hopeful",
                "Still facing issues but learning from them now",
                "Starting to see real progress, confidence growing",
                "Looking back, feeling proud of how far we've come",
                "Ready for the next phase, excited but mindful of lessons learned"
            ]
            
            results = []
            for thought in journey:
                result = await explorer._explore_emotional_depth(thought)
                results.append(result)
                
                print(colored(f"\n📝 Journey Entry:", "cyan"))
                print(f"  Thought: {thought}")
                print(colored("  Analysis:", "magenta"))
                print(f"    Primary: {result.get('primary_emotion')}")
                print(f"    Secondary: {', '.join(result.get('secondary_emotions', []))}")
                print(f"    Context: {result['emotional_context'].get('situation')}")
            
            # Verify progression
            assert len(explorer.emotional_context['history']) == len(journey), "Should track full journey"
            assert len(explorer.emotional_context['transitions']) >= 3, "Should identify major transitions"
            
            # Check theme development
            themes = explorer.emotional_context['themes']
            assert len(themes) > 0, "Should identify emotional themes"
            
            print(colored("\n📊 Journey Analysis:", "green"))
            print(f"  Transitions: {len(explorer.emotional_context['transitions'])}")
            print(f"  Themes Tracked: {len(themes)}")
            print("  Emotional Arc:")
            for i, result in enumerate(results, 1):
                print(f"    {i}. {result.get('primary_emotion')} → {', '.join(result.get('secondary_emotions', []))}")
            
        except Exception as e:
            print(colored(f"Emotional journey test failed: {str(e)}", "red"))
            raise

@pytest.mark.asyncio
class TestPatternCorrelation:
    """Test pattern correlation capabilities."""
    
    @pytest.fixture
    async def analyzer(self):
        return PatternAnalyst()
    
    async def test_emotional_pattern_correlation(self, analyzer):
        """Test recognition of recurring emotional patterns."""
        try:
            analyzer = await analyzer
            
            thought_sequence = [
                "Feeling nervous about starting this project",
                "Made some progress after pushing through the nerves",
                "Another challenge, feeling that familiar nervousness",
                "Breakthrough! The nervous energy helped me focus",
                "Starting to see how my nervousness often leads to progress"
            ]
            
            print(colored("\n🔄 Testing Pattern Correlation", "cyan"))
            print("Processing thought sequence...")
            
            results = []
            total_patterns = 0
            for thought in thought_sequence:
                result = await analyzer._find_new_patterns(thought)
                results.append(result)
                total_patterns += len(result)
                
                print(colored(f"\n📝 Entry:", "yellow"))
                print(f"  Thought: {thought}")
                print(f"  Patterns: {len(result)}")
                
                # Print actual patterns for debugging
                for pattern in result:
                    print(f"    • {pattern['category']}: {pattern['theme']} ({pattern['confidence']:.2f})")
            
            # Verify we're finding patterns
            assert total_patterns > len(thought_sequence), "Should find multiple patterns"
            assert len(analyzer.pattern_history) == total_patterns, "Should store all patterns"
            
            # Check for correlated patterns
            correlations = await analyzer._analyze_pattern_correlations()
            
            print(colored("\n🎯 Pattern Correlations:", "green"))
            for correlation in correlations:
                print(f"  • {correlation['pattern']} → {correlation['outcome']}")
                print(f"    Confidence: {correlation['confidence']:.2f}")
            
            # Verify correlations found
            assert len(correlations) > 0, "Should identify pattern correlations"
            assert any(c['confidence'] > 0.7 for c in correlations), "Should find high-confidence patterns"
            
            print(colored("\n📊 Pattern History:", "blue"))
            for entry in analyzer.pattern_history:
                print(f"  • {entry['category']}: {entry['theme']}")
                print(f"    From: {entry['thought']}")
            
            # Check for correlated patterns
            correlations = await analyzer._analyze_pattern_correlations()
            
            print(colored("\n🎯 Pattern Correlations:", "green"))
            for correlation in correlations:
                print(f"  • Pattern: {correlation['pattern']}")
                print(f"    Leads to: {correlation['outcome']}")
                print(f"    Evidence: {', '.join(correlation['evidence'])}")
                print(f"    Confidence: {correlation['confidence']:.2f}")
                print(f"    Occurrences: {correlation['occurrences']}")
            
            # Verify correlations found
            assert len(correlations) > 0, "Should identify pattern correlations"
            assert any(
                'nervousness' in c['pattern'].lower() and 'progress' in c['outcome'].lower() 
                for c in correlations
            ), "Should identify nervousness-progress pattern"
            
        except Exception as e:
            print(colored(f"Pattern correlation test failed: {str(e)}", "red"))
            raise