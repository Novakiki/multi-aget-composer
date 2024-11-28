"""Interactive CLI for cognitive agents."""
import click
import asyncio
from termcolor import colored
from cognitive_agents import CognitiveAgent

@click.command()
@click.option('--interactive', '-i', is_flag=True, 
              help='Start interactive session')
async def main(interactive):
    """Process thoughts with cognitive agents."""
    agent = CognitiveAgent("CLI Observer")
    
    if interactive:
        click.echo(colored("\n Welcome to Cognitive Agents", "cyan"))
        click.echo("Share your thoughts, type 'exit' to quit\n")
        
        while True:
            thought = click.prompt('💭 Your thought')
            if thought.lower() == 'exit':
                break
                
            click.echo(colored("\nProcessing...", "cyan"))
            result = await agent.process_thought(thought)
            
            # Show natural unfolding
            click.echo(colored("\n🔄 Patterns Found:", "yellow"))
            for pattern in result.get('patterns', []):
                click.echo(f"  • {pattern}")
            
            click.echo(colored("\n💡 Understanding:", "green"))
            click.echo(f"  {result.get('analysis', '')}")
    else:
        # Single thought processing
        thought = click.prompt('Share a thought')
        result = await agent.process_thought(thought)
        click.echo(result)

if __name__ == '__main__':
    asyncio.run(main()) 