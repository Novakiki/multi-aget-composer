"""
Integration Test Suite

Tests the complete workflow of the quality monitoring system.
"""

import pytest
import os
import tempfile
import time
from pathlib import Path
from watchdog.observers import Observer
from termcolor import colored

from quality_monitor.quality_monitor import QualityMonitor
from quality_monitor.file_monitor import FileChangeHandler
from config.quality_standards import (
    MAX_FUNCTION_LINES,
    MAX_NESTED_DEPTH,
    MIN_DOCSTRING_WORDS,
    MIN_COMMENT_RATIO,
    LEARNING_THRESHOLDS
)

# Constants for test data and examples
SAMPLE_SIZE_MIN = 1
EXAMPLE_VALUES = [1.0, 2.0]  # Simple example for docstrings
EXAMPLE_AVERAGE = 1.5        # Pre-calculated for examples

GOOD_CODE = '''"""
Example Module

Description:
    Shows clean code patterns with a simple counter example.

Usage:
    from counter import count_positive_numbers
    result = count_positive_numbers([1, -2, 3])

Examples:
    >>> numbers = [1, -2, 3]
    >>> count = count_positive_numbers(numbers)
    >>> print(f"Positive numbers: {count}")
    Positive numbers: 2
"""

from typing import List

# Constants for validation
MIN_LIST_SIZE = 1
DEFAULT_RETURN = 0

def count_positive_numbers(numbers: List[int]) -> int:
    """
    Count how many positive numbers are in a list.
    
    Description:
        Simple function that counts numbers greater than zero.
    
    Args:
        numbers: List of integers to check
        
    Returns:
        int: Count of positive numbers
        
    Examples:
        >>> result = count_positive_numbers([1, -2, 3])
        >>> print(result)
        2
    """
    # Input validation
    if not numbers:
        print("Error: Empty list provided")
        return DEFAULT_RETURN
        
    try:
        # Count positive numbers using clear variable names
        positive_count = sum(1 for num in numbers if num > 0)
        return positive_count
        
    except TypeError as e:
        # Log error with helpful message
        print(f"Error counting numbers: {str(e)}")
        return DEFAULT_RETURN
'''

BAD_CODE = '''
def x(a):
    """Do stuff."""
    try:
        # Deeply nested code
        if a:
            if a > 0:
                if a < 10:
                    for i in range(a):
                        try:
                            # Magic number
                            if i == 42:
                                # Clever hack
                                return [j for j in range(i) if j % 2]
                        except:  # Broad exception
                            pass  # Silent failure
                            
    except Exception:  # Another broad exception
        return None  # No error info
'''

@pytest.fixture
def test_environment():
    """Set up a test environment with temporary files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test directory structure
        test_dir = Path(tmpdir)
        (test_dir / "src").mkdir()
        (test_dir / "monitor_data").mkdir()
        
        # Create test files
        good_file = test_dir / "src" / "good_code.py"
        bad_file = test_dir / "src" / "bad_code.py"
        
        with open(good_file, 'w', encoding='utf-8') as f:
            f.write(GOOD_CODE)
        with open(bad_file, 'w', encoding='utf-8') as f:
            f.write(BAD_CODE)
            
        yield {
            "dir": test_dir,
            "good_file": good_file,
            "bad_file": bad_file
        }

def test_complete_workflow(test_environment):
    """Test the entire quality monitoring workflow."""
    
    # 1. Initialize monitoring system
    monitor = QualityMonitor()
    handler = FileChangeHandler()
    observer = Observer()
    
    try:
        # 2. Start file monitoring
        observer.schedule(handler, str(test_environment["dir"]), recursive=True)
        observer.start()
        print(colored("\nMonitoring system started", "cyan"))
        
        # 3. Check good code
        print(colored("\nChecking good code...", "cyan"))
        monitor.check_file(test_environment["good_file"])
        good_issues = monitor.issues.get(str(test_environment["good_file"]), [])
        
        # Verify good code results
        assert len(good_issues) == 0, "Good code should have no issues"
        assert len(monitor.learning_system.patterns["successful_patterns"]) > 0
        
        # 4. Check bad code
        print(colored("\nChecking bad code...", "cyan"))
        monitor.check_file(test_environment["bad_file"])
        bad_issues = monitor.issues.get(str(test_environment["bad_file"]), [])
        
        # Verify bad code results
        assert len(bad_issues) > 0, "Bad code should have issues"
        assert any("complexity" in str(issue).lower() for issue in bad_issues)
        
        # 5. Verify learning
        print(colored("\nVerifying learning system...", "cyan"))
        learning_system = monitor.learning_system
        
        # Check pattern learning
        assert len(learning_system.patterns["successful_patterns"]) > 0
        assert len(learning_system.patterns["issue_patterns"]) > 0
        
        # Check effectiveness tracking
        assert len(learning_system.patterns["effectiveness"]) > 0
        
        # 6. Generate and verify report
        print(colored("\nGenerating report...", "cyan"))
        report = monitor.generate_report()
        
        # Verify report content
        assert "Code Quality Report" in report
        assert "good_code.py" in report
        assert "bad_code.py" in report
        
        print(colored("\nIntegration test completed successfully", "green"))
        
    finally:
        observer.stop()
        observer.join()

def test_system_adaptation(test_environment):
    """Test system's ability to adapt and learn."""
    monitor = QualityMonitor()
    
    # 1. Initial learning phase
    print(colored("\nInitial learning phase...", "cyan"))
    monitor.check_file(test_environment["good_file"])
    initial_patterns = len(monitor.learning_system.patterns["successful_patterns"])
    
    # 2. Adaptation phase
    print(colored("\nAdaptation phase...", "cyan"))
    for _ in range(3):  # Multiple checks to allow adaptation
        monitor.check_file(test_environment["good_file"])
        monitor.check_file(test_environment["bad_file"])
    
    # 3. Verify adaptation
    final_patterns = len(monitor.learning_system.patterns["successful_patterns"])
    assert final_patterns >= initial_patterns, "System should learn new patterns"
    
    # 4. Check confidence growth
    confidence = monitor.learning_system._calculate_learning_confidence()
    assert 0 <= confidence <= 1, "Confidence should be normalized"
    print(colored(f"\nSystem confidence: {confidence:.2f}", "cyan"))

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])