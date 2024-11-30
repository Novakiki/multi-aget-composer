# Quick Start Guide

## Core Concept
The system enables natural learning through:
- Question evolution
- Pattern emergence
- Meta-awareness

## Prerequisites
- Python 3.9+
- MongoDB 5.0+
- Neo4j 4.4+
- Pinecone account

## Installation
```bash
# Clone repository
git clone https://github.com/your-org/evolution-system.git

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Key Files to Understand
1. **Meta Learning**
```python
cognitive_agents/memory/meta_learning.py
# Shows how meta-awareness emerges
```

2. **Natural Connection**
```python
cognitive_agents/memory/natural_connection.py
# Shows how understanding flows
```

3. **Tests**
```python
tests/memory/test_meta_learning.py
tests/memory/test_natural_connection.py
# Show system in action
```

## Running Tests
```bash
# Test meta learning
pytest -v -s tests/memory/test_meta_learning.py

# Test natural connection
pytest -v -s tests/memory/test_natural_connection.py
```

## Troubleshooting
1. Check logs in /var/log/evolution-system/
2. Verify environment variables are set
3. Ensure database connections are active

## Next Development Areas
1. Pattern Recognition
2. Question Evolution
3. Meta-Awareness
4. Performance Optimization
5. Error Recovery