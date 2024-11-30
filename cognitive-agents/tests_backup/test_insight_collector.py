import pytest
from cognitive_agents.core.insight_collector import InsightCollector

@pytest.mark.asyncio
async def test_pattern_addition():
    """Test basic pattern processing."""
    collector = InsightCollector()
    
    # Add pattern
    pattern = {'type': 'test_pattern', 'data': 'test'}
    await collector.add_pattern(pattern, 'test_domain')
    
    # Verify
    synthesis = collector.get_synthesis()
    assert 'test_domain' in synthesis['patterns']
    assert synthesis['patterns']['test_domain'] == 1

@pytest.mark.asyncio
async def test_connection_emergence():
    """Test natural connection emergence."""
    collector = InsightCollector()
    
    # Add multiple patterns
    patterns = [
        {'type': 'pattern1', 'data': 'test1'},
        {'type': 'pattern2', 'data': 'test2'}
    ]
    
    for pattern in patterns:
        await collector.add_pattern(pattern, 'test_domain')
    
    # Verify connections emerged
    synthesis = collector.get_synthesis()
    assert synthesis['connections'] > 0

@pytest.mark.asyncio
async def test_insight_emergence():
    """Test higher-order insight emergence."""
    collector = InsightCollector()
    
    # Add multiple patterns to trigger insight
    patterns = [
        {'type': 'pattern1', 'data': 'test1'},
        {'type': 'pattern2', 'data': 'test2'},
        {'type': 'pattern3', 'data': 'test3'}
    ]
    
    for pattern in patterns:
        await collector.add_pattern(pattern, 'test_domain')
    
    # Verify insight emerged
    synthesis = collector.get_synthesis()
    assert synthesis['emergent_insights'] > 0

@pytest.mark.asyncio
async def test_cross_domain_synthesis():
    """Test synthesis across different domains."""
    collector = InsightCollector()
    
    # Add patterns in different domains
    domains = ['emotional', 'behavioral', 'cognitive']
    for domain in domains:
        await collector.add_pattern(
            {'type': f'pattern_{domain}', 'data': 'test'},
            domain
        )
    
    # Verify cross-domain synthesis
    synthesis = collector.get_synthesis()
    assert len(synthesis['patterns']) == len(domains)
    assert synthesis['connections'] > 0 