"""Test AI-enhanced quality checking."""

import pytest
from quality_monitor.ai_integration import IntegratedQualityChecker

# Test code samples
GOOD_CODE = '''
def greet(name: str) -> str:
    """Return a greeting message.
    
    Args:
        name: Person to greet
        
    Returns:
        Greeting message
    """
    return f"Hello, {name}!"
'''

BAD_CODE = '''
def x(a):
    try: return a
    except: pass
'''

@pytest.mark.asyncio
async def test_integrated_checker():
    """Test that integrated checker works."""
    checker = IntegratedQualityChecker()
    
    # Check good code
    results = await checker.check_code(GOOD_CODE)
    assert results["score"] > 50, "Good code should score well"
    
    # Check bad code
    results = await checker.check_code(BAD_CODE)
    assert results["score"] < 50, "Bad code should score poorly"
    assert len(results["suggestions"]) > 0, "Should have suggestions" 