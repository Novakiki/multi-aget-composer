"""Quality standards and thresholds for code analysis."""

from typing import Dict, List

# Code Quality Standards
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
    },
    "naming": {
        "function_style": "snake_case",
        "class_style": "PascalCase",
        "constant_style": "UPPER_CASE"
    }
}

# Learning Thresholds
LEARNING_CONFIG = {
    "min_confidence": 0.8,
    "max_history": 1000,
    "update_frequency": 10
}

# Report Settings
REPORT_CONFIG = {
    "show_suggestions": True,
    "max_issues": 5,
    "priority_levels": ["HIGH", "MEDIUM", "LOW"],
    "output_format": "text"
}

# File Type Standards
FILE_TYPES = {
    "python": {
        "extensions": [".py", ".pyi"],
        "priority": "high",
        "checks": ["docstring", "typing", "error_handling", "naming"]
    },
    "markdown": {
        "extensions": [".md", ".markdown"],
        "priority": "medium",
        "checks": ["formatting", "links"]
    },
    "config": {
        "extensions": [".json", ".yaml", ".yml"],
        "priority": "low",
        "checks": ["syntax", "schema"]
    }
}
