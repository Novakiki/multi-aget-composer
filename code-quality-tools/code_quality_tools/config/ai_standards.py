"""AI-powered code quality analysis."""

import os
import json
from typing import Dict
from termcolor import colored
from openai import AsyncOpenAI

class AIQualityAnalyzer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        if not os.getenv('OPENAI_API_KEY'):
            print(colored("Warning: OPENAI_API_KEY not found", "yellow"))
            self.mock_mode = True
        else:
            self.mock_mode = False
            print(colored("AI Quality Analyzer initialized", "green"))

    async def analyze_code(self, content: str) -> Dict:
        """Analyze code using AI."""
        try:
            if self.mock_mode:
                return self._mock_analysis()

            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": """You are a code quality analyzer. Analyze the code and return a JSON response with this structure:
                    {
                        "quality_score": float between 0-1,
                        "suggestions": list of improvement suggestions,
                        "issues": list of specific issues found,
                        "confidence": float between 0-1
                    }"""
                }, {
                    "role": "user",
                    "content": f"Analyze this code and return json: {content}"
                }],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            print(colored("✓ AI analysis complete", "green"))
            return result

        except Exception as e:
            print(colored(f"AI analysis error: {str(e)}", "red"))
            return self._mock_analysis()

    def _mock_analysis(self) -> Dict:
        """Fallback mock analysis when AI unavailable."""
        print(colored("Using mock analysis", "yellow"))
        return {
            "quality_score": 0.7,
            "suggestions": [
                "Add more detailed docstrings",
                "Consider adding type hints",
                "Add error handling"
            ],
            "issues": [
                {"type": "documentation", "severity": "medium", "message": "Brief docstring"},
                {"type": "typing", "severity": "low", "message": "Missing type hints"}
            ],
            "confidence": 0.5
        }