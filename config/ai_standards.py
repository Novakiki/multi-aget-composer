"""AI configuration and standards."""

import os
from typing import Dict, Optional, List
from openai import OpenAI
from termcolor import colored

# Constants
AI_MODELS = {
    'DEFAULT': 'gpt-4',
    'FAST': 'gpt-3.5-turbo',
    'DETAILED': 'gpt-4-turbo-preview'
}

class AIQualityAnalyzer:
    """AI-powered code quality analyzer."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        if not os.getenv('OPENAI_API_KEY'):
            print(colored("Warning: OPENAI_API_KEY not found", "yellow"))
    
    async def analyze_code(self, code: str, model: str = AI_MODELS['DEFAULT']) -> Optional[Dict]:
        """Analyze code quality using AI."""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": f"Analyze this Python code for quality:\n\n{code}"
                }],
                temperature=0.1
            )
            
            return {
                "issues": [],
                "score": 0,
                "suggestions": response.choices[0].message.content
            }
            
        except Exception as e:
            print(colored(f"AI analysis failed: {str(e)}", "red"))
            return None
    
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