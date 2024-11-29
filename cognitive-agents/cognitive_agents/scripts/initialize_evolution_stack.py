import asyncio
from termcolor import colored
from cognitive_agents.memory.evolution_services import EvolutionServices

async def initialize_stack():
    """Initialize evolution stack with test data."""
    print(colored("\n🌱 Initializing Evolution Stack:", "cyan"))
    
    services = EvolutionServices()
    
    # 1. Create test pattern
    pattern = {
        'content': 'Learning happens naturally through interaction',
        'type': 'insight',
        'themes': ['learning', 'interaction']
    }
    
    # 2. Store across all dimensions
    try:
        # MongoDB - Store pattern context
        await services.get_service('mongodb').evolution.patterns.insert_one({
            'pattern': pattern,
            'stage': 'emerging'
        })
        print(colored("✅ Pattern Context Stored", "green"))
        
        # Neo4j - Create pattern node
        async with services.get_service('neo4j').session() as session:
            await session.run("""
                CREATE (p:Pattern {content: $content})
                WITH p
                UNWIND $themes as theme
                MERGE (t:Theme {name: theme})
                CREATE (p)-[:HAS_THEME]->(t)
            """, content=pattern['content'], themes=pattern['themes'])
        print(colored("✅ Knowledge Graph Created", "green"))
        
        print(colored("\n✨ Evolution Stack Initialized!", "green"))
        
    except Exception as e:
        print(colored(f"❌ Initialization Error: {str(e)}", "red"))

if __name__ == "__main__":
    asyncio.run(initialize_stack()) 