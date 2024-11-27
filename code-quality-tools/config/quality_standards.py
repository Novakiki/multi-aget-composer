"""
Quality Standards Configuration

This module defines the quality thresholds and standards used throughout the system.
"""

# Code Structure Standards
MAX_FUNCTION_LINES = 25        # Balance between flexibility and maintainability
MAX_NESTED_DEPTH = 3           # Keep nesting manageable
MAX_LINE_LENGTH = 80           # Standard line length
MIN_COMMENT_RATIO = 0.12       # Reasonable comment coverage

# Documentation Standards
MIN_DOCSTRING_WORDS = 10       # Ensure meaningful docs
REQUIRED_SECTIONS = [
    "Description",
    "Usage",
    "Examples"
]

# Learning Thresholds
LEARNING_THRESHOLDS = {
    'min_success_ratio': 0.8,  # Learn from good code
    'pattern_min_length': 5,   # Meaningful patterns
    'max_issues_to_learn': 1   # Limited issues allowed
}

__all__ = [
    'MAX_FUNCTION_LINES',
    'MAX_NESTED_DEPTH',
    'MAX_LINE_LENGTH',
    'MIN_COMMENT_RATIO',
    'MIN_DOCSTRING_WORDS',
    'REQUIRED_SECTIONS',
    'LEARNING_THRESHOLDS'
] 