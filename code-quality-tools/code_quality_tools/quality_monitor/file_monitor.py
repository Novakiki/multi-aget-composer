"""File monitoring with async support."""

import asyncio
from watchdog.events import FileSystemEventHandler
from termcolor import colored
from pathlib import Path

class FileChangeHandler(FileSystemEventHandler):
    """Handles file system events."""
    
    def __init__(self):
        self.quality_monitor = None  # Will be set later
        self.loop = None  # Will be set later
        print(colored("File Change Handler initialized", "green"))

    def set_event_loop(self, loop, quality_monitor):
        """Set the event loop and quality monitor for async operations."""
        self.loop = loop
        self.quality_monitor = quality_monitor

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(colored(f"\nFile changed: {event.src_path}", "cyan"))
            if self.loop and self.quality_monitor:
                asyncio.run_coroutine_threadsafe(
                    self.quality_monitor.check_file(event.src_path),
                    self.loop
                )