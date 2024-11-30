# Test Organization

## Directory Structure
```
tests/
├── unit/              # Unit tests
│   ├── memory/       # Memory component tests
│   ├── core/         # Core functionality tests
│   └── advanced/     # Advanced feature tests
├── integration/       # Integration tests
│   ├── pinecone/     # Pinecone integration
│   ├── mongodb/      # MongoDB integration
│   └── neo4j/        # Neo4j integration
└── evolution/        # Evolution tests
    ├── memory/       # Memory evolution
    └── core/         # Core evolution
```

## Running Tests
```bash
# Run specific test types
pytest -v -m unit          # Unit tests
pytest -v -m integration   # Integration tests
pytest -v -m evolution    # Evolution tests

# Run specific components
pytest -v tests/unit/memory/       # Memory unit tests
pytest -v tests/integration/       # All integration tests
``` 