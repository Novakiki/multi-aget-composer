# API Documentation

## Community Integration Endpoints

### Pattern Sharing
```python
POST /api/community/patterns
{
    "pattern": {
        "observation": str,
        "context": dict,
        "questions": list
    }
}
```

### Collective Understanding
```python
GET /api/community/understanding
Returns:
{
    "shared_patterns": list,
    "emerging_insights": list,
    "collective_questions": list
}
```

## CognitiveOrchestrator

### process_thoughts()
```python
async def process_thoughts(
    thoughts: Union[str, List[str]]
) -> Dict:
    """Process single or multiple thoughts.
    
    Args:
        thoughts: Single thought string or list of thoughts
        
    Returns:
        Dict containing:
        - Single: {"patterns": [], "emotions": {}, "synthesis": {}}
        - Multiple: {"results": [{"thought": "", ...}, ...]}
    """
```

### Configuration
```python
PROCESSING_SETTINGS = {
    'PARALLEL_MODE': 'auto',
    'BATCH_THRESHOLD': 3,
    'TIMEOUT': 30,
    'MAX_CONCURRENT': 5
} 
```

## Question-Based Endpoints

### Shared Exploration
```python
POST /api/questions/shared
{
    "question": str,
    "context": Dict,
    "curiosity_level": float
}

Returns:
{
    "resonance": {
        "shared_by": List[str],
        "resonance_score": float,
        "emerging_questions": List[str]
    }
}
```

### Question Evolution
```python
GET /api/questions/evolution
Returns:
{
    "question_paths": List[Dict],
    "understanding_depth": float,
    "collective_insights": List[Dict]
}