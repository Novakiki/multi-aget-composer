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
│   └── pinecone/          # Pinecone integration
│       ├── test_pinecone_connection.py
│       ├── test_pinecone_index.py
│       └── test_pinecone_query.py
└── evolution/             # Evolution tests
    ├── core/             # Core evolution
    └── memory/          # Memory evolution
```

## Running Tests
```bash
# Run by category
pytest -v -m unit          # Unit tests
pytest -v -m integration   # Integration tests
pytest -v -m evolution     # Evolution tests

# Run by component
pytest -v tests/unit/memory/       # Memory tests
pytest -v tests/integration/       # Integration tests
pytest -v tests/evolution/        # Evolution tests
``` 