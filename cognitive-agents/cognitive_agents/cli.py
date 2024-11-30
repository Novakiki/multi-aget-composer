"""Evolution System CLI."""
import os
import click
import asyncio
from termcolor import colored
from .memory.pattern_store import PatternStore
from .memory.pattern_network import PatternNetwork
from .memory.pattern_semantics import PatternSemantics
from .memory.theme_extraction import ThemeExtraction
from .memory.question_evolution import QuestionEvolution

@click.group()
def cli():
    """Natural Pattern Evolution System"""
    pass

@cli.command()
@click.argument('question')
@click.option('--test', is_flag=True, help='Run in test mode')
def evolve(question, test):
    """Evolve a question naturally."""
    async def run():
        try:
            if test:
                # Use mock services
                print(colored("\n🔄 Running in Test Mode", "yellow"))
                result = {
                    'pattern_id': 'test_pat_1',
                    'themes': ['learning', 'patterns', 'evolution'],
                    'connections': [
                        {'metadata': {'content': 'How do patterns form?'}, 'score': 0.9}
                    ]
                }
            else:
                print(colored("\n🔄 Initializing Evolution System", "cyan"))
                
                # Initialize components
                store = PatternStore(os.getenv('MONGODB_URI'))
                print(colored("✓ Pattern Store Ready", "green"))
                
                network = PatternNetwork(
                    store=store,
                    uri=os.getenv('NEO4J_URI'),
                    user=os.getenv('NEO4J_USER'),
                    password=os.getenv('NEO4J_PASSWORD')
                )
                print(colored("✓ Knowledge Network Ready", "green"))
                
                semantics = PatternSemantics(
                    network=network,
                    api_key=os.getenv('PINECONE_API_KEY')
                )
                print(colored("✓ Semantic Understanding Ready", "green"))
                
                theme_extractor = ThemeExtraction(store, network)
                
                # Create evolution system
                evolution = QuestionEvolution(
                    store=store,
                    network=network,
                    semantics=semantics,
                    theme_extractor=theme_extractor
                )
                
                # Evolve question
                print(colored(f"\n🤔 Evolving Question: {question}", "cyan"))
                result = await evolution.evolve_question(question)
                
                # Display results
                print(colored("\n✨ Evolution Results:", "green"))
                print(f"Pattern ID: {result['pattern_id']}")
                print(f"Themes: {', '.join(result['themes'])}")
                print("\nSimilar Patterns:")
                for pattern in result['connections']:
                    print(f"  • {pattern['metadata']['content']} ({pattern['score']:.2f})")
                
        except Exception as e:
            print(colored(f"\n❌ Evolution Error: {str(e)}", "red"))
            
    asyncio.run(run())

if __name__ == '__main__':
    cli() 