"""Examples of different cognitive agent usage patterns."""

import asyncio
from termcolor import colored
from typing import Dict, List
from datetime import datetime

from ..agents.cognitive_agent import CognitiveAgent

async def demonstrate_natural_unfolding():
    """Show how understanding deepens naturally."""
    try:
        print(colored("\n🌱 Demonstrating Natural Unfolding", "cyan"))
        agent = CognitiveAgent("Natural Observer")
        
        # Initial thought
        thought = "I feel overwhelmed with everything changing"
        print(colored(f"\n💭 Initial Thought: '{thought}'", "white"))
        
        # First pass - surface understanding
        result1 = await agent.process_thought(thought)
        
        # Let it deepen
        deeper_thought = "Looking deeper at feeling overwhelmed with change"
        print(colored(f"\n🔄 Deepening: '{deeper_thought}'", "white"))
        result2 = await agent.process_thought(deeper_thought)
        
        return {
            "initial": result1,
            "deeper": result2,
            "patterns_recognized": len(agent.pattern_memory)
        }
        
    except Exception as e:
        print(colored(f"Error in natural unfolding: {str(e)}", "red"))
        return {"error": str(e)}

async def explore_pattern_connections():
    """Demonstrate pattern recognition across thoughts."""
    try:
        print(colored("\n🔍 Exploring Pattern Connections", "cyan"))
        agent = CognitiveAgent("Pattern Explorer")
        
        # Related thoughts
        thoughts = [
            "I'm nervous about starting a new job",
            "Moving to a new city feels scary",
            "Learning new skills makes me anxious"
        ]
        
        patterns = []
        for thought in thoughts:
            print(colored(f"\n💭 Processing: '{thought}'", "white"))
            result = await agent.process_thought(thought)
            patterns.extend(result.get('patterns', []))
        
        return {
            "unique_patterns": list(set(patterns)),
            "total_processed": len(thoughts),
            "pattern_connections": len(agent.pattern_memory)
        }
        
    except Exception as e:
        print(colored(f"Error in pattern exploration: {str(e)}", "red"))
        return {"error": str(e)}

async def demonstrate_resource_awareness():
    """Show resource-aware processing."""
    try:
        print(colored("\n⚡ Demonstrating Resource Awareness", "cyan"))
        agent = CognitiveAgent("Resource Monitor")
        
        # Simple thought - shouldn't spawn
        simple = "Today was okay"
        print(colored(f"\n💭 Simple Thought: '{simple}'", "white"))
        result1 = await agent.process_thought(simple)
        
        # Complex thought - might spawn
        complex = """I'm noticing how my reactions to change 
        have evolved over time, especially in how I handle 
        uncertainty and new situations"""
        print(colored(f"\n💭 Complex Thought: '{complex}'", "white"))
        result2 = await agent.process_thought(complex)
        
        return {
            "simple_spawned": len(result1.get('sub_thoughts', [])) > 0,
            "complex_spawned": len(result2.get('sub_thoughts', [])) > 0,
            "resource_efficiency": "Demonstrated spawn control"
        }
        
    except Exception as e:
        print(colored(f"Error in resource demo: {str(e)}", "red"))
        return {"error": str(e)}

async def main():
    """Run usage examples."""
    try:
        # Natural unfolding
        result1 = await demonstrate_natural_unfolding()
        print(colored("\n✨ Natural Unfolding Results:", "green"))
        print(f"Patterns Recognized: {result1['patterns_recognized']}")
        
        # Pattern connections
        result2 = await explore_pattern_connections()
        print(colored("\n✨ Pattern Connection Results:", "green"))
        print(f"Unique Patterns: {len(result2['unique_patterns'])}")
        
        # Resource awareness
        result3 = await demonstrate_resource_awareness()
        print(colored("\n✨ Resource Awareness Results:", "green"))
        print(f"Resource Efficiency: {result3['resource_efficiency']}")
        
    except Exception as e:
        print(colored(f"Error in examples: {str(e)}", "red"))

if __name__ == "__main__":
    asyncio.run(main()) 