"""Simple demonstration of code quality checks."""

import os
import sys
from termcolor import colored

# Add parent directory to path so we can import quality_monitor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Bad code example (this is what we'll check)
BAD_CODE = '''
def risky_function():
    try:
        x = input()  # Unsafe!
        exec(x)      # Very unsafe!
    except:
        pass        # Silent failure!
'''

def main():
    """Run the demo."""
    try:
        from quality_monitor import QualityMonitor
        monitor = QualityMonitor()
        
        # Create temporary file with bad code
        print(colored("\n🔍 Checking Bad Code:", "cyan"))
        print(colored("-------------------", "cyan"))
        
        with open("bad_example.py", "w", encoding="utf-8") as f:
            f.write(BAD_CODE)
        
        # Run the check
        monitor.check_file("bad_example.py")
        
        # Get and print report
        report = monitor.generate_report()
        print(report)
        
    except Exception as e:
        print(colored(f"\n❌ Error: {str(e)}", "red"))
    finally:
        # Clean up
        if os.path.exists("bad_example.py"):
            os.remove("bad_example.py")

if __name__ == "__main__":
    main() 