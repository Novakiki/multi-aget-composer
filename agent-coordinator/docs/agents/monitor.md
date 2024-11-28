# Monitor Agent

The Monitor Agent watches for file changes and coordinates quality checks.

## Usage

```python
from coordinator import MonitorAgent

# Initialize agent
monitor = MonitorAgent()

# Start monitoring current directory
monitor.start(".")

# Monitor runs in background until interrupted
```

## Configuration

The Monitor Agent uses configuration from `agent_standards.py`:

```python
AGENT_CONFIG = {
    "monitor": {
        "check_interval": 1.0,  # seconds
        "ignore_patterns": [
            "*.pyc",
            "__pycache__",
            "*.json"
        ]
    }
}
```

## Features

- Real-time file change detection
- Automatic quality checks
- File type detection
- Priority-based processing
- Status updates

## Methods

### start(path: str = ".")
Starts monitoring a directory for changes.

**Parameters:**
- `path`: Directory to monitor (default: current directory)

### on_modified(event)
Internal method that handles file modification events.

## Communication

The Monitor Agent sends these messages:
- `Monitor starting up`: When initializing
- `File changed: {path}`: When files change
- `# Monitor Agent ready`: When ready for files

## Status Updates

The agent broadcasts its status:
- `WORKING`: While processing changes
- `IDLE`: When waiting for changes
- `ERROR`: If processing fails 