import os
import click
from termcolor import colored
from pinecone import Pinecone
from neo4j import AsyncGraphDatabase
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def validate_environment():
    """Validate all evolution environment variables and connections."""
    print(colored("\n🔍 Validating Evolution Stack:", "cyan"))
    
    try:
        # 1. MongoDB
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        await client.admin.command('ping')
        print(colored("✅ MongoDB Connected", "green"))
        
        # 2. Neo4j
        async with AsyncGraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "evolution")  # Default password from installation
        ) as driver:
            await driver.verify_connectivity()
            print(colored("✅ Neo4j Connected", "green"))
            
        # 3. Pinecone (Already validated)
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        indexes = pc.list_indexes().names()
        print(colored("✅ Pinecone Connected", "green"))
        print(f"  • Available Indexes: {indexes}")
        
        print(colored("\n✨ Evolution Stack Ready!", "green"))
        return True
        
    except Exception as e:
        print(colored(f"❌ Validation Error: {str(e)}", "red"))
        return False

@click.command()
def validate():
    """Validate evolution environment."""
    asyncio.run(validate_environment())

if __name__ == "__main__":
    validate() 