"""Quality monitoring system with AI integration."""

import asyncio
from pathlib import Path
from typing import Dict, List
from termcolor import colored

from ..config.ai_standards import AIQualityAnalyzer

class QualityMonitor:
    def __init__(self):
        self.ai_analyzer = AIQualityAnalyzer()
        print(colored("Quality Monitor initialized", "green"))

    async def check_file(self, file_path: str) -> Dict:
        """Check file quality with AI assistance."""
        try:
            print(colored(f"\nAnalyzing {file_path}...", "cyan"))
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get AI analysis
            analysis = await self.ai_analyzer.analyze_code(content)
            
            # Process results
            self._update_learning_system(file_path, analysis)
            
            return analysis
            
        except Exception as e:
            print(colored(f"Error checking file: {str(e)}", "red"))
            return {"error": str(e)}

    def _update_learning_system(self, file_path: str, analysis: Dict) -> None:
        """Update learning system with new results."""
        try:
            if analysis.get("quality_score", 0) > 0.8:
                print(colored("✓ High quality code detected", "green"))
            elif analysis.get("suggestions"):
                print(colored("! Suggestions found:", "yellow"))
                for suggestion in analysis["suggestions"]:
                    print(colored(f"  • {suggestion}", "yellow"))
        except Exception as e:
            print(colored(f"Learning system error: {str(e)}", "red"))