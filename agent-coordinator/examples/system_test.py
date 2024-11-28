"""Test the complete agent coordination system."""

import os
import sys
import time
from pathlib import Path
from termcolor import colored

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def run_test():
    """Run complete system test."""
    try:
        print(colored("\n🚀 Agent System Test", "cyan"))
        print(colored("=" * 50, "cyan"))
        
        # Step 1: Setup Agent
        print(colored("\n1. Testing Setup Agent", "cyan"))
        from coordinator import SetupAgent
        setup = SetupAgent()
        
        if not setup.create_structure():
            print(colored("❌ Setup failed", "red"))
            return
        
        # Step 2: Monitor Agent
        print(colored("\n2. Testing Monitor Agent", "cyan"))
        from coordinator import MonitorAgent
        monitor = MonitorAgent()
        
        # Step 3: Test File Changes
        print(colored("\n3. Testing File Handling", "cyan"))
        test_files = [
            ("good_code.py", """
def calculate_sum(numbers: list[float]) -> float:
    \"\"\"Calculate sum of numbers.\"\"\"
    return sum(numbers)
"""),
            ("bad_code.py", """
def x():
    try: return input()
    except: pass
""")
        ]
        
        # Create and check files
        for filename, content in test_files:
            print(colored(f"\nTesting {filename}...", "cyan"))
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            time.sleep(1)  # Wait for monitor
            
            # Clean up
            os.remove(filename)
        
        print(colored("\n✅ System test completed", "green"))
        
    except Exception as e:
        print(colored(f"\n❌ Test failed: {str(e)}", "red"))
        raise

if __name__ == "__main__":
    run_test() 