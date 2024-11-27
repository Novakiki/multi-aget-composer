"""AI-enhanced quality monitoring."""

import ast
from typing import Dict, List, Optional
from termcolor import colored
import json

from .quality_monitor import QualityMonitor
from config.ai_standards import AIQualityAnalyzer

class IntegratedQualityChecker:
    """Combines traditional and AI-powered quality checks."""
    
    def __init__(self):
        """Initialize both standard and AI checkers."""
        try:
            self.standard_checker = QualityMonitor()
            self.ai_checker = AIQualityAnalyzer()
            print(colored("Integrated Quality Checker initialized", "green"))
        except Exception as e:
            print(colored(f"Error initializing checkers: {e}", "red"))
            raise
    
    async def check_code(self, code: str) -> Dict:
        """
        Run both standard and AI-powered checks on code.
        
        Args:
            code: Source code to analyze
            
        Returns:
            Combined analysis results
        """
        results = {
            "standard_issues": [],
            "ai_issues": [],
            "suggestions": [],
            "score": 0
        }
        
        try:
            # Parse code for standard checks
            tree = ast.parse(code)
            
            # Run standard checks directly
            all_issues = []
            for checker in self.standard_checker.checkers:
                issues = checker.check(code, tree)
                all_issues.extend(issues)
            
            results["standard_issues"] = all_issues
            
            # Get AI analysis
            print(colored("\nRunning AI analysis...", "cyan"))
            ai_result = await self.ai_checker.analyze_code(code)
            
            if ai_result:
                # Parse AI results
                ai_data = json.loads(ai_result)
                results["ai_issues"] = ai_data.get("issues", [])
                results["score"] = ai_data.get("score", 0)
                
                # Get enhanced suggestions
                results["suggestions"] = self._enhance_suggestions(
                    results["standard_issues"],
                    results["ai_issues"]
                )
            
            return results
            
        except Exception as e:
            print(colored(f"Error during code analysis: {e}", "red"))
            return results
    
    def _enhance_suggestions(self, standard_issues: List[Dict], ai_issues: List[Dict]) -> List[Dict]:
        """Combine and enhance suggestions from both sources."""
        try:
            enhanced = []
            
            # Process standard issues
            for issue in standard_issues:
                suggestion = {
                    "source": "standard",
                    "type": issue["type"],
                    "message": issue["message"],
                    "suggestion": issue.get("suggestion", "No suggestion available")
                }
                enhanced.append(suggestion)
            
            # Process AI issues
            for issue in ai_issues:
                suggestion = {
                    "source": "ai",
                    "type": issue["type"],
                    "message": issue["message"],
                    "suggestion": issue.get("suggestion", "No AI suggestion available")
                }
                enhanced.append(suggestion)
            
            return enhanced
            
        except Exception as e:
            print(colored(f"Error enhancing suggestions: {e}", "yellow"))
            return [] 