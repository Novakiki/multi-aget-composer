"""Quality monitoring core module."""

import ast
from typing import Dict, List, Optional
from termcolor import colored
from pathlib import Path
import json
from datetime import datetime

from config.quality_standards import (
    MAX_FUNCTION_LINES,
    MAX_NESTED_DEPTH,
    MAX_LINE_LENGTH,
    MIN_COMMENT_RATIO,
    MIN_DOCSTRING_WORDS,
    REQUIRED_SECTIONS,
    LEARNING_THRESHOLDS
)
from .checkers import StyleChecker, DocumentationChecker, ComplexityChecker

class LearningSystem:
    """Learns from code quality patterns."""
    
    def __init__(self):
        self.history_file = Path("monitor_data/learning_history.json")
        self.history_file.parent.mkdir(exist_ok=True)
        self.patterns = {
            "successful_patterns": {},
            "issue_patterns": {},
            "effectiveness": {},
            "threshold_adjustments": {}
        }
        print(colored("Learning System initialized", "green"))
    
    def learn_from_file(self, file_path: str, issues: List[Dict], stats: Dict) -> None:
        """Learn from file analysis results."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Learn from successful patterns if few issues
            if len(issues) <= LEARNING_THRESHOLDS['max_issues_to_learn']:
                self._update_successful_patterns(content)
            
            # Learn from issues found
            self._update_issue_patterns(issues)
            
            # Track effectiveness
            self._update_effectiveness(file_path, issues, stats)
            
        except Exception as e:
            print(colored(f"Learning error: {str(e)}", "yellow"))
    
    def _update_successful_patterns(self, content: str) -> None:
        """Update patterns from successful code."""
        try:
            # Extract meaningful code patterns
            lines = content.split('\n')
            for i in range(len(lines) - 1):  # Look at pairs of lines
                pattern = lines[i].strip()
                next_pattern = lines[i + 1].strip()
                
                # Store individual patterns
                if len(pattern) >= LEARNING_THRESHOLDS['pattern_min_length']:
                    self.patterns["successful_patterns"][pattern] = \
                        self.patterns["successful_patterns"].get(pattern, 0) + 1
                
                # Store pattern pairs (like try-except)
                if pattern and next_pattern:
                    pair = f"{pattern}\n{next_pattern}"
                    self.patterns["successful_patterns"][pair] = \
                        self.patterns["successful_patterns"].get(pair, 0) + 1
                    
        except Exception as e:
            print(colored(f"Error updating patterns: {e}", "yellow"))
    
    def _update_issue_patterns(self, issues: List[Dict]) -> None:
        """Update patterns from issues found."""
        try:
            for issue in issues:
                key = f"{issue['type']}:{issue['category']}"
                self.patterns["issue_patterns"][key] = \
                    self.patterns["issue_patterns"].get(key, 0) + 1
                    
        except Exception as e:
            print(colored(f"Error updating issues: {e}", "yellow"))
    
    def _update_effectiveness(self, file_path: str, issues: List[Dict], stats: Dict) -> None:
        """Track effectiveness of quality checks."""
        try:
            if file_path not in self.patterns["effectiveness"]:
                self.patterns["effectiveness"][file_path] = []
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "issues_found": len(issues),
                "stats": stats,
                "learning_confidence": self._calculate_learning_confidence()
            }
            
            self.patterns["effectiveness"][file_path].append(result)
            
        except Exception as e:
            print(colored(f"Error updating effectiveness: {e}", "yellow"))
    
    def _calculate_learning_confidence(self) -> float:
        """Calculate current confidence in learning system."""
        try:
            pattern_count = len(self.patterns["successful_patterns"])
            issue_count = len(self.patterns["issue_patterns"])
            
            if pattern_count + issue_count == 0:
                return 0.0
            
            return pattern_count / (pattern_count + issue_count)
            
        except Exception as e:
            print(colored(f"Error calculating confidence: {e}", "yellow"))
            return 0.0
    
    def _predict_potential_issues(self, code: str) -> List[Dict]:
        """Predict potential issues based on learning history."""
        try:
            predictions = []
            for pattern, count in self.patterns["issue_patterns"].items():
                if count >= 3:  # Pattern occurs frequently
                    issue_type, message = pattern.split(':', 1)
                    predictions.append({
                        "type": issue_type,
                        "message": message,
                        "confidence": count / max(len(self.patterns["issue_patterns"]), 1)
                    })
            return sorted(predictions, key=lambda x: x["confidence"], reverse=True)
        except Exception as e:
            print(colored(f"Error predicting issues: {e}", "yellow"))
            return []
    
    def _calculate_pattern_confidence(self, frequency: int) -> float:
        """Calculate confidence for a specific pattern."""
        total = sum(self.patterns["successful_patterns"].values())
        return frequency / max(total, 1)
    
    def _adapt_thresholds(self) -> None:
        """Adapt quality thresholds based on learning."""
        try:
            confidence = self._calculate_learning_confidence()
            self.patterns["threshold_adjustments"] = {
                "adjustments": [  # List of adjustment objects
                    {
                        "confidence": confidence,
                        "threshold": "max_line_length",
                        "current": MAX_LINE_LENGTH,
                        "suggested": MAX_LINE_LENGTH + (5 if confidence > 0.8 else 0)
                    },
                    {
                        "confidence": confidence,
                        "threshold": "min_docstring_words",
                        "current": MIN_DOCSTRING_WORDS,
                        "suggested": MIN_DOCSTRING_WORDS - (2 if confidence > 0.9 else 0)
                    }
                ]
            }
        except Exception as e:
            print(colored(f"Error adapting thresholds: {e}", "yellow"))

class QualityMonitor:
    """Main quality monitoring class."""
    
    def __init__(self):
        self.learning_system = LearningSystem()
        self.checkers = [
            StyleChecker(),
            DocumentationChecker(),
            ComplexityChecker()
        ]
        self.issues: Dict[str, List[Dict]] = {}
        print(colored("Quality Monitor initialized", "green"))
    
    def check_file(self, file_path: str) -> None:
        """Run quality checks on a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            all_issues = []
            
            # Run checks
            for checker in self.checkers:
                issues = checker.check(content, tree)
                all_issues.extend(issues)
            
            # Store results
            self.issues[str(file_path)] = all_issues
            
            # Learn from results
            stats = self._gather_statistics(content, tree)
            self.learning_system.learn_from_file(file_path, all_issues, stats)
            
        except Exception as e:
            print(colored(f"Error checking {file_path}: {e}", "red"))
            
    def _gather_statistics(self, content: str, tree: ast.AST) -> Dict:
        """Gather code statistics."""
        return {
            "lines": len(content.split('\n')),
            "functions": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
            "classes": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
        }
    
    def generate_report(self) -> str:
        """Generate a quality report."""
        report = ["Code Quality Report", "=" * 20]
        
        # Summarize issues
        for file_path, file_issues in self.issues.items():
            report.append(f"\nFile: {file_path}")
            if not file_issues:
                report.append("✅ No issues found")
            else:
                for issue in file_issues:
                    report.append(
                        f"⚠️  {issue['type']}: {issue['message']}\n"
                        f"   Suggestion: {issue['suggestion']}"
                    )
        
        # Add learning insights
        confidence = self.learning_system._calculate_learning_confidence()
        report.append(f"\nLearning Confidence: {confidence:.2f}")
        
        return "\n".join(report)