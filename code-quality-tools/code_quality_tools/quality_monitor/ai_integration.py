"""AI integration for quality checking."""

import ast
import os
from typing import Dict, List, Optional
from termcolor import colored

from . import QualityMonitor  # Import from same directory
from ..config.ai_standards import AIQualityAnalyzer

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
        """Run both standard and AI-powered checks on code."""
        results = {
            "score": 0,
            "issues": [],
            "suggestions": []
        }
        
        try:
            # Parse code for standard checks
            tree = ast.parse(code)
            
            # Run standard checks
            standard_issues = []
            for checker in self.standard_checker.checkers:
                issues = checker.check(code, tree)
                standard_issues.extend(issues)
            
            # Get AI analysis
            print(colored("\nRunning AI analysis...", "cyan"))
            ai_result = await self.ai_checker.analyze_code(code)
            
            if ai_result:
                # Combine all issues
                all_issues = standard_issues + ai_result.get("issues", [])
                
                # Update results
                results.update({
                    "score": ai_result.get("score", 0),
                    "issues": all_issues,  # Include both standard and AI issues
                    "suggestions": ai_result.get("suggestions", [])
                })
            
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