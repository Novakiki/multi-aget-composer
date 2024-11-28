# Quality Agent

The Quality Agent analyzes code quality using AI-powered tools and learning systems.

## Usage

```python
from coordinator import QualityAgent

# Initialize agent
quality = QualityAgent()

# Check a specific file
quality.check_file("example.py")
```

## Configuration

The Quality Agent uses settings from `quality_standards.py`:

```python
QUALITY_CHECKS = {
    "docstring": {
        "required": True,
        "min_length": 10,
        "style": "google"
    },
    "typing": {
        "required": True,
        "check_returns": True,
        "check_args": True
    },
    "error_handling": {
        "require_specific": True,
        "no_bare_except": True,
        "require_logging": True
    }
}

FILE_TYPES = {
    "python": {
        "extensions": [".py", ".pyi"],
        "priority": "high",
        "checks": ["docstring", "typing", "error_handling"]
    }
}
```

## Features

- AI-powered code analysis
- Language-specific checks
- Learning from code patterns
- Priority-based reporting
- Detailed suggestions

## Methods

### check_file(file_path: str)
Analyzes a file for quality issues.

**Parameters:**
- `file_path`: Path to file to check

**Output Example:**
```
Quality Report for example.py (python)
==================================================
Running Checks: docstring, typing, error_handling

✅ Good documentation
⚠️ Consider adding return type hints
⚠️ Specific exception handling recommended

Learning Status:
- Confidence: 0.92
- Priority: high
``` 