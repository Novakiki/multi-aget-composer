"""Test suite for CLI adaptive timeouts."""
import pytest
from cognitive_agents.cli import _calculate_timeout

@pytest.mark.parametrize("thought,has_previous_patterns,expected", [
    # Simple thoughts (base: 10s)
    ("I am tired", False, 10),
    
    # Abstract thoughts (+2s)
    ("I feel deeply connected", False, 12),
    ("I think this matters", False, 12),
    
    # Long thoughts (+2s)
    ("This is a very long thought that should definitely trigger the length complexity factor in our system", False, 12),
    
    # With previous patterns (+3s)
    ("Simple follow-up", True, 13),
    
    # Combined complexity
    ("I feel this is a very complex and deep thought that requires significant processing", True, 15),  # Abstract +2, Length +2, Patterns +3
])
def test_timeout_calculation(thought, has_previous_patterns, expected):
    """Test timeout calculations for different scenarios."""
    timeout = _calculate_timeout(thought, has_previous_patterns)
    assert timeout == expected 