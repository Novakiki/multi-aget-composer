"""Simple demo of async quality monitoring."""

import asyncio
import os
from pathlib import Path
from termcolor import colored
from ..quality_monitor import QualityMonitor

async def main():
    try:
        print(colored("\n🚀 Starting Quality Monitor Demo", "cyan"))
        
        # Initialize monitor
        monitor = QualityMonitor()
        
        # Example Python file to check
        test_file = "test_code.py"
        
        # Create a test file
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("""
def example_function():
    \"\"\"This is a test function.\"\"\"
    return True
            """)
        
        # Run async analysis
        print(colored("\nAnalyzing test file...", "cyan"))
        results = await monitor.check_file(test_file)
        
        # Show results
        print(colored("\nAnalysis Results:", "cyan"))
        print(f"Quality Score: {results.get('quality_score', 'N/A')}")
        if results.get('suggestions'):
            print("\nSuggestions:")
            for suggestion in results['suggestions']:
                print(f"• {suggestion}")
                
    except Exception as e:
        print(colored(f"\n❌ Error: {str(e)}", "red"))
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    asyncio.run(main()) 