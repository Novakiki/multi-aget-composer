"""Example of async file monitoring."""

import asyncio
import sys
import time
from pathlib import Path
from termcolor import colored
from watchdog.observers import Observer
from ..quality_monitor import FileChangeHandler, QualityMonitor

async def run():
    """Main async function."""
    # Set start time at beginning of run
    run.start_time = time.time()
    
    try:
        print(colored("\n🔍 Starting File Monitor", "cyan"))
        
        # Create test directory
        watch_dir = Path("test_watch_dir")
        watch_dir.mkdir(exist_ok=True)
        
        # Set up file monitoring
        event_handler = FileChangeHandler()
        event_handler.set_event_loop(
            asyncio.get_running_loop(),
            QualityMonitor()
        )
        
        observer = Observer()
        observer.schedule(event_handler, str(watch_dir), recursive=False)
        observer.start()
        
        print(colored(f"\n👀 Watching directory: {watch_dir}", "green"))
        print(colored("📝 Create or modify .py files to test", "yellow"))
        print(colored("Press Ctrl+C to stop", "yellow"))
        
        # Create a test file to demonstrate monitoring
        test_file = watch_dir / "test_script.py"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("""
def example():
    \"\"\"Test function\"\"\"
    x = 1  # Add some code to trigger analysis
    return x + 1
            """)
            
        # Keep the script running and handle file changes
        while True:
            await asyncio.sleep(1)
            # Simulate a file modification after 5 seconds
            if not hasattr(run, "modified") and time.time() - run.start_time > 5:
                print(colored("\n📝 Modifying test file...", "cyan"))
                with open(test_file, "a", encoding="utf-8") as f:
                    f.write("""
def another_function():
    \"\"\"Another test\"\"\"
    return True
                    """)
                run.modified = True
            
    except KeyboardInterrupt:
        print(colored("\n⏹️  Stopping monitor...", "yellow"))
        observer.stop()
            
    except Exception as e:
        print(colored(f"\n❌ Error: {str(e)}", "red"))
    finally:
        # Cleanup
        observer.join()
        import shutil
        shutil.rmtree(watch_dir, ignore_errors=True)
        print(colored("\n✅ Monitor stopped and cleanup complete", "green"))

def main():
    """Entry point for the command line tool."""
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print(colored("\n⏹️  Monitor stopped by user", "yellow"))
    except Exception as e:
        print(colored(f"\n❌ Error: {str(e)}", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main() 