import os
from termcolor import colored
from pinecone import Pinecone, ServerlessSpec
from neo4j import AsyncGraphDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List

async def validate_evolution_stack(required_services: List[str] = None):
    """Validate evolution stack with optional service requirements."""
    try:
        required_services = required_services or ['pinecone', 'neo4j', 'mongodb']
        available_services = []
        
        print(colored("\n🧬 Validating Evolution Services:", "cyan"))
        
        # 1. Semantic Evolution (Pinecone)
        if 'pinecone' in required_services:
            try:
                api_key = os.getenv('PINECONE_API_KEY')
                if not api_key:
                    print(colored("❌ PINECONE_API_KEY not set", "red"))
                else:
                    pc = Pinecone(api_key=api_key)
                    evolution_index = 'pattern-evolution'
                    indexes = pc.list_indexes().names()
                    
                    if evolution_index not in indexes:
                        print(colored(f"  • Creating index: {evolution_index}", "yellow"))
                        pc.create_index(
                            name=evolution_index,
                            dimension=384,
                            metric='cosine',
                            spec=ServerlessSpec(
                                cloud='gcp',
                                region='gcp-starter'
                            )
                        )
                    available_services.append('pinecone')
                    print(colored("✅ Semantic Evolution (Pinecone)", "green"))
                    print(f"  • Evolution Index: {evolution_index}")
            except Exception as e:
                print(colored(f"❌ Pinecone Error: {str(e)}", "red"))
                
        # Similar blocks for Neo4j and MongoDB...
        
        # Check if we have all required services
        missing_services = set(required_services) - set(available_services)
        if missing_services:
            print(colored(f"❌ Missing required services: {missing_services}", "red"))
            return False
            
        print(colored("\n✨ Evolution Stack Ready!", "green"))
        print(f"  • Available Services: {available_services}")
        return True
        
    except Exception as e:
        print(colored(f"❌ Evolution Stack Error: {str(e)}", "red"))
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(validate_evolution_stack()) 