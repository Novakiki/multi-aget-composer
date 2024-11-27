"""Demonstration of Setup Agent functionality."""

import os
import sys
from termcolor import colored

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def run_demo():
    """Run the setup agent demonstration."""
    try:
        print(colored("\n🚀 Setup Agent Demo", "cyan"))
        print(colored("=" * 50, "cyan"))
        
        # Import and initialize
        from agents.setup.setup_agent import SetupAgent
        agent = SetupAgent()
        
        # Step 1: Create Structure
        print(colored("\n1. Creating Project Structure", "cyan"))
        if agent.create_structure():
            print(colored("✅ Structure created successfully", "green"))
        else:
            print(colored("❌ Structure creation failed", "red"))
            return
        
        # Step 2: Verify Structure
        print(colored("\n2. Verifying Structure", "cyan"))
        if agent.verify_structure():
            print(colored("✅ Structure verified successfully", "green"))
        else:
            print(colored("❌ Structure verification failed", "red"))
            
    except Exception as e:
        print(colored(f"\n❌ Demo failed: {str(e)}", "red"))

if __name__ == "__main__":
    run_demo() 