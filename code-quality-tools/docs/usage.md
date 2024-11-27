# Usage Guide

## Quick Start

```python
from quality_monitor import QualityMonitor

# Initialize
monitor = QualityMonitor()

# Check a file
results = monitor.check_file("your_code.py")

# Generate report
report = monitor.generate_report()
```

## Features

### Security Checks
- Detects unsafe patterns
- Validates input handling
- Checks file operations
- Monitors system calls

### Performance Analysis
- Function complexity
- Loop efficiency
- Memory usage patterns
- Resource handling

### Learning System
- Adapts to your patterns
- Learns from good code
- Tracks improvements
- Suggests optimizations
