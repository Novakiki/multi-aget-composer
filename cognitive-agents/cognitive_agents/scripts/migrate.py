async def migrate_patterns():
    """Migrate existing patterns to new architecture."""
    # 1. Extract from current store
    old_patterns = await old_store.get_all_patterns()
    
    # 2. Migrate to new stores
    for pattern in old_patterns:
        # Semantic patterns to Pinecone
        await evolution_core.store_semantic_pattern(pattern)
        
        # Knowledge network to Neo4j
        await evolution_core.create_pattern_node(pattern)
        
        # Rich context to MongoDB
        await evolution_core.store_pattern_context(pattern) 