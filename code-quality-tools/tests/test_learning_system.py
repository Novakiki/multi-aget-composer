"""
Test suite for the Learning System.

Tests the core functionality of pattern learning, issue prediction,
and system adaptation.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from quality_monitor.quality_monitor import LearningSystem
from config.quality_standards import (
    LEARNING_THRESHOLDS,
    MIN_DOCSTRING_WORDS
)

# Test Data
GOOD_CODE = '''
def calculate_sum(numbers):
    """Calculate sum of numbers."""
    return sum(numbers)

def process_data(data):
    """Process input data safely."""
    try:
        result = calculate_sum(data)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None
'''

BAD_CODE = '''
def x():
    try:
        if a:
            if b:
                if c:
                    d()
    except Exception:
        pass
'''

@pytest.fixture
def learning_system():
    """Create a fresh learning system for each test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        system = LearningSystem()
        system.history_file = Path(tmpdir) / "test_history.json"
        yield system

def test_pattern_learning(learning_system):
    """Test that system learns from good patterns."""
    # Create a test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f:
        f.write(GOOD_CODE)
        f.flush()
        
        # Learn from file
        learning_system.learn_from_file(f.name, [], {"lines": 10, "comments": 2})
        
        # Check patterns were learned
        assert len(learning_system.patterns["successful_patterns"]) > 0
        
        # Verify pattern quality
        patterns = learning_system.patterns["successful_patterns"]
        assert any("try:" in p for p in patterns)
        assert any("def" in p for p in patterns)

def test_issue_prediction(learning_system):
    """Test that system predicts potential issues."""
    # Create a test file with known issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f:
        f.write(BAD_CODE)
        f.flush()
        
        # Add some learning history
        learning_system.patterns["issue_patterns"].update({
            "CRITICAL:Nesting": 5,
            "IMPORTANT:Documentation": 3
        })
        
        # Get predictions
        predictions = learning_system._predict_potential_issues(BAD_CODE)
        
        # Verify predictions
        assert len(predictions) > 0
        assert any(p["type"] == "CRITICAL" for p in predictions)
        assert any("Nesting" in p["message"] for p in predictions)

def test_confidence_calculation(learning_system):
    """Test confidence scoring."""
    # Add some history
    learning_system.patterns["successful_patterns"]["pattern1"] = 5
    learning_system.patterns["successful_patterns"]["pattern2"] = 3
    
    # Calculate confidence
    confidence = learning_system._calculate_pattern_confidence(5)
    
    # Verify confidence
    assert 0 <= confidence <= 1
    assert confidence > learning_system._calculate_pattern_confidence(1)

def test_effectiveness_tracking(learning_system):
    """Test effectiveness tracking over time."""
    file_path = "test.py"
    
    # Track multiple checks
    for i in range(3):
        learning_system._update_effectiveness(
            file_path,
            [{"type": "STYLE", "category": "Documentation"}] if i == 0 else [],
            {"lines": 10, "comments": 2}
        )
    
    # Verify tracking
    effectiveness = learning_system.patterns["effectiveness"][file_path]
    assert len(effectiveness) == 3
    assert effectiveness[-1]["issues_found"] == 0  # Last check had no issues
    assert "learning_confidence" in effectiveness[-1]

def test_adaptation(learning_system):
    """Test system adaptation based on learning."""
    learning_system.patterns["successful_patterns"].update({
        "pattern1": 10,
        "pattern2": 8
    })
    
    learning_system._adapt_thresholds()
    
    # Check adjustments list
    adjustments = learning_system.patterns["threshold_adjustments"]["adjustments"]
    assert len(adjustments) > 0
    assert all(isinstance(adj["confidence"], float) for adj in adjustments)

if __name__ == "__main__":
    pytest.main([__file__]) 