async def test_similarity_search(self, semantics):
    """Test semantic similarity search."""
    semantics = await semantics
    
    # Create test pattern
    pattern_id = "test_pat_1"
    
    # Find similar patterns
    similar = await semantics.find_similar(pattern_id)
    assert len(similar) > 0
    assert similar[0]['score'] > 0.5  # Should have relevance score 