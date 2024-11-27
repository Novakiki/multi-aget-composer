"""Test real AI integration with OpenAI."""

import pytest
import asyncio
import os
from pathlib import Path
from termcolor import colored

from quality_monitor.ai_integration import IntegratedQualityChecker

# Test code samples
GOOD_CODE = '''
def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers to average
        
    Returns:
        float: The calculated average
        
    Raises:
        ValueError: If list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
'''

BAD_CODE = '''
def x(a):
    try:
        if a:
            if a > 0:
                if a < 10:
                    return [i for i in range(a)]
    except: pass
'''

@pytest.mark.asyncio
async def test_ai_analysis():
    """Test real AI code analysis."""
    if not os.getenv('OPENAI_API_KEY'):
        pytest.skip("OPENAI_API_KEY not set")
    
    checker = IntegratedQualityChecker()
    
    # Test good code
    results = await checker.check_code(GOOD_CODE)
    assert results["score"] > 50, "Good code should score well"
    assert len(results["issues"]) == 0, "Good code should have no issues"
    
    # Test bad code
    results = await checker.check_code(BAD_CODE)
    assert results["score"] < 50, "Bad code should score poorly"
    assert len(results["issues"]) > 0, "Bad code should have issues"
    assert any("nesting" in str(i).lower() for i in results["issues"]), "Should catch deep nesting"

if __name__ == "__main__":
    asyncio.run(test_ai_analysis()) 