# Evolution Testing Patterns

## Core Principles
1. Natural Evolution
   - Test how patterns emerge
   - Verify connection formation
   - Track semantic understanding

2. Test Independence
   - Use "test-key" to bypass external services
   - Mock only what's necessary
   - Keep tests focused and clear

3. Three Dimensions
   - Storage Tests (MongoDB)
   - Network Tests (Neo4j)
   - Semantic Tests (Pinecone)

## Implementation Patterns

### 1. Service Bypass Pattern
```python
class PatternSemantics:
    def __init__(self, network, api_key: str):
        # Bypass external services in tests
        if api_key == "test-key":
            self.pc = None
            self.index = None
            return
```

### 2. Test Setup Pattern
```python
@pytest.fixture
async def semantics(self):
    """Create test semantic understanding system."""
    mock_network = AsyncMock()
    
    # Create test instance
    semantics = PatternSemantics(
        network=mock_network,
        api_key="test-key"
    )
    
    # Mock just what we need
    semantics.index = AsyncMock()
    return semantics
```

### 3. Evolution Testing Pattern
```python
async def test_pattern_evolution(self, semantics):
    """Test natural pattern emergence."""
    pattern = {
        'content': 'Learning emerges naturally',
        'themes': ['learning', 'evolution']
    }
    
    # Test pattern storage
    pattern_id = await store_pattern(pattern)
    
    # Test connection formation
    await connect_pattern(pattern_id)
    
    # Test semantic understanding
    similar = await find_similar(pattern_id)
    assert len(similar) > 0
```

## Best Practices
1. Test Natural Flow
   - Follow real usage patterns
   - Test complete evolution cycles
   - Verify pattern connections

2. Mock Minimally
   - Only mock external services
   - Keep internal logic intact
   - Use realistic test data

3. Clear Assertions
   - Test pattern emergence
   - Verify connections
   - Check semantic relationships