# Setup Agent

The Setup Agent is responsible for creating and validating project structure.

## Usage

```python
from coordinator import SetupAgent

# Initialize agent
setup = SetupAgent()

# Create project structure
success = setup.create_structure()
```

## Configuration

The Setup Agent uses configuration from `agent_standards.py`:

```python
AGENT_CONFIG = {
    "setup": {
        "required_dirs": [
            "modules",
            "monitor_config",
            "agents",
            "shared"
        ],
        "required_files": [
            "default.json",
            "create_project.sh",
            "requirements.txt"
        ]
    }
}
```

## Methods

### create_structure()
Creates the required project structure.

**Returns:**
- `bool`: True if successful, False otherwise

### verify_structure()
Verifies all required components exist.

**Returns:**
- `bool`: True if valid, False if missing components

## Communication

The Setup Agent sends the following messages:
- `Creating project structure`: When starting
- `Created directory: {path}`: For each directory
- `Created file: {path}`: For each file
- `# Setup Agent complete`: When finished 