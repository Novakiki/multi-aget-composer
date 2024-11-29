import pytest
from cognitive_agents.core.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_basic_thought_processing():
    """Test basic thought processing flow."""
    orchestrator = Orchestrator()
    
    # Process a simple thought
    thought = "I feel curious about learning"
    result = await orchestrator.process_thought(thought)
    
    # Verify basic processing occurred
    assert result is not None
    assert 'patterns' in result
    assert 'connections' in result
    assert 'emergent_insights' in result

@pytest.mark.asyncio
async def test_multi_dimensional_processing():
    """Test processing across dimensions."""
    orchestrator = Orchestrator()
    
    # Process thought that should engage all dimensions
    thought = "I notice patterns repeating in my life"
    result = await orchestrator.process_thought(thought)
    
    # Verify dimensional processing
    synthesis = result
    assert len(synthesis['patterns']) >= 3  # One per dimension
    assert synthesis['connections'] > 0     # Connections formed
    
@pytest.mark.asyncio
async def test_natural_emergence():
    """Test natural pattern emergence."""
    orchestrator = Orchestrator()
    
    # Process multiple related thoughts
    thoughts = [
        "I feel excited about new ideas",
        "Learning brings me joy",
        "Understanding patterns excites me"
    ]
    
    results = []
    for thought in thoughts:
        result = await orchestrator.process_thought(thought)
        results.append(result)
    
    # Verify emergence
    final_result = results[-1]
    assert final_result['emergent_insights'] > 0
    
@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling and recovery."""
    orchestrator = Orchestrator()
    
    # Test with invalid input
    result = await orchestrator.process_thought("")
    assert 'error' in result
    
    # Verify system can continue processing
    valid_result = await orchestrator.process_thought("A valid thought")
    assert 'error' not in valid_result
    