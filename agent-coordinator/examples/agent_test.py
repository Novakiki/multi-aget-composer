"""Test the agent system with real code examples."""

import os
import sys
import time
from pathlib import Path
from termcolor import colored

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def run_test():
    """Run the agent system test."""
    try:
        print(colored("\n🚀 Agent System Test", "cyan"))
        print(colored("=" * 50, "cyan"))
        
        # Step 1: Initialize Agents
        print(colored("\n1. Initializing Agents", "cyan"))
        from coordinator import SetupAgent, MonitorAgent, QualityAgent
        
        setup = SetupAgent()
        monitor = MonitorAgent()
        quality = QualityAgent()
        
        # Step 2: Create Test Files
        print(colored("\n2. Creating Test Files", "cyan"))
        test_file = "test_code.py"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("""
def example_function(x: int) -> int:
    \"\"\"Example function for testing.\"\"\"
    try:
        return x + 1
    except Exception as e:
        print(f"Error: {e}")
        return 0
""")
        
        # Step 3: Run Quality Check
        print(colored("\n3. Running Quality Check", "cyan"))
        quality.check_file(test_file)
        
        # Clean up
        os.remove(test_file)
        print(colored("\n✅ Test completed", "green"))
        
    except Exception as e:
        print(colored(f"\n❌ Test failed: {str(e)}", "red"))
        raise

if __name__ == "__main__":
    run_test() 