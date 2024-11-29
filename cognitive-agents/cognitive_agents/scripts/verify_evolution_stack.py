import asyncio
import os
from termcolor import colored
from neo4j import AsyncGraphDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from pinecone import Pinecone

async def verify_stack():
    """Verify all evolution services."""
    print(colored("\n🔍 Verifying Evolution Stack:", "cyan"))
    
    try:
        # 1. Neo4j
        driver = AsyncGraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "evolution")
        )
        async with driver.session() as session:
            result = await session.run("RETURN 1")
            await result.single()
            print(colored("✅ Neo4j Connected", "green"))
            
        # 2. MongoDB
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        await client.admin.command('ping')
        print(colored("✅ MongoDB Connected", "green"))
        
        # 3. Pinecone
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        indexes = pc.list_indexes().names()
        print(colored("✅ Pinecone Connected", "green"))
        print(f"  • Available Indexes: {indexes}")
        
        print(colored("\n✨ Evolution Stack Ready!", "green"))
        
    except Exception as e:
        print(colored(f"❌ Verification Error: {str(e)}", "red"))

if __name__ == "__main__":
    asyncio.run(verify_stack()) 