"""Demo of enhanced cognitive agent system with rich visualization."""

import asyncio
import json
from pathlib import Path
from termcolor import colored
from ..agents.cognitive_agent import CognitiveAgent

def format_cognitive_process(depth: int, role: str) -> str:
    """Format the cognitive process visualization."""
    prefix = "  " * depth
    process_map = {
        0: "🌟 Primary Observation",
        1: "🔄 Pattern Analysis",
        2: "💭 Emotional Exploration",
        3: "🔮 Integration Synthesis"
    }
    
    return f"\n{prefix}{process_map.get(depth, '🔍 Deep Analysis')} | {role}"

def format_insight(insight: dict, indent: int = 0) -> str:
    """Format insight with enhanced visualization."""
    prefix = "  " * indent
    output = []
    
    # Show cognitive process
    if 'depth' in insight:
        output.append(format_cognitive_process(insight['depth'], insight.get('perspective', 'Observer')))
    
    # Show process boundary
    output.append(f"{prefix}{'═' * (50 - len(prefix))}")
    
    # Handle insights with enhanced formatting
    if isinstance(insight.get('insights'), dict):
        insight_data = insight['insights']
        
        # Handle integrated understanding
        if 'integrated_understanding' in insight_data:
            understanding = insight_data['integrated_understanding']
            
            output.append(colored(f"\n{prefix}🧠 Cognitive Synthesis:", "cyan"))
            
            if 'connected_patterns' in understanding:
                output.append(colored(f"\n{prefix}🔄 Pattern Network:", "yellow"))
                for pattern in understanding['connected_patterns']:
                    output.append(f"{prefix}  ◆ {pattern}")
            
            if 'synthesized_meta_cognition' in understanding:
                output.append(colored(f"\n{prefix}🤔 Meta-Cognitive Layer:", "magenta"))
                output.append(f"{prefix}  {understanding['synthesized_meta_cognition']}")
            
            if 'emergent_understanding' in understanding:
                output.append(colored(f"\n{prefix}💡 Emergent Insight Layer:", "cyan"))
                output.append(f"{prefix}  {understanding['emergent_understanding']}")
        else:
            # Standard insight formatting
            if 'analysis' in insight_data:
                output.append(colored(f"\n{prefix}📝 Cognitive Analysis:", "cyan"))
                output.append(f"{prefix}  {insight_data['analysis']}")
            
            if 'patterns' in insight_data:
                output.append(colored(f"\n{prefix}🔄 Pattern Recognition:", "yellow"))
                for pattern in insight_data['patterns']:
                    output.append(f"{prefix}  ◆ {pattern}")
            
            if 'meta_cognition' in insight_data:
                output.append(colored(f"\n{prefix}🤔 Meta-Cognitive Process:", "magenta"))
                output.append(f"{prefix}  {insight_data['meta_cognition']}")
            
            if 'implications' in insight_data:
                output.append(colored(f"\n{prefix}💭 Cognitive Implications:", "blue"))
                output.append(f"{prefix}  {insight_data['implications']}")
    
    # Show integration metrics with clean formatting
    if 'meta_synthesis' in insight:
        meta = insight['meta_synthesis']
        output.append(colored(f"\n{prefix}📊 Integration Metrics:", "blue"))
        output.append(f"{prefix}  ╭{'─' * 40}╮")
        output.append(f"{prefix}  │ Patterns Connected: {meta['patterns_connected']:<6}     │")
        output.append(f"{prefix}  │ Cognitive Depth:    {meta['depth_reached']:<6}     │")
        output.append(f"{prefix}  │ Integration Score:  {meta['integration_quality']:<6.2f}   │")
        output.append(f"{prefix}  ╰{'─' * 40}╯")
    
    # Show cognitive boundary
    output.append(f"\n{prefix}{'═' * (50 - len(prefix))}")
    
    # Handle recursive exploration
    if 'sub_thoughts' in insight:
        output.append(format_insight(insight['sub_thoughts'], indent + 1))
    
    return "\n".join(output)

async def main():
    try:
        # Create primary cognitive agent
        print(colored("\n🌟 Initializing Cognitive Exploration System", "cyan"))
        primary = CognitiveAgent("Primary Observer")
        
        # Process a thought
        thought = "I feel anxious about making changes in my life"
        print(colored(f"\n💭 Processing Thought: '{thought}'", "white"))
        
        result = await primary.process_thought(thought)
        
        # Display formatted results
        print(colored("\n=== Cognitive Analysis Results ===", "cyan"))
        print(format_insight(result))
        
        # Show meta information
        if 'meta' in result:
            print(colored("\n📊 Meta Information:", "yellow"))
            print(f"  • Agent: {result['meta']['agent']}")
            print(f"  • Context Size: {result['meta']['context_size']}")
            print(f"  • Patterns Recognized: {result['meta']['patterns_recognized']}")
        
        # Save results for analysis
        output_dir = Path(__file__).parent.parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"analysis_{int(asyncio.get_event_loop().time())}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            
        print(colored(f"\n✅ Analysis saved to {output_file}", "green"))
            
    except Exception as e:
        print(colored(f"\n❌ Error: {str(e)}", "red"))

if __name__ == "__main__":
    asyncio.run(main()) 