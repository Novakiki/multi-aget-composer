"""Interactive CLI for cognitive agents."""
import click
import asyncio
import sys
import time
from termcolor import colored
from cognitive_agents import CognitiveAgent

def _calculate_timeout(thought: str, has_previous_patterns: bool) -> int:
    """Calculate appropriate timeout based on thought complexity."""
    base_timeout = 10  # Base timeout for simple thoughts
    
    # Add time for complexity factors
    complexity_score = 0
    
    # Abstract concepts (words like "feel", "think", "sense", "intuition")
    abstract_words = {"feel", "think", "sense", "intuit", "believe", "understand"}
    if any(word in thought.lower() for word in abstract_words):
        complexity_score += 2
    
    # Length complexity
    if len(thought.split()) > 15:
        complexity_score += 2
    
    # Previous pattern integration
    if has_previous_patterns:
        complexity_score += 3
    
    # Return adaptive timeout
    return base_timeout + complexity_score

@click.command()
@click.option('--interactive', '-i', is_flag=True, 
              help='Start interactive session')
def cli(interactive):
    """Process thoughts with cognitive agents."""
    asyncio.run(main(interactive))

async def main(interactive):
    """Main async function."""
    agent = CognitiveAgent("CLI Observer")
    has_previous_patterns = False
    
    if interactive:
        click.echo(colored("\n Welcome to Cognitive Agents", "cyan"))
        click.echo("Share your thoughts, type 'exit' to quit\n")
        
        while True:
            try:
                thought = click.prompt('💭 Your thought')
                if thought.lower() == 'exit':
                    break
                if not thought.strip():
                    click.echo(colored("\n⚠️  Please share a thought", "yellow"))
                    continue
                    
                # Calculate adaptive timeout
                timeout = _calculate_timeout(thought, has_previous_patterns)
                click.echo(colored(f"\nProcessing (timeout: {timeout}s)...", "cyan"))
                
                try:
                    # Initial processing
                    result = await agent.process_thought(thought)
                    has_previous_patterns = True  # Mark that we have patterns
                    
                    # Wait for integration with better feedback
                    click.echo(colored("\n🔄 Integrating insights...", "cyan"))
                    start_time = time.time()
                    
                    while not result.get('insights', {}).get('integrated_understanding'):
                        if time.time() - start_time > timeout:
                            raise TimeoutError(
                                f"Integration exceeded {timeout}s timeout"
                            )
                        await asyncio.sleep(0.2)
                        
                        # Show integration status with timing
                        elapsed = time.time() - start_time
                        status = f"{'Connecting patterns' if result.get('patterns') else 'Processing'} ({elapsed:.1f}s/{timeout}s)"
                        sys.stdout.write(f"\r{status}...")
                        sys.stdout.flush()
                    
                    # Clear status line
                    sys.stdout.write('\r' + ' ' * 50 + '\r')
                    
                    # Now access complete data
                    insights = result['insights']
                    understanding = insights['integrated_understanding']
                    
                    # Show complete analysis
                    if understanding.get('patterns'):
                        click.echo(colored("\n🔄 Patterns Found:", "yellow"))
                        for pattern in understanding['patterns']:
                            click.echo(f"  • {pattern}")
                            
                    if understanding.get('analysis'):
                        click.echo(colored("\n💡 Understanding:", "green"))
                        click.echo(f"  {understanding['analysis']}")
                        
                    if understanding.get('meta_cognition'):
                        click.echo(colored("\n🤔 Meta Reflection:", "magenta"))
                        click.echo(f"  {understanding['meta_cognition']}")
                        
                except TimeoutError:
                    click.echo(colored("\n⚠️  Integration is taking longer than expected", "yellow"))
                    click.echo("  Try a simpler thought or wait for system to complete")
                except Exception as e:
                    click.echo(colored(f"\n❌ Error: {str(e)}", "red"))
                    
            except KeyboardInterrupt:
                click.echo(colored("\n\n👋 Goodbye!", "cyan"))
                break
            except Exception as e:
                click.echo(colored(f"\n❌ Error: {str(e)}", "red"))
    else:
        # Single thought processing
        thought = click.prompt('Share a thought')
        result = await agent.process_thought(thought)
        click.echo(result)

if __name__ == '__main__':
    cli() 