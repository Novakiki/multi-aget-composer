"""Tests for specialized cognitive agents."""
from typing import Dict, List
import pytest
from cognitive_agents.agents.specialized_agents import (
    PatternAnalyst,
    EmotionalExplorer,
    IntegrationSynthesizer
)
from cognitive_agents.pattern_store.db import PatternStore
from cognitive_agents.visualization.pattern_viz import PatternVisualizer
from termcolor import colored
import time

@pytest.fixture(autouse=True)
async def cleanup_db():
    """Clean up database before each test."""
    store = PatternStore()
    store.cleanup()
    yield

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

@pytest.mark.asyncio
class TestPatternAdaptability:
    """Test how well patterns adapt to different emotional contexts."""
    
    @pytest.fixture
    async def analyzer(self):
        return PatternAnalyst()
    
    async def test_different_emotional_sequences(self, analyzer):
        """Test pattern recognition across different emotional sequences."""
        try:
            analyzer = await analyzer
            visualizer = PatternVisualizer()
            
            sequences = {
                "confidence": [
                    "I'm really unsure about starting this project",
                    "Starting to understand it better now",
                    "Finally feeling confident about where this is going"
                ],
                "frustration": [
                    "Nothing is working right in this project",
                    "Keep running into the same problems",
                    "Found a way through the issues finally"
                ],
                "excitement": [
                    "Can't wait to begin this new project",
                    "Making incredible progress already",
                    "This turned out even better than I hoped"
                ]
            }
            
            for emotion_type, sequence in sequences.items():
                # Reset state before each sequence
                analyzer.reset_state()
                
                print(colored(f"\n🔄 Testing {emotion_type.title()} Sequence", "cyan"))
                
                # Process thoughts...
                for thought in sequence:
                    result = await analyzer._find_new_patterns(thought)
                    print(colored(f"\n Entry:", "yellow"))
                    print(f"  Thought: {thought}")
                    print(f"  Patterns: {len(result)}")
                    for pattern in result:
                        print(f"    • {pattern['category']}: {pattern['theme']} ({pattern['confidence']:.2f})")
                
                # Get analysis results
                analysis_result = await analyzer._analyze_pattern_correlations()
                
                # Show correlations
                print(colored(f"\n🎯 {emotion_type.title()} Correlations:", "green"))
                for correlation in analysis_result['correlations']:
                    print(f"  • Pattern: {correlation['pattern']}")
                    print(f"    Leads to: {correlation['outcome']}")
                    print(f"    Evidence: {', '.join(correlation['evidence'])}")
                    print(f"    Confidence: {correlation['confidence']:.2f}")
                
                # Show summary ONCE at the end
                if 'summary' in analysis_result:
                    print(colored("\n📊 Final Pattern Summary:", "blue"))
                    total = sum(analysis_result['summary'].values())
                    for category, count in analysis_result['summary'].items():
                        if count > 0:
                            percentage = (count / total) * 100
                            print(f"  {category.title()}: {count} ({percentage:.1f}%)")
                
                # Verify results
                assert len(analysis_result['correlations']) > 0, f"Should find patterns in {emotion_type} sequence"
                assert any(
                    emotion_type.lower() in c['pattern'].lower() or
                    emotion_type.lower() in c['outcome'].lower()
                    for c in analysis_result['correlations']
                ), f"Should identify {emotion_type}-related patterns"
        except Exception as e:
            print(colored(f"Adaptability test failed: {str(e)}", "red"))
            raise

@pytest.mark.asyncio
class TestJournalAnalysis:
    """Test pattern recognition in journal entries."""
    
    @pytest.fixture
    async def analyzer(self):
        return PatternAnalyst()
    
    async def test_journal_entries(self, analyzer):
        """Test analysis of longer, natural journal entries."""
        journal_entries = [
            """Today was a mix of emotions. Started the project feeling overwhelmed 
            by its scope, but as I began breaking it down into smaller pieces, 
            things started clicking. Found myself getting excited about the 
            possibilities, even though there's still so much uncertainty.""",
            
            """Spent the morning wrestling with a particularly challenging problem. 
            Initially felt frustrated and stuck, going in circles. But then had 
            this moment of clarity - stepped back, took a break, and when I 
            returned, saw the solution from a completely different angle. It's 
            interesting how often breakthroughs come after stepping away.""",
            
            """Looking back at the last few weeks, I can see a clear pattern in 
            how I approach challenges. There's always this initial resistance, 
            followed by gradual acceptance, and then usually a creative burst 
            once I fully engage. Starting to understand my own process better."""
        ]
        
        try:
            analyzer = await analyzer
            
            print(colored("\n📔 Testing Journal Analysis", "cyan"))
            
            for entry in journal_entries:
                print(colored("\n📝 Processing Entry:", "yellow"))
                print(f"  {entry[:100]}...")
                
                patterns = await analyzer._find_new_patterns(entry)
                
                print(colored("\n🔍 Detected Patterns:", "green"))
                for pattern in patterns:
                    print(f"  • {pattern['category']}: {pattern['theme']} ({pattern['confidence']:.2f})")
                
                # Verify rich pattern detection
                assert len(patterns) >= 3, "Should detect multiple patterns in rich text"
                assert any(p['category'] == 'meta' for p in patterns), "Should detect meta patterns"
                
            # Analyze overall progression
            analysis = await analyzer._analyze_pattern_correlations()
            
            print(colored("\n📊 Journal Analysis Summary:", "blue"))
            if 'summary' in analysis:
                total = sum(analysis['summary'].values())
                for category, count in analysis['summary'].items():
                    if count > 0:
                        percentage = (count / total) * 100
                        print(f"  {category.title()}: {count} ({percentage:.1f}%)")
            
            # Verify correlations
            assert len(analysis['correlations']) > 0, "Should find pattern correlations"
            
        except Exception as e:
            print(colored(f"Journal analysis failed: {str(e)}", "red"))
            raise

@pytest.mark.asyncio
class TestBatchProcessing:
    """Test batch processing capabilities."""
    
    @pytest.fixture
    async def analyzer(self):
        return PatternAnalyst()
    
    async def test_batch_performance(self, analyzer):
        """Test that batch processing maintains pattern quality."""
        # Await the analyzer fixture first
        analyzer = await analyzer
        
        # Use same text for both to ensure fair comparison
        text = "Starting project phase 1"
        
        # Get individual result
        individual_result = await analyzer._find_new_patterns(text)
        
        # Get batch result
        batch_result = await analyzer._process_entries([text])
        
        # Compare pattern quality
        assert len(batch_result) == len(individual_result)
        assert all(
            p['category'] in [ip['category'] for ip in individual_result]
            for p in batch_result
        )
        
        # Add debug output
        print("\n📊 Pattern Quality Comparison:")
        print("Individual Patterns:")
        for p in individual_result:
            print(f"  • {p['category']}: {p['theme']} ({p['confidence']:.2f})")
        print("\nBatch Patterns:")
        for p in batch_result:
            print(f"  • {p['category']}: {p['theme']} ({p['confidence']:.2f})")

@pytest.mark.asyncio
class TestParallelProcessing:
    """Test parallel processing capabilities."""
    
    @pytest.fixture
    async def analyzer(self):
        return PatternAnalyst()
    
    async def test_parallel_processing(self, analyzer):
        """Test parallel processing maintains deep analysis."""
        analyzer = await analyzer
        
        entries = [
            "Starting the project with careful planning",
            "Making progress through systematic steps",
            "Encountering challenges but staying focused",
            "Finding solutions through collaboration",
            "Reflecting on lessons learned"
        ]
        
        # Process in parallel
        parallel_results = await analyzer._process_entries(entries)
        
        # Process individually for comparison
        individual_results = []
        for entry in entries:
            result = await analyzer._find_new_patterns(entry)
            individual_results.extend(result)
        
        # Compare results
        print("\n📊 Deep Analysis Comparison:")
        print(f"Parallel Processing: {len(parallel_results)} patterns")
        print(f"Individual Processing: {len(individual_results)} patterns")
        
        # Verify deep analysis is maintained
        assert len(parallel_results) >= len(individual_results)
        assert all(
            any(
                p['category'] == ip['category'] and 
                p['confidence'] >= 0.7 and
                len(p['evidence']) > 0
                for ip in individual_results
            )
            for p in parallel_results
        )

@pytest.mark.asyncio
class TestPatternEvolution:
    """Test pattern evolution and sequence analysis capabilities."""
    
    @pytest.fixture
    async def analyst(self):
        return PatternAnalyst()
    
    async def test_sequence_analysis(self, analyst):
        """Test analysis of thought sequences."""
        thoughts = [
            "I feel nervous about change",
            "Starting to understand why change makes me nervous",
            "Noticing a pattern in how I respond to change"
        ]
        
        result = await analyst.analyze_pattern_sequence(thoughts)
        
        # Verify structure
        assert 'sequence_patterns' in result
        assert 'theme_evolution' in result
        assert 'transitions' in result
        assert 'meta_insights' in result
        
        # Verify sequence tracking
        assert len(result['sequence_patterns']) == len(thoughts)
        
        # Verify theme evolution
        themes = result['theme_evolution']
        assert len(themes) > 0
        for theme_data in themes.values():
            assert 'first_seen' in theme_data
            assert 'occurrences' in theme_data
            assert 'confidence_history' in theme_data
            
    async def test_pattern_transitions(self, analyst):
        """Test pattern transition tracking."""
        thoughts = [
            "Change makes me nervous",
            "I'm learning to handle change",
            "Starting to see change as opportunity"
        ]
        
        result = await analyst.analyze_pattern_sequence(thoughts)
        
        # Verify transitions
        transitions = result['transitions']
        assert len(transitions) > 0
        for transition in transitions:
            assert 'from_pattern' in transition
            assert 'to_pattern' in transition
            assert 'confidence' in transition
            
        # Verify progression
        assert len(result['meta_insights']) > 0
        
    async def test_theme_tracking(self, analyst):
        """Test theme evolution tracking."""
        thoughts = [
            "I worry about failure",
            "Failure is part of learning",
            "Learning from failure makes me stronger"
        ]
        
        result = await analyst.analyze_pattern_sequence(thoughts)
        themes = result['theme_evolution']
        
        # Check theme progression
        assert any('failure' in theme.lower() for theme in themes)
        assert any('learning' in theme.lower() for theme in themes)
        
        # Check theme data
        for theme_data in themes.values():
            assert theme_data['occurrences'] > 0
            assert len(theme_data['confidence_history']) > 0
            assert len(theme_data['related_patterns']) > 0