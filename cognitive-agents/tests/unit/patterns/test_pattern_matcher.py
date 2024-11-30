import pytest
from datetime import datetime
from cognitive_agents.pattern_matching.pattern_matcher import PatternMatcher, Pattern

@pytest.fixture
def matcher():
    return PatternMatcher()

@pytest.fixture
def sample_input():
    return {
        'sequence_id': '123',
        'thought': 'I feel anxious when thinking about the future',
        'timestamp': datetime.now().isoformat(),
        'context': {
            'emotional_state': 'anxious',
            'triggers': ['future thoughts'],
            'intensity': 0.7
        }
    }

@pytest.fixture
def sample_pattern():
    return Pattern(
        id='test_pattern_1',
        type='emotional',
        content={'theme': 'anxiety', 'focus': 'future'},
        context={'temporal': {}, 'emotional': {}, 'behavioral': {}, 'cognitive': {}},
        confidence=0.8,
        connections=[],
        emergence_time=datetime.now().isoformat(),
        evolution_stage='initial'
    )

@pytest.mark.asyncio
async def test_pattern_recognition(matcher, sample_input):
    """Test basic pattern recognition functionality."""
    patterns = await matcher.find_patterns(sample_input)
    
    assert patterns is not None
    assert len(patterns) > 0
    assert all(isinstance(p, Pattern) for p in patterns)

@pytest.mark.asyncio
async def test_context_extraction(matcher, sample_input):
    """Test context extraction from input."""
    context = await matcher._extract_context(sample_input)
    
    assert 'temporal' in context
    assert 'emotional' in context
    assert 'behavioral' in context
    assert 'cognitive' in context
    
    # Verify temporal context
    assert 'timestamp' in context['temporal']
    assert 'sequence' in context['temporal']

@pytest.mark.asyncio
async def test_pattern_validation(matcher, sample_pattern):
    """Test pattern validation process."""
    validated = await matcher._validate_patterns([sample_pattern])
    
    assert len(validated) > 0
    assert validated[0].confidence >= 0.7
    assert validated[0].id == sample_pattern.id

@pytest.mark.asyncio
async def test_connection_analysis(matcher):
    """Test pattern connection analysis."""
    pattern1 = Pattern(
        id='test_1',
        type='emotional',
        content={'theme': 'anxiety'},
        context={},
        confidence=0.8,
        connections=[],
        emergence_time=datetime.now().isoformat(),
        evolution_stage='initial'
    )
    
    pattern2 = Pattern(
        id='test_2',
        type='behavioral',
        content={'action': 'avoidance'},
        context={},
        confidence=0.8,
        connections=[],
        emergence_time=datetime.now().isoformat(),
        evolution_stage='initial'
    )
    
    connected = await matcher._analyze_connections([pattern1, pattern2])
    
    assert len(connected) == 2
    assert connected[0].connections or connected[1].connections

@pytest.mark.asyncio
async def test_multi_dimensional_analysis(matcher, sample_input):
    """Test multi-dimensional pattern analysis."""
    patterns = await matcher.find_patterns(sample_input)
    
    # Check for patterns across dimensions
    pattern_types = {p.type for p in patterns}
    assert len(pattern_types) > 1  # Should find patterns in multiple dimensions

@pytest.mark.asyncio
async def test_confidence_calculation(matcher, sample_pattern):
    """Test pattern confidence calculation."""
    confidence = matcher._calculate_confidence(sample_pattern)
    
    assert 0 <= confidence <= 1
    assert isinstance(confidence, float)

@pytest.mark.asyncio
async def test_connection_strength(matcher):
    """Test connection strength calculation."""
    pattern1 = Pattern(
        id='test_1',
        type='emotional',
        content={'theme': 'anxiety'},
        context={},
        confidence=0.8,
        connections=[],
        emergence_time=datetime.now().isoformat(),
        evolution_stage='initial'
    )
    
    pattern2 = Pattern(
        id='test_2',
        type='behavioral',
        content={'action': 'avoidance'},
        context={},
        confidence=0.8,
        connections=[],
        emergence_time=datetime.now().isoformat(),
        evolution_stage='initial'
    )
    
    strength = matcher._calculate_connection_strength(pattern1, pattern2)
    
    assert 0 <= strength <= 1
    assert isinstance(strength, float)

@pytest.mark.asyncio
async def test_error_handling(matcher):
    """Test error handling with invalid input."""
    patterns = await matcher.find_patterns({})  # Empty input
    assert patterns == []
    
    patterns = await matcher.find_patterns(None)  # None input
    assert patterns == [] 