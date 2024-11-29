"""Demonstrate personal growth tracking with community insights."""
from typing import Dict, List
from termcolor import colored
import asyncio

from cognitive_agents.agents.specialized_agents import CognitiveOrchestrator
from cognitive_agents.pattern_store.community_patterns import CommunityPatternStore
from cognitive_agents.visualization.pattern_viz import PatternVisualizer

async def track_growth_journey():
    """Show a complete growth tracking journey."""
    print(colored("\n Growth Journey Tracking Demo", "cyan"))
    
    # Initialize components
    orchestrator = CognitiveOrchestrator()
    pattern_store = CommunityPatternStore()
    visualizer = PatternVisualizer()
    
    # Example growth journey
    journey_entries = [
        "Starting to learn about mindfulness, feeling uncertain",
        "Day 5: Noticed myself being more present in conversations",
        "Two weeks in: Handling stress better, but still challenging",
        "One month: Significant change in how I approach difficulties"
    ]
    
    try:
        # 1. Process Journey
        print(colored("\n1. Processing Growth Journey", "cyan"))
        results = []
        for entry in journey_entries:
            result = await orchestrator.process_thoughts(entry)
            results.append(result)
            
        # 2. Extract Patterns
        print(colored("\n2. Identifying Growth Patterns", "cyan"))
        patterns = await pattern_store.extract_growth_patterns(results)
        
        # 3. Community Validation
        print(colored("\n3. Community Pattern Validation", "cyan"))
        validated_patterns = await pattern_store.validate_growth_patterns(patterns)
        
        # 4. Visualize Progress
        print(colored("\n4. Growth Visualization", "cyan"))
        visualizer.show_pattern_evolution(validated_patterns)
        
        return validated_patterns
        
    except Exception as e:
        print(colored(f"❌ Error in growth tracking: {str(e)}", "red"))
        return None

async def main():
    """Run the complete demonstration."""
    patterns = await track_growth_journey()
    if patterns:
        print(colored("\n✅ Growth tracking demo completed", "green"))
        
if __name__ == "__main__":
    asyncio.run(main()) 