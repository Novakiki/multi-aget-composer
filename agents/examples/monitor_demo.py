"""Demonstration of Monitor Agent working with Setup Agent."""

import os
import sys
import time
from termcolor import colored

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def run_demo():
    """Run the monitoring system demonstration."""
    try:
        print(colored("\n🔄 Monitor Agent Demo", "cyan"))
        print(colored("=" * 50, "cyan"))
        
        # First run setup
        from agents.setup.setup_agent import SetupAgent
        setup = SetupAgent()
        
        if not setup.create_structure():
            print(colored("❌ Setup failed, cannot start monitor", "red"))
            return
            
        # Start monitoring
        from agents.monitor.monitor_agent import MonitorAgent
        monitor = MonitorAgent()
        
        print(colored("\nStarting file monitoring...", "cyan"))
        monitor.start(".")
        
        # Demo file changes
        print(colored("\nSimulating file changes...", "cyan"))
        test_file = "test_changes.txt"
        
        # Create file
        with open(test_file, "w") as f:
            f.write("Initial content")
        time.sleep(2)
        
        # Modify file
        with open(test_file, "a") as f:
            f.write("\nModified content")
        time.sleep(2)
        
        # Cleanup
        os.remove(test_file)
        print(colored("\n✅ Demo completed", "green"))
        
    except Exception as e:
        print(colored(f"\n❌ Demo failed: {str(e)}", "red"))
        
    finally:
        print(colored("\nPress Ctrl+C to exit", "yellow"))

if __name__ == "__main__":
    run_demo() 