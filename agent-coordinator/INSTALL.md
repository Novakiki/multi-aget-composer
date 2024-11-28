# Installation

## Development Install

```bash
# Clone repository
git clone https://github.com/Novakiki/multi-agent-composer.git
cd multi-agent-composer

# Install code-quality-tools
cd code-quality-tools
pip install -e .

# Install agent-coordinator
cd ../agent-coordinator
pip install -e .
```

## Testing Installation

```python
from coordinator import SetupAgent, MonitorAgent, QualityAgent

# Should work without errors
agents = [SetupAgent(), MonitorAgent(), QualityAgent()]
print("✅ Installation successful")
``` 