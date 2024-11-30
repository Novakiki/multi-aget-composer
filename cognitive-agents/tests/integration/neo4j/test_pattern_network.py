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
        
        # Create network instance
        network = PatternNetwork(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="evolution"
        )
        
        # Verify Neo4j connection first
        if not verify_neo4j_connection():
            print(colored("✗ Neo4j connection failed in fixture", "red"))
            pytest.fail("Neo4j connection failed")
            
        print(colored("✓ Neo4j connection verified", "green"))
        
        # Connect network
        try:
            connected = await network.connect()
            if not connected:
                print(colored("✗ Network connection failed", "red"))
                pytest.fail("Network connection failed")
            print(colored("✓ Network connected", "green"))
            
            return network
            
        except Exception as e:
            print(colored(f"✗ Error in fixture: {str(e)}", "red"))
            raise
    
    async def test_pattern_connection(self, network):
        """Test actual Neo4j pattern connection."""
        # Await the network fixture
        network = await network
        
        try:
            print(colored("\n🔄 Starting pattern connection test", "cyan"))
            print(f"Network object type: {type(network)}")
            
            pattern = {
                'content': 'Test pattern',
                'themes': ['test'],
                'type': 'test'
            }
            print(f"Pattern to connect: {pattern}")

            print(colored("Attempting to connect pattern...", "cyan"))
            result = await network.connect_pattern("test_1", pattern)
            print(f"Connection result: {result}")
            
            assert result is True
            print(colored("✓ Pattern connected successfully", "green"))
            
        except Exception as e:
            print(colored(f"✗ Test error: {str(e)}", "red"))
            raise
            
        finally:
            if network:
                print(colored("Cleaning up network connection...", "cyan"))
                await network.close()
                print(colored("✓ Network connection closed", "green"))