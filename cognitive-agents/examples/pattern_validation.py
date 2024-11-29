"""Demonstrate the community pattern validation system."""
from typing import Dict
from termcolor import colored
import asyncio

from cognitive_agents.pattern_store.community_patterns import CommunityPatternStore
from cognitive_agents.visualization.pattern_viz import PatternVisualizer

async def demonstrate_pattern_validation():
    """Show complete pattern validation flow."""
    print(colored("\n🔍 Community Pattern Validation Demo", "cyan"))
    
    # Initialize stores
    pattern_store = CommunityPatternStore()
    visualizer = PatternVisualizer()
    
    # Example pattern proposal
    pattern = {
        'theme': 'Growth Mindset',
        'evidence': [
            'Learning from challenges',
            'Embracing feedback',
            'Continuous improvement'
        ],
        'context': 'Personal Development',
        'applicability': 0.85,
        'initial_validation': {
            'clarity_score': 0.9,
            'uniqueness_score': 0.8
        }
    }
    
    try:
        # 1. Submit Pattern
        print(colored("\n1. Submitting Pattern", "cyan"))
        pattern_id = await pattern_store.submit_pattern(
            pattern=pattern,
            proposer_id="community_member_1"
        )
        
        # 2. Initial Validation
        print(colored("\n2. Initial Community Testing", "cyan"))
        validators = [
            ("validator_1", "upvote", "Strong evidence base"),
            ("validator_2", "refinement", "Add resilience aspect"),
            ("validator_3", "upvote", "Clear practical value")
        ]
        
        for validator_id, vote_type, feedback in validators:
            await pattern_store.vote_on_pattern(
                pattern_id=pattern_id,
                voter_id=validator_id,
                vote_type=vote_type,
                feedback=feedback
            )
            
        # 3. Check Status
        print(colored("\n3. Validation Status", "cyan"))
        status = await pattern_store.get_validation_status(pattern_id)
        
        # 4. Visualize Progress
        print(colored("\n4. Pattern Evolution", "cyan"))
        visualizer.show_pattern_evolution([{
            'pattern_id': pattern_id,
            'status': status,
            'validation_metrics': pattern_store.get_validation_metrics(pattern_id)
        }])
        
        return pattern_id, status
        
    except Exception as e:
        print(colored(f"❌ Error in validation demo: {str(e)}", "red"))
        return None, None

async def main():
    """Run the complete demonstration."""
    pattern_id, status = await demonstrate_pattern_validation()
    if pattern_id:
        print(colored("\n✅ Pattern validation demo completed", "green"))
        
if __name__ == "__main__":
    asyncio.run(main()) 