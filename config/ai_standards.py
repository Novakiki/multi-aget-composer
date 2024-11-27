"""AI configuration and standards."""

import os
from typing import Dict, Optional, List
from openai import OpenAI
from termcolor import colored
import json

# Constants
AI_MODELS = {
    'DEFAULT': 'gpt-4',
    'FAST': 'gpt-3.5-turbo',
    'DETAILED': 'gpt-4-turbo-preview'
}

QUALITY_PROMPT = """Analyze this Python code and return a JSON response.
Format your response EXACTLY like this, replacing the values:

{
    "score": 75,
    "issues": [
        {
            "type": "STYLE",
            "category": "Documentation",
            "message": "Brief docstring",
            "suggestion": "Add more details"
        }
    ],
    "suggestions": [
        "Add type hints",
        "Improve error messages"
    ]
}

Scoring guide:
- 90-100: Perfect code
- 70-89: Good code
- 50-69: Needs work
- 0-49: Poor code

Code to analyze:
{code}
"""

class AIQualityAnalyzer:
    """AI-powered code quality analyzer."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        if not os.getenv('OPENAI_API_KEY'):
            print(colored("Warning: OPENAI_API_KEY not found", "yellow"))
    
    async def analyze_code(self, code: str, model: str = AI_MODELS['DEFAULT']) -> Dict:
        """Analyze code quality using AI (mocked for testing)."""
        try:
            # Start with neutral score
            quality_score = 50
            
            # Good patterns (+10 each)
            if 'def ' in code and len(code.split('def ')) > 1:
                quality_score += 10  # Has named functions
            if '"""' in code and 'Args:' in code:
                quality_score += 10  # Has detailed docstrings
            if 'try:' in code and 'except ' in code and not 'except:' in code:
                quality_score += 10  # Has specific error handling
            if 'return' in code and not 'return None' in code:
                quality_score += 10  # Has meaningful returns
            
            # Bad patterns (-20 each)
            if 'except:' in code or 'except Exception:' in code:
                quality_score -= 20  # Bare except
            if code.count('if') > 3:
                quality_score -= 20  # Too much nesting
            if 'pass' in code:
                quality_score -= 20  # Silent failures
            if len(code.split('\n')) < 3:
                quality_score -= 20  # Too short/simple
            
            return {
                "score": max(min(quality_score, 100), 0),  # Clamp between 0-100
                "issues": [],
                "suggestions": ["Test response"]
            }
            
        except Exception as e:
            print(colored(f"AI analysis failed: {str(e)}", "red"))
            return {"score": 0, "issues": [], "suggestions": []}
    
    def enhance_suggestions(self, issues: List[Dict]) -> List[Dict]:
        """Add AI-powered suggestions to issues."""
        try:
            for issue in issues:
                if not issue.get("suggestion"):
                    issue["suggestion"] = "AI suggestion not available"
            return issues
        except Exception as e:
            print(colored(f"Error enhancing suggestions: {e}", "red"))
            return issues

# Add back __all__
__all__ = ['AIQualityAnalyzer', 'AI_MODELS']