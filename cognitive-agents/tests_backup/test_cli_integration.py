"""Test CLI integration with timeouts."""
import pytest
import asyncio
from cognitive_agents import CognitiveAgent
from cognitive_agents.cli import _calculate_timeout
import time
import json

async def process_thought_with_timeout(thought: str) -> dict:
    """Process a thought with appropriate timeout."""
    try:
        print(f"\n🔍 Testing thought: '{thought}'")
        agent = CognitiveAgent("Test Observer")
        
        # Calculate dynamic timeout based on complexity
        base_timeout = _calculate_timeout(thought, has_previous_patterns=False)
        spawn_time = 15
        integration_buffer = 10  # Add buffer for integration
        timeout = base_timeout + spawn_time + integration_buffer
        
        print(f"⏱️  Timeout calculated: {timeout}s (base: {base_timeout}s + spawn: {spawn_time}s + buffer: {integration_buffer}s)")
        
        # Initialize timing
        start_time = time.time()
        dots = 0
        
        print("\n⚙️  Processing started...")
        async with asyncio.timeout(timeout):
            # Get initial result
            result = await agent.process_thought(thought)
            print("\n📊 Initial result structure:")
            print(f"  Keys: {list(result.keys())}")
            if 'insights' in result:
                print(f"  Insight keys: {list(result['insights'].keys())}")
            
            # Track spawned agents and processing
            spawn_count = 0
            integration_start = time.time()
            
            # Wait for result to be ready
            while True:
                current_time = time.time()
                elapsed = current_time - start_time
                integration_time = current_time - integration_start
                
                # Debug current state
                print(f"\n🔍 Current state at {elapsed:.1f}s:")
                print(f"  Has insights: {'insights' in result}")
                if 'insights' in result:
                    print(f"  Has understanding: {'integrated_understanding' in result['insights']}")
                    if 'integrated_understanding' in result['insights']:
                        understanding = result['insights']['integrated_understanding']
                        print(f"  Understanding keys: {list(understanding.keys())}")
                        print(f"  Patterns: {len(understanding.get('patterns', []))}")
                
                # Check if we have a complete result
                if result.get('insights', {}).get('integrated_understanding'):
                    print(f"\n✅ Complete: {elapsed:.1f}s | Agents: {spawn_count}")
                    return result
                
                # Check for timeout
                if integration_time > timeout:
                    print(f"\n⚠️  Integration timeout after {elapsed:.1f}s")
                    print("Last result structure:")
                    print(json.dumps(result, indent=2))
                    break
                
                # Show detailed status
                status = f"Processing: {elapsed:.1f}s/{timeout}s"
                if result.get('sub_thoughts'):
                    spawn_count += 1
                    status += f" | Agents: {spawn_count}"
                
                dots = (dots + 1) % 4
                print(f"\r🔄 {status} {'.' * dots}", end='')
                await asyncio.sleep(1)  # Increased sleep to reduce output spam
            
            # If we get here without returning, integration failed
            print("\n❌ Integration incomplete")
            return None
            
    except asyncio.TimeoutError:
        print(f"\n❌ Timeout: {timeout}s exceeded")
        return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None

@pytest.mark.asyncio
async def test_cli_processing():
    """Test full CLI processing with different complexities."""
    test_cases = [
        # (thought, expected_min_patterns, description)
        (
            "I am happy today",  # Simple emotion
            1,
            "Simple emotional state"
        ),
        (
            "I feel deeply connected to this project and its potential",  # Abstract
            2,
            "Abstract feeling with context"
        ),
        (
            "Moving to a new country has completely changed how I see myself and the world",  # Complex
            3,
            "Complex life transition"
        ),
        (
            "Ok",  # Minimal
            1,
            "Minimal input"
        ),
        (
            "I notice that when I work on this system, patterns of understanding emerge naturally",  # Meta
            3,
            "Self-referential observation"
        )
    ]
    
    results = []
    for thought, min_patterns, description in test_cases:
        print(f"\n{'='*50}")
        print(f"Test Case: {description}")
        print(f"Thought: {thought}")
        print(f"Expecting: At least {min_patterns} pattern(s)")
        print(f"{'='*50}")
        
        start_time = time.time()
        result = await process_thought_with_timeout(thought)
        elapsed = time.time() - start_time
        
        # Store test results
        test_result = {
            "description": description,
            "thought": thought,
            "elapsed": elapsed,
            "success": result is not None,
            "patterns": len(result['insights']['integrated_understanding']['patterns']) if result else 0
        }
        results.append(test_result)
        
        # Basic result checks
        assert result is not None, f"Processing failed for: {description}"
        assert 'insights' in result, f"Missing 'insights' in result for: {description}"
        assert 'integrated_understanding' in result['insights'], f"Missing 'integrated_understanding' for: {description}"
        
        # Pattern checks
        patterns = result['insights']['integrated_understanding'].get('patterns', [])
        assert len(patterns) >= min_patterns, f"Found {len(patterns)} patterns, expected at least {min_patterns}"
        
        # Show what we got
        print(f"\n✨ Results for: {description}")
        print(f"Time taken: {elapsed:.1f}s")
        print("\nPatterns found:")
        for pattern in patterns:
            print(f"  • {pattern}")
    
    # Show test summary
    print("\n📊 Test Summary")
    print("=" * 50)
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"{status} {r['description']}: {r['patterns']} patterns in {r['elapsed']:.1f}s")