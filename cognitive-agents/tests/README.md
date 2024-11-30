# Test Organization

## Directory Structure
```
tests/
├── unit/                    # Unit tests
│   ├── community/          # Community features
│   │   ├── test_collective_learning.py
│   │   ├── test_pattern_democracy.py
│   │   └── test_wisdom_emergence.py
│   ├── core/               # Core functionality
│   │   ├── test_agent_pool.py
│   │   ├── test_cognitive_agent.py
│   │   └── test_event_bus.py
│   ├── memory/            # Memory components
│   │   ├── test_pattern_store.py
│   │   ├── test_pattern_network.py
│   │   └── test_pattern_semantics.py
│   └── patterns/          # Pattern matching
│       └── test_pattern_matcher.py
├── integration/            # Integration tests
│   ├── pinecone/          # Pinecone integration
│   │   ├── test_pinecone_connection.py
│   │   ├── test_pinecone_index.py
│   │   └── test_pinecone_query.py
│   └── neo4j/            # Neo4j integration
│       ├── test_pattern_network.py
│       ├── test_pattern_network.py
│       └── test_pattern_network.py
└── evolution/             # Evolution tests
    ├── core/             # Core evolution
    └── memory/          # Memory evolution
```

## Memory Tests Organization

### Unit Tests (tests/unit/memory/)
- Pattern Storage: test_pattern_store.py
- Embeddings: test_embeddings.py
- Network: test_pattern_network.py
- Semantics: test_pattern_semantics.py
- Theme Extraction: test_theme_extraction.py
- Question Evolution: test_question_evolution.py
- Pattern Relationships: test_pattern_relationships.py

### Evolution Tests (tests/evolution/memory/)
- Pattern Semantics: test_pattern_semantics_evolution.py
- Natural Connection: test_natural_connection.py
- Pattern History: test_pattern_history.py
- Meta Learning: test_meta_learning.py
- Hybrid Evolution: test_hybrid_evolution.py
- Evolution Stack: test_evolution_stack.py

## Integration Tests
### Neo4j Tests
- Connection: test_pattern_network.py
  - Verifies Neo4j connectivity
  - Tests pattern storage
  - Tests graph relationships

### Running Neo4j Tests
```bash
# Run Neo4j integration tests
pytest -v tests/integration/neo4j/ -s

# Verify Neo4j connection
python verify_neo4j.py
```

## Running Memory Tests
```bash
# Run all memory tests
pytest -v tests/*/memory/

# Run specific categories
pytest -v tests/unit/memory/          # Unit tests
pytest -v tests/evolution/memory/     # Evolution tests
```

## Running Tests
```bash
# Run by category
pytest -v -m unit          # Unit tests
pytest -v -m integration   # Integration tests
pytest -v -m evolution     # Evolution tests

# Run by component
pytest -v tests/unit/memory/       # Memory tests
pytest -v tests/integration/memory/       # Memory tests
pytest -v tests/evolution/memory/        # Memory tests
``` 