"""Demonstration of agents communicating with each other."""

import os
import sys
import time
from termcolor import colored

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def run_demo():
    """Run the agent communication demonstration."""
    try:
        print(colored("\n🤝 Agent Communication Demo", "cyan"))
        print(colored("=" * 50, "cyan"))
        
        # Initialize communication
        from agents.shared.communication import AgentCommunication
        from agents.shared.patterns import AgentStatus
        comm = AgentCommunication()
        
        # Setup Agent starts work
        print(colored("\n1. Setup Agent Starting", "cyan"))
        comm.broadcast_status("setup", AgentStatus.WORKING)
        comm.notify_agents("Creating project structure", "SetupAgent")
        time.sleep(1)
        
        # Setup Agent finishes
        comm.broadcast_status("setup", AgentStatus.IDLE)
        comm.notify_agents("# Setup Agent complete", "SetupAgent")
        time.sleep(1)
        
        # Monitor Agent responds
        print(colored("\n2. Monitor Agent Responding", "cyan"))
        if comm.wait_for_signal("Setup Agent complete"):
            comm.broadcast_status("monitor", AgentStatus.WORKING)
            comm.notify_agents("Starting file monitoring", "MonitorAgent")
            time.sleep(1)
            
            comm.broadcast_status("monitor", AgentStatus.IDLE)
            comm.notify_agents("# Monitor Agent ready", "MonitorAgent")
        
        print(colored("\n✅ Demo completed", "green"))
        
    except Exception as e:
        print(colored(f"\n❌ Demo failed: {str(e)}", "red"))

if __name__ == "__main__":
    run_demo() 