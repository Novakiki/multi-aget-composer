"""
Monitor Usage Example

This example demonstrates how to use the quality monitoring system
to check code quality and get feedback.
"""

import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Check for required packages
try:
    from termcolor import colored
except ImportError:
    print("Error: termcolor package is required. Install with:")
    print("pip install termcolor")
    sys.exit(1)

try:
    from quality_monitor.quality_monitor import QualityMonitor
    from quality_monitor.file_monitor import FileChangeHandler
    from quality_monitor.ai_integration import IntegratedQualityChecker
except ImportError as e:
    print(f"Error importing project modules: {e}")
    print("Make sure you're in the correct directory and all files exist.")
    sys.exit(1)

def demonstrate_monitor():
    """Show practical usage of the quality monitoring system."""
    
    # Initialize the monitor
    print(colored("\n1. Initializing Quality Monitor", "cyan"))
    monitor = QualityMonitor()
    
    # Example: Check a single file
    print(colored("\n2. Checking Single File", "cyan"))
    example_file = "examples/sample_code.py"
    monitor.check_file(example_file)
    
    # Get and display report
    print(colored("\n3. Generating Quality Report", "cyan"))
    report = monitor.generate_report()
    print(report)
    
    # Example: Check multiple files
    print(colored("\n4. Checking Multiple Files", "cyan"))
    python_files = [f for f in os.listdir(".") if f.endswith(".py")]
    for file in python_files:
        print(colored(f"\nAnalyzing {file}...", "yellow"))
        monitor.check_file(file)
    
    # Get learning insights
    print(colored("\n5. Learning System Insights", "cyan"))
    learning_data = monitor.learning_system.patterns
    print("\nSuccessful Patterns:", len(learning_data["successful_patterns"]))
    print("Issues Identified:", len(learning_data["issue_patterns"]))
    
    # Show adaptations
    print(colored("\n6. System Adaptations", "cyan"))
    adaptations = learning_data.get("threshold_adjustments", {})
    for param, adjustment in adaptations.items():
        print(f"\nParameter: {param}")
        print(f"Current: {adjustment['current']}")
        print(f"Suggested: {adjustment['suggested']}")
        print(f"Confidence: {adjustment['confidence']:.2f}")

def create_sample_code():
    """Create a sample Python file for demonstration."""
    sample_code = '''
def example_function(x, y):
    """Calculate something."""
    result = x + y
    return result

class ExampleClass:
    """A simple example class."""
    
    def __init__(self):
        self.value = 0
    
    def process(self, data):
        # This is a comment
        if data > 0:
            if self.value > 0:
                if data > self.value:
                    # Deep nesting example
                    return data
        return None
'''
    
    with open("examples/sample_code.py", "w", encoding="utf-8") as f:
        f.write(sample_code)

def main():
    """Run the demonstration."""
    print(colored("Quality Monitor Usage Demonstration", "green", attrs=["bold"]))
    print("=" * 50)
    
    # Create example directory and sample code
    os.makedirs("examples", exist_ok=True)
    create_sample_code()
    
    try:
        demonstrate_monitor()
    except Exception as e:
        print(colored(f"\nError during demonstration: {str(e)}", "red"))
    finally:
        # Cleanup - Fixed to handle non-empty directory
        try:
            if os.path.exists("examples/sample_code.py"):
                os.remove("examples/sample_code.py")
            # Don't try to remove examples directory as it contains our script
        except Exception as e:
            print(colored(f"Cleanup error: {e}", "yellow"))

if __name__ == "__main__":
    main() 