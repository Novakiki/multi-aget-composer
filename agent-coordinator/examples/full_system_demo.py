"""Demonstration of the complete agent system working together."""

import os
import sys
import time
from pathlib import Path
from termcolor import colored

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def run_demo():
    """Run the complete system demonstration."""
    try:
        print(colored("\n🚀 Complete System Demo", "cyan"))
        print(colored("=" * 50, "cyan"))
        
        # Step 1: Initialize Setup Agent
        print(colored("\n1. Initializing Setup Agent", "cyan"))
        from agents.setup.setup_agent import SetupAgent
        setup = SetupAgent()
        
        # Step 2: Create Project Structure
        print(colored("\n2. Creating Project Structure", "cyan"))
        if not setup.create_structure():
            print(colored("❌ Setup failed", "red"))
            return
            
        # Step 3: Start Monitor Agent
        print(colored("\n3. Starting Monitor Agent", "cyan"))
        from agents.monitor.monitor_agent import MonitorAgent
        monitor = MonitorAgent()
        
        # Step 4: Begin Monitoring
        print(colored("\n4. Starting File Monitoring", "cyan"))
        monitor.start(".")
        
        # Step 5: Demonstrate File Changes
        print(colored("\n5. Testing File Changes", "cyan"))
        test_files = [
            ("good_code.py", """
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
"""),
            ("bad_code.py", """
def x():
    try: return input()
    except: pass
""")
        ]
        
        # Create and modify files
        for filename, content in test_files:
            # Create file
            print(colored(f"\nCreating {filename}...", "cyan"))
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            time.sleep(2)  # Wait for detection
            
            # Modify file
            print(colored(f"Modifying {filename}...", "cyan"))
            with open(filename, "a", encoding="utf-8") as f:
                f.write("\n# Modified")
            time.sleep(2)  # Wait for detection
            
            # Clean up
            os.remove(filename)
        
        print(colored("\n✅ Demo completed successfully", "green"))
        
    except Exception as e:
        print(colored(f"\n❌ Demo failed: {str(e)}", "red"))
    finally:
        print(colored("\nPress Ctrl+C to exit monitoring", "yellow"))

if __name__ == "__main__":
    run_demo() 