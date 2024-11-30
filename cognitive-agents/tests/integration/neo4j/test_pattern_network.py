import pytest
from cognitive_agents.memory.pattern_network import PatternNetwork
from termcolor import colored
from tests.integration.neo4j.test_helpers import verify_neo4j_connection

pytestmark = [
    pytest.mark.asyncio(loop_scope="function"),
    pytest.mark.integration
]

class TestPatternNetwork:
    @pytest.fixture
    async def network(self):
        """Create and connect to Neo4j."""
        print(colored("\n🔄 Setting up network fixture...", "cyan"))
        
        network = PatternNetwork(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="evolution"
        )
        
        if not verify_neo4j_connection():
            print(colored("✗ Neo4j connection failed in fixture", "red"))
            pytest.fail("Neo4j connection failed")
            
        print(colored("✓ Neo4j connection verified", "green"))
        
        try:
            connected = await network.connect()
            if not connected:
                print(colored("✗ Network connection failed", "red"))
                pytest.fail("Network connection failed")
            print(colored("✓ Network connected", "green"))
            
            # Clean up any existing test data
            await self.cleanup_neo4j(network)
            
            return network
            
        except Exception as e:
            print(colored(f"✗ Error in fixture: {str(e)}", "red"))
            raise

    async def cleanup_neo4j(self, network):
        """Clean up test data between runs."""
        async with network.driver.session() as session:
            await session.run("""
                MATCH (n)
                DETACH DELETE n
            """)
            print(colored("✓ Test data cleaned up", "green"))

    async def test_pattern_connection(self, network):
        """Test basic pattern connection."""
        network = await network
        
        try:
            pattern = {
                'content': 'Test pattern',
                'themes': ['test'],
                'type': 'test'
            }
            result = await network.connect_pattern("test_1", pattern)
            assert result is True
            
        finally:
            if network:
                await network.close()

    async def verify_theme_relationships(self, network, theme_name: str) -> list:
        """Verify patterns connected to a theme."""
        async with network.driver.session() as session:
            result = await session.run("""
                MATCH (t:Theme {name: $theme})<-[:HAS_THEME]-(p:Pattern)
                RETURN collect(p.id) as pattern_ids
                """, theme=theme_name)
            record = await result.single()
            return record["pattern_ids"]

    async def verify_pattern_connections(self, network, pattern_id: str) -> dict:
        """Verify pattern's themes and connections."""
        async with network.driver.session() as session:
            result = await session.run("""
                MATCH (p:Pattern {id: $pattern_id})-[:HAS_THEME]->(t:Theme)
                RETURN collect(t.name) as themes
                """, pattern_id=pattern_id)
            record = await result.single()
            return {"themes": record["themes"]}

    async def test_theme_relationships(self, network):
        """Test natural theme relationship formation."""
        network = await network
        
        try:
            patterns = [
                {
                    'content': 'Learning happens naturally',
                    'themes': ['learning', 'natural'],
                    'type': 'insight'
                },
                {
                    'content': 'Natural patterns emerge',
                    'themes': ['patterns', 'natural'],
                    'type': 'insight'
                }
            ]
            
            print(colored("\n🔄 Testing Theme Relationships:", "cyan"))
            
            # Connect patterns
            for i, pattern in enumerate(patterns):
                result = await network.connect_pattern(f"theme_test_{i}", pattern)
                assert result is True
                print(colored(f"✓ Pattern {i} connected", "green"))
            
            # Verify theme relationships
            natural_patterns = await self.verify_theme_relationships(network, "natural")
            assert len(natural_patterns) == 2, "Both patterns should connect to 'natural' theme"
            
            learning_patterns = await self.verify_theme_relationships(network, "learning")
            assert len(learning_patterns) == 1, "One pattern should connect to 'learning' theme"
            
            print(colored("✓ Theme relationships verified", "green"))
            
        finally:
            if network:
                await network.close()

    async def test_pattern_evolution(self, network):
        """Test how patterns evolve and connect over time."""
        network = await network
        
        try:
            # Initial pattern
            base_pattern = {
                'content': 'Understanding grows naturally',
                'themes': ['understanding', 'growth'],
                'type': 'insight'
            }
            
            print(colored("\n🔄 Testing Pattern Evolution:", "cyan"))
            
            # Connect base pattern
            result = await network.connect_pattern("evolution_1", base_pattern)
            assert result is True
            print(colored("✓ Base pattern connected", "green"))
            
            # Verify base pattern connections
            base_connections = await self.verify_pattern_connections(network, "evolution_1")
            assert set(base_connections["themes"]) == {"understanding", "growth"}
            print(colored("✓ Base pattern verified", "green"))
            
            # Evolving pattern
            evolved_pattern = {
                'content': 'Understanding deepens through connections',
                'themes': ['understanding', 'connections', 'depth'],
                'type': 'insight'
            }
            
            # Connect evolved pattern
            result = await network.connect_pattern("evolution_2", evolved_pattern)
            assert result is True
            print(colored("✓ Evolved pattern connected", "green"))
            
            # Verify evolved pattern connections
            evolved_connections = await self.verify_pattern_connections(network, "evolution_2")
            assert set(evolved_connections["themes"]) == {"understanding", "connections", "depth"}
            
            # Verify shared themes
            understanding_patterns = await self.verify_theme_relationships(network, "understanding")
            assert len(understanding_patterns) == 2, "Both patterns should share 'understanding' theme"
            print(colored("✓ Pattern evolution verified", "green"))
            
        finally:
            if network:
                await network.close()

    async def test_pattern_querying(self, network):
        """Test pattern querying capabilities."""
        network = await network
        
        try:
            # Create test patterns
            patterns = [
                {
                    'content': 'Pattern A',
                    'themes': ['test', 'a'],
                    'type': 'test'
                },
                {
                    'content': 'Pattern B',
                    'themes': ['test', 'b'],
                    'type': 'test'
                }
            ]
            
            print(colored("\n🔍 Testing Pattern Queries:", "cyan"))
            
            # Add patterns
            for i, pattern in enumerate(patterns):
                result = await network.connect_pattern(f"query_test_{i}", pattern)
                assert result is True
                print(colored(f"✓ Pattern {i} connected", "green"))
            
            # Query by theme
            test_patterns = await self.verify_theme_relationships(network, "test")
            assert len(test_patterns) == 2, "Should find both test patterns"
            print(colored("✓ Theme query verified", "green"))
            
            # Query specific pattern
            pattern_a = await self.verify_pattern_connections(network, "query_test_0")
            assert "a" in pattern_a["themes"], "Should find pattern A themes"
            print(colored("✓ Pattern query verified", "green"))
            
        finally:
            if network:
                await network.close()