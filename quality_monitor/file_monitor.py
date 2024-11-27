"""File monitoring module."""

from typing import Dict, Optional, Set
from watchdog.events import FileSystemEventHandler
from termcolor import colored
from datetime import datetime
from pathlib import Path

from .quality_monitor import QualityMonitor

class FileChangeHandler(FileSystemEventHandler):
    """Handles file system events."""
    
    def __init__(self):
        self.quality_monitor = QualityMonitor()
        self.active_files: Set[str] = set()
        print(colored("File Change Handler initialized", "green"))

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            self.quality_monitor.check_file(event.src_path)