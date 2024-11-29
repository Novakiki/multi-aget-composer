import pytest
from cognitive_agents.memory.natural_connection import NaturalConnection
from termcolor import colored

@pytest.mark.asyncio
class TestNaturalConnection:
    @pytest.fixture
    async def connection(self):
        """Create and return connection."""
        return NaturalConnection()
        
    async def test_individual_to_collective_flow(self, connection):
        """Test natural flow from individual to collective."""
        # Await the fixture first
        connection = await connection
        
        # Seed initial pattern
        connection.flow['emerging_patterns'].append({
            'type': 'emergent',
            'content': 'Learning happens naturally',
            'questions': ['How do we learn?']
        })
        
        individual_insight = {
            'type': 'individual',
            'content': 'I notice patterns in learning',
            'questions': ['How do these patterns evolve?'],
            'uncertainty': 0.3
        }
        
        # Let it flow naturally
        result = await connection.allow_flow(individual_insight)
        
        print(colored("\n🔄 Testing Individual → Collective Flow:", "cyan"))
        print(f"Original Insight: {individual_insight['content']}")
        print(f"Flow Result: {result.get('emerging_patterns', [])}")
        
        # Verify natural emergence
        assert len(result.get('emerging_patterns', [])) > 0
        assert not any(p.get('forced', False) for p in result['emerging_patterns'])
        
    async def test_collective_to_individual_flow(self, connection):
        """Test natural flow from collective to individual."""
        # Collective wisdom emerges
        collective_wisdom = {
            'type': 'collective',
            'patterns': ['Learning evolves naturally'],
            'questions': ['How do we grow together?']
        }
        
        # Let it influence naturally
        result = await connection.allow_flow(collective_wisdom)
        
        print(colored("\n🔄 Testing Collective → Individual Flow:", "cyan"))
        print(f"Collective Wisdom: {collective_wisdom['patterns']}")
        print(f"Natural Integration: {result.get('integration', [])}")
        
        # Verify organic integration
        assert 'integration' in result
        assert result['integration']['type'] == 'natural'
        
    async def test_emergent_understanding(self, connection):
        """Test natural emergence between levels."""
        # Multiple insights flow
        insights = [
            {'type': 'individual', 'content': 'Learning takes time'},
            {'type': 'collective', 'patterns': ['Growth is organic']},
            {'type': 'individual', 'content': 'Understanding emerges'}
        ]
        
        # Let understanding emerge
        results = []
        for insight in insights:
            result = await connection.allow_flow(insight)
            results.append(result)
            
        print(colored("\n🌱 Testing Natural Emergence:", "cyan"))
        for r in results:
            print(f"Emerging Understanding: {r.get('emerging_patterns', [])}")
            
        # Verify natural evolution
        assert len(results) == len(insights)
        assert all('emerging_patterns' in r for r in results)
        
    async def test_natural_resistance(self, connection):
        """Test system allows natural resistance."""
        # Force an insight
        forced_insight = {
            'type': 'individual',
            'content': 'This must be true',
            'force': True
        }
        
        # System should resist forcing
        result = await connection.allow_flow(forced_insight)
        
        print(colored("\n🛡️ Testing Natural Resistance:", "cyan"))
        print(f"Forced Insight: {forced_insight}")
        print(f"System Response: {result}")
        
        # Verify natural resistance
        assert result.get('resistance', False)
        assert 'natural flow required' in result.get('message', '').lower() 