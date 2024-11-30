import pytest
from cognitive_agents.core.agent_pool import AgentPool

@pytest.mark.asyncio
async def test_agent_creation():
    """Test basic agent creation and pooling."""
    pool = AgentPool()
    
    # Get new agent
    agent = await pool.get_agent('test_type')
    assert agent is not None
    assert agent['type'] == 'test_type'
    
    # Verify active agents
    stats = pool.get_pool_stats()
    assert stats['active'] == 1
    assert 'test_type' in str(stats['available'])

@pytest.mark.asyncio
async def test_agent_reuse():
    """Test agent reuse functionality."""
    pool = AgentPool()
    
    # Get and release agent
    agent1 = await pool.get_agent('test_type')
    await pool.release_agent(agent1['id'])
    
    # Get another agent - should reuse
    agent2 = await pool.get_agent('test_type')
    assert agent2['id'] == agent1['id']

@pytest.mark.asyncio
async def test_multiple_agents():
    """Test handling multiple agents."""
    pool = AgentPool()
    
    # Create multiple agents
    agents = []
    for _ in range(3):
        agent = await pool.get_agent('test_type')
        agents.append(agent)
    
    # Verify all are active
    stats = pool.get_pool_stats()
    assert stats['active'] == 3
    
    # Release all
    for agent in agents:
        await pool.release_agent(agent['id'])
    
    # Verify all returned to pool
    stats = pool.get_pool_stats()
    assert stats['active'] == 0
    assert stats['available']['test_type'] == 3

@pytest.mark.asyncio
async def test_pool_metrics():
    """Test pool performance metrics."""
    pool = AgentPool()
    
    # Create and use agent
    agent = await pool.get_agent('test_type')
    metrics = pool.performance_metrics[agent['id']]
    
    # Verify metric tracking
    assert 'activated_at' in metrics
    assert 'reuse_count' in metrics
    assert 'processing_time' in metrics 