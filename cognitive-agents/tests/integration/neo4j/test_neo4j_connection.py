import pytest
import os
from neo4j import AsyncGraphDatabase
from termcolor import colored

pytestmark = pytest.mark.integration

@pytest.mark.asyncio
class TestNeo4jConnection:
    @pytest.fixture
    async def graph(self):
        """Create Neo4j connection."""
        uri = "bolt://localhost:7687"
        auth = ("neo4j", "evolution")
        
        print(colored(f"\n🔌 Connecting to Neo4j:", "cyan"))
        print(f"URI: {uri}")
        
        driver = AsyncGraphDatabase.driver(uri, auth=auth)
        
        # Verify connection
        async with driver.session() as session:
            result = await session.run("RETURN 1 as num")
            record = await result.single()
            assert record["num"] == 1
            print(colored("✅ Neo4j connection successful", "green"))
            
        return driver
        
    async def test_neo4j_basic_operations(self, graph):
        """Test basic Neo4j operations."""
        # Await the fixture
        driver = await graph
        
        async with driver.session() as session:
            # Create test node
            await session.run(
                "CREATE (n:TestNode {name: $name}) RETURN n",
                name="test_node"
            )
            
            # Query test node
            result = await session.run(
                "MATCH (n:TestNode {name: $name}) RETURN n.name",
                name="test_node"
            )
            record = await result.single()
            assert record["n.name"] == "test_node"
            
            # Cleanup
            await session.run(
                "MATCH (n:TestNode {name: $name}) DELETE n",
                name="test_node"
            )
            
        print(colored("✅ Neo4j operations successful", "green")) 