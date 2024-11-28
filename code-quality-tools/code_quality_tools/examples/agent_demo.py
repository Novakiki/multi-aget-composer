"""Demo of agent coordination system."""

import asyncio
from pathlib import Path
from termcolor import colored
from ..agents import AgentCoordinator
from ..agents.quality_agent import QualityAgent
from ..agents.file_monitor_agent import FileMonitorAgent

async def main():
    try:
        # Initialize coordinator
        coordinator = AgentCoordinator()
        
        # Create and register agents
        file_monitor = FileMonitorAgent()
        quality_agent = QualityAgent()
        
        coordinator.register_agent(file_monitor)
        coordinator.register_agent(quality_agent)
        
        # Start message processing
        process_task = asyncio.create_task(coordinator.process_messages())
        
        # Create test directory
        watch_dir = Path("test_watch_dir")
        watch_dir.mkdir(exist_ok=True)
        
        # Start file monitor
        await file_monitor.start()
        
        # Tell monitor to watch directory
        await coordinator.route_message(
            "System",
            {
                'type': 'watch_directory',
                'path': str(watch_dir)
            }
        )
        
        # Create test file
        test_file = watch_dir / "test_script.py"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("""
def example():
    \"\"\"Test function\"\"\"
    return True
            """)
        
        # Wait for initial analysis
        await asyncio.sleep(2)
        
        # Modify file to trigger another analysis
        with open(test_file, "a", encoding="utf-8") as f:
            f.write("""

def another_function():
    # TODO: Add documentation
    x = 1
    return x + 42
            """)
            
        # Wait for second analysis
        await asyncio.sleep(2)
        
    except Exception as e:
        print(colored(f"\n❌ Error: {str(e)}", "red"))
    finally:
        # Cleanup
        await file_monitor.stop()
        process_task.cancel()
        try:
            await process_task
        except asyncio.CancelledError:
            pass
        
        # Remove test directory
        import shutil
        shutil.rmtree(watch_dir, ignore_errors=True)

if __name__ == "__main__":
    asyncio.run(main()) 