"""Integration tests for agent and quality systems."""

import os
import sys
import json
from pathlib import Path
from termcolor import colored

# Add both packages to path
ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT / 'code-quality-tools'))
sys.path.append(str(ROOT / 'agent-coordinator'))

# Import at module level
from coordinator import QualityAgent

def setup_learning_data():
    """Initialize learning system with sample data."""
    learning_file = ROOT / 'code-quality-tools/data/learning_history.json'
    learning_file.parent.mkdir(exist_ok=True)
    
    sample_data = {
        "history": [
            {
                "file": "example.py",
                "issues": ["docstring", "typing"],
                "confidence": 0.85
            },
            {
                "file": "test.py",
                "issues": ["error_handling"],
                "confidence": 0.92
            }
        ],
        "version": "1.0"
    }
    
    with open(learning_file, "w") as f:
        json.dump(sample_data, f, indent=2)
    print(colored("Learning data initialized", "green"))

def setup_module():
    """Set up test module - run once before all tests."""
    print(colored("\n🔧 Setting up test environment", "cyan"))
    setup_learning_data()

def teardown_module():
    """Clean up after all tests."""
    print(colored("\n🧹 Cleaning up test environment", "cyan"))
    learning_file = ROOT / 'code-quality-tools/data/learning_history.json'
    if learning_file.exists():
        os.remove(learning_file)

def reset_quality_monitor():
    """Reset quality monitor state between tests."""
    # Clear learning history
    learning_file = ROOT / 'code-quality-tools/data/learning_history.json'
    if learning_file.exists():
        os.remove(learning_file)
    setup_learning_data()
    
    # Clear any cached results
    quality = QualityAgent()
    quality.monitor._current_results = []
    return quality

def test_quality_integration():
    """Test quality agent using quality tools."""
    try:
        print(colored("\n🧪 Testing Quality Integration", "cyan"))
        quality = reset_quality_monitor()  # Get fresh instance
        
        # Create test file
        test_file = "test_integration.py"
        with open(test_file, "w") as f:
            f.write("""
def example():
    \"\"\"Test function.\"\"\"
    try:
        return 42
    except:
        pass
""")
        
        quality.check_file(test_file)
        os.remove(test_file)
        print(colored("✅ Integration test passed", "green"))
        
    except Exception as e:
        print(colored(f"❌ Test failed: {str(e)}", "red"))
        raise

def test_good_code():
    """Test with well-formatted code."""
    try:
        print(colored("\n🧪 Testing Good Code", "cyan"))
        quality = reset_quality_monitor()  # Get fresh instance
        
        test_file = "good_test.py"
        with open(test_file, "w") as f:
            f.write("""
def calculate_sum(numbers: list[float]) -> float:
    \"\"\"Calculate sum of numbers.
    
    Args:
        numbers: List of numbers to sum
        
    Returns:
        float: The total sum
    \"\"\"
    try:
        return sum(numbers)
    except TypeError as e:
        print(f"Error: {e}")
        return 0.0
""")
        
        quality.check_file(test_file)
        os.remove(test_file)
        print(colored("✅ Good code test passed", "green"))
        
    except Exception as e:
        print(colored(f"❌ Test failed: {str(e)}", "red"))
        raise

if __name__ == "__main__":
    test_quality_integration()
    test_good_code() 