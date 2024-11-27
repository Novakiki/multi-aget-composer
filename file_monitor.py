import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from termcolor import colored
from datetime import datetime
from pathlib import Path
from typing import Set, Dict, Optional

from agent_learning_system import AgentLearningSystem
from quality_monitor import QualityMonitor

class FileChangeHandler(FileSystemEventHandler):
    """Handles file system events and coordinates with learning system."""
    
    def __init__(self):
        self.learning_system = AgentLearningSystem()
        self.quality_monitor = QualityMonitor()
        
        # Track active files
        self.active_files: Set[str] = set()
        self.last_modified: Dict[str, datetime] = {}
        
        print(colored("File Change Handler initialized", "green"))

    def on_modified(self, event):
        if not event.src_path.endswith('.py'):
            return
            
        file_path = event.src_path
        filename = os.path.basename(file_path)
        
        # Avoid processing the same change multiple times
        current_time = datetime.now()
        if (file_path in self.last_modified and 
            (current_time - self.last_modified[file_path]).total_seconds() < 1):
            return
            
        self.last_modified[file_path] = current_time
        
        try:
            # Register file activity
            self.active_files.add(file_path)
            
            # Notify learning system
            context = {
                "file": filename,
                "time": current_time.isoformat(),
                "type": "modification"
            }
            
            # Determine active agent from file changes
            agent_id = self._detect_active_agent(file_path)
            if agent_id:
                self.learning_system.register_agent_action(
                    agent_id=agent_id,
                    action="file_modified",
                    context=context
                )
            
            # Run quality check
            quality_report = self.quality_monitor.check_file(file_path)
            
            # Update learning system with quality results
            if agent_id:
                self.learning_system.update_quality_impact(agent_id, quality_report)
            
            print(colored(f"Processed changes in {filename}", "cyan"))
            
        except Exception as e:
            print(colored(f"Error processing {filename}: {str(e)}", "red"))

    def _detect_active_agent(self, file_path: str) -> Optional[str]:
        """Detect which agent is working on the file based on content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for agent markers
            for agent_id in ["Agent 0", "Agent 1", "Agent 2", "Agent 3", "Agent 4"]:
                if f"# {agent_id}" in content:
                    return agent_id
                    
        except Exception as e:
            print(colored(f"Error detecting agent: {str(e)}", "yellow"))
        
        return None

def start_monitoring(path: str = "."):
    """Start the file monitoring system."""
    print(colored("Starting file monitoring...", "cyan"))
    print(colored(f"Monitoring directory: {path}", "cyan"))
    
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(colored("\nStopping file monitor...", "yellow"))
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    start_monitoring() 