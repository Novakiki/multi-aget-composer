"""Simple test of the agent coordination system."""

import os
import sys
from pathlib import Path
from termcolor import colored

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_imports():
    """Test that all imports work."""
    try:
        print(colored("\n🔍 Testing Imports", "cyan"))
        
        # Test coordinator imports
        from coordinator import SetupAgent, MonitorAgent, QualityAgent
        print(colored("✅ Core imports work", "green"))
        
        # Test agent initialization
        setup = SetupAgent()
        monitor = MonitorAgent()
        quality = QualityAgent()
        print(colored("✅ Agents initialize", "green"))
        
        # Test basic functionality
        test_file = "test_code.py"
        with open(test_file, "w") as f:
            f.write("def test(): pass\n")
        
        print(colored("\n🔄 Testing File Handling", "cyan"))
        quality.check_file(test_file)
        os.remove(test_file)
        print(colored("✅ File handling works", "green"))
        
    except Exception as e:
        print(colored(f"\n❌ Test failed: {str(e)}", "red"))
        raise

if __name__ == "__main__":
    test_imports() 