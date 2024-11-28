"""File monitoring agent."""

import asyncio
from pathlib import Path
from typing import Dict, Optional
from termcolor import colored
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .base_agent import BaseAgent

class FileEventHandler(FileSystemEventHandler):
    """Handles file system events for the agent."""
    
    def __init__(self, agent):
        self.agent = agent
        self.loop = None
        
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            if self.loop:
                asyncio.run_coroutine_threadsafe(
                    self.agent.handle_file_change(event.src_path),
                    self.loop
                )

class FileMonitorAgent(BaseAgent):
    """Agent responsible for monitoring file changes."""
    
    def __init__(self):
        super().__init__("FileMonitorAgent")
        self.observer = Observer()
        self.event_handler = FileEventHandler(self)
        self.watched_paths = set()
        
    def watch_directory(self, path: str) -> None:
        """Start watching a directory."""
        try:
            path = str(Path(path).resolve())
            if path not in self.watched_paths:
                # Set the event loop for the handler
                self.event_handler.loop = asyncio.get_event_loop()
                self.observer.schedule(self.event_handler, path, recursive=False)
                self.watched_paths.add(path)
                print(colored(f"Watching directory: {path}", "green"))
        except Exception as e:
            print(colored(f"Error watching directory: {str(e)}", "red"))
    
    async def start(self) -> None:
        """Start the file monitor."""
        self.observer.start()
        print(colored("File Monitor Agent started", "green"))
    
    async def stop(self) -> None:
        """Stop the file monitor."""
        self.observer.stop()
        self.observer.join()
        print(colored("File Monitor Agent stopped", "yellow"))
    
    async def handle_message(self, message: Dict) -> Optional[Dict]:
        """Handle incoming messages."""
        try:
            if message.get('type') == 'watch_directory':
                self.watch_directory(message['path'])
            return None
        except Exception as e:
            print(colored(f"Error handling message: {str(e)}", "red"))
            return None
    
    async def handle_file_change(self, file_path: str) -> None:
        """Handle file change event."""
        try:
            await self.send_message({
                'type': 'file_change',
                'file_path': file_path
            })
            print(colored(f"File change detected: {file_path}", "cyan"))
        except Exception as e:
            print(colored(f"Error handling file change: {str(e)}", "red")) 