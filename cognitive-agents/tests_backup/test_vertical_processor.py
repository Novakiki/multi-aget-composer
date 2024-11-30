import pytest
import asyncio
from cognitive_agents.agents.vertical_processor import VerticalProcessor

@pytest.mark.asyncio
async def test_vertical_processing():
    processor = VerticalProcessor()
    thought = "I notice patterns repeating in my life"
    
    # Test surface processing
    surface_result = await processor.process_at_depth(thought, 'surface')
    assert surface_result['depth_level'] == 'surface'
    assert 'patterns' in surface_result
    
    # Test intermediate processing
    intermediate_result = await processor.process_at_depth(thought, 'intermediate')
    assert intermediate_result['depth_level'] == 'intermediate'
    assert 'patterns' in intermediate_result
    
    # Test deep processing
    deep_result = await processor.process_at_depth(thought, 'deep')
    assert deep_result['depth_level'] == 'deep'
    assert 'patterns' in deep_result

@pytest.mark.asyncio
async def test_depth_pattern_extraction():
    processor = VerticalProcessor()
    thought = "I see immediate patterns and deeper connections"
    
    # Process at different depths
    results = await asyncio.gather(
        processor.process_at_depth(thought, 'surface'),
        processor.process_at_depth(thought, 'intermediate'),
        processor.process_at_depth(thought, 'deep')
    )
    
    # Verify pattern extraction
    for result in results:
        assert 'patterns' in result
        assert isinstance(result['patterns'], list) 

@pytest.mark.asyncio
async def test_vertical_depth_features():
    processor = VerticalProcessor()
    thought = "I feel anxious about changes in my life"
    
    # Test each depth level's specific features
    surface_result = await processor.process_at_depth(thought, 'surface')
    assert surface_result['meta']['depth_features'] == ['quick pattern detection', 'basic categorization']
    
    intermediate_result = await processor.process_at_depth(thought, 'intermediate')
    assert intermediate_result['meta']['depth_features'] == ['pattern_connections', 'context_building']
    
    deep_result = await processor.process_at_depth(thought, 'deep')
    assert deep_result['meta']['depth_features'] == ['meta_patterns', 'systemic_insights']
    
    # Verify pattern classification
    for pattern in surface_result['patterns']:
        assert processor._is_surface_pattern(pattern)
    
    for pattern in intermediate_result['patterns']:
        assert processor._is_connection_pattern(pattern)
    
    for pattern in deep_result['patterns']:
        assert processor._is_meta_pattern(pattern)