import asyncio
from neo4j import AsyncGraphDatabase
from termcolor import colored

async def verify_neo4j():
    """Verify Neo4j connection."""
    try:
        driver = AsyncGraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "evolution")
        )
        async with driver.session() as session:
            result = await session.run("RETURN 1")
            await result.single()
            print(colored("✅ Neo4j Connected", "green"))
            
    except Exception as e:
        print(colored(f"❌ Neo4j Error: {str(e)}", "red"))

if __name__ == "__main__":
    asyncio.run(verify_neo4j()) 