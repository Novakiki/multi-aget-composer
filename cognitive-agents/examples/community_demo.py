"""Demonstrate community pattern validation."""

async def demo_community_validation():
    # Initialize system
    pattern_store = CommunityPatternStore()
    
    # Example pattern proposal
    pattern = {
        'theme': 'Growth Mindset',
        'evidence': ['Learning from challenges'],
        'context': 'Personal Development'
    }
    
    # Community validation flow
    pattern_id = await pattern_store.submit_pattern(pattern)
    await pattern_store.vote_on_pattern(pattern_id, 'validator1', 'upvote')
    
    # Show validation status
    status = await pattern_store.get_validation_status(pattern_id)
    print(f"Pattern Status: {status}") 