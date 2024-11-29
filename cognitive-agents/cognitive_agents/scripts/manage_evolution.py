import click
from cognitive_agents.memory.evolution_services import EvolutionServices

@click.group()
def cli():
    """Evolution services management."""
    pass
    
@cli.command()
def validate():
    """Validate evolution services."""
    services = EvolutionServices()
    for name in ['pinecone', 'neo4j', 'mongodb']:
        if services.is_available(name):
            click.echo(f"✅ {name} available")
        else:
            click.echo(f"❌ {name} not available")
            
@cli.command()
def create_indexes():
    """Create required indexes."""
    services = EvolutionServices()
    if services.is_available('pinecone'):
        pc = services.get_service('pinecone')
        # Create indexes... 