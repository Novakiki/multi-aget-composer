"""Test suite for cognitive agent system."""

import pytest
import asyncio
from typing import Dict, List
from cognitive_agents.agents.cognitive_agent import CognitiveAgent

@pytest.mark.asyncio
async def test_natural_unfolding():
    """Test natural deepening of understanding."""
    agent = CognitiveAgent("Test Observer")
    
    # Initial thought
    result1 = await agent.process_thought("I feel stuck")
    
    # Deeper exploration
    result2 = await agent.process_thought("Exploring why I feel stuck")
    
    # Assertions
    assert len(result2['patterns']) >= len(result1['patterns'])
    assert result2['depth'] > result1['depth']
    assert 'meta_synthesis' in result2

@pytest.mark.asyncio
async def test_resource_awareness():
    """Test smart spawning behavior."""
    agent = CognitiveAgent("Test Monitor")
    
    # Simple thought shouldn't spawn
    simple = await agent.process_thought("Today was fine")
    assert not simple.get('sub_thoughts')
    
    # Complex thought should spawn carefully
    complex = await agent.process_thought(
        """I'm noticing patterns in how I respond to 
        challenges, especially when facing uncertainty 
        about the future and what it might bring"""
    )
    spawn_score = complex.get('meta_synthesis', {}).get('integration_quality', 0)
    assert spawn_score > 0.5  # Should meet spawn threshold

@pytest.mark.asyncio
async def test_pattern_memory():
    """Test pattern recognition and memory."""
    agent = CognitiveAgent("Test Pattern Analyst")
    
    # Process related thoughts
    thoughts = [
        "Change makes me nervous",
        "New situations are scary",
        "I worry about the unknown"
    ]
    
    patterns = set()
    for thought in thoughts:
        result = await agent.process_thought(thought)
        patterns.update(result.get('patterns', []))
    
    # Check pattern memory
    assert len(agent.pattern_memory) > 0
    assert len(patterns) > 0
    
    # Check pattern relevance
    last_pattern = agent.pattern_memory[-1]
    is_relevant = agent._is_pattern_relevant(last_pattern, thoughts[-1])
    assert is_relevant 