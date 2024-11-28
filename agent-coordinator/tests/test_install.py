"""Test package installation and imports."""

import os
import sys
from pathlib import Path
from termcolor import colored

def test_imports():
    """Test that all components can be imported."""
    try:
        print(colored("\n🧪 Testing Package Imports", "cyan"))
        
        # Test coordinator imports
        from coordinator import SetupAgent, MonitorAgent, QualityAgent
        print(colored("✅ Core imports work", "green"))
        
        # Test quality tools imports
        from quality_monitor import QualityMonitor
        print(colored("✅ Quality tools imports work", "green"))
        
        # Test agent creation
        agents = [SetupAgent(), MonitorAgent(), QualityAgent()]
        print(colored("✅ Agents initialize", "green"))
        
    except Exception as e:
        print(colored(f"\n❌ Import test failed: {str(e)}", "red"))
        raise

if __name__ == "__main__":
    test_imports() 