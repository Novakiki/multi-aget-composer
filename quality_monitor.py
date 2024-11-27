import ast
import os
from termcolor import colored
from typing import Dict, List, Set, Tuple, Protocol
from datetime import datetime
from abc import ABC, abstractmethod
from collections import defaultdict
import json
from pathlib import Path

# Constants
from config.quality_standards import (
    MAX_FUNCTION_LINES,
    MAX_NESTED_DEPTH,
    MIN_DOCSTRING_WORDS,
    MIN_COMMENT_RATIO,
    MAX_LINE_LENGTH,
    ALLOWED_SHORT_NAMES
)

class QualityChecker(ABC):
    """Base class for all quality checkers."""
    
    @abstractmethod
    def check(self, content: str, tree: ast.AST) -> List[Dict]:
        """Run quality checks and return list of issues."""
        pass

class CodeStructureChecker(QualityChecker):
    """Checks code structure: function length, nesting, etc."""
    
    def check(self, content: str, tree: ast.AST) -> List[Dict]:
        issues = []
        self._check_function_length(tree, issues)
        self._check_nesting_depth(tree, issues)
        return issues
    
    def _check_function_length(self, tree: ast.AST, issues: List[Dict]):
        """Check function length against standards."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                length = len(node.body)
                if length > MAX_FUNCTION_LINES:
                    issues.append({
                        "type": "CRITICAL",
                        "category": "Code Structure",
                        "message": f"Function '{node.name}' is too long ({length} lines)",
                        "suggestion": "Break into smaller, focused functions"
                    })

    def _check_nesting_depth(self, tree: ast.AST, issues: List[Dict]):
        """Check nesting depth for complexity."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                depth = self._get_max_depth(node)
                if depth > MAX_NESTED_DEPTH:
                    issues.append({
                        "type": "CRITICAL",
                        "category": "Code Structure",
                        "message": f"Deep nesting in '{node.name}' (depth: {depth})",
                        "suggestion": "Extract nested logic into helper functions"
                    })

    def _get_max_depth(self, node: ast.AST, current: int = 0) -> int:
        """Calculate maximum nesting depth."""
        max_depth = current
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While, ast.If, ast.With)):
                child_depth = self._get_max_depth(child, current + 1)
                max_depth = max(max_depth, child_depth)
        return max_depth

class DocumentationChecker(QualityChecker):
    """Checks documentation quality and completeness."""
    
    def check(self, content: str, tree: ast.AST) -> List[Dict]:
        issues = []
        self._check_docstrings(tree, issues)
        self._check_comments(content, issues)
        return issues
    
    def _check_docstrings(self, tree: ast.AST, issues: List[Dict]):
        """Check docstring presence and quality."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                self._check_node_docstring(node, issues)

    def _check_node_docstring(self, node: ast.AST, issues: List[Dict]):
        """Check individual node's docstring."""
        docstring = ast.get_docstring(node)
        node_type = node.__class__.__name__.lower()
        node_name = getattr(node, 'name', 'module')
        
        if not docstring:
            issues.append({
                "type": "IMPORTANT",
                "category": "Documentation",
                "message": f"Missing docstring in {node_type} '{node_name}'",
                "suggestion": "Add descriptive docstring"
            })
        elif len(docstring.split()) < MIN_DOCSTRING_WORDS:
            issues.append({
                "type": "STYLE",
                "category": "Documentation",
                "message": f"Brief docstring in {node_type} '{node_name}'",
                "suggestion": "Expand docstring with more details"
            })

class ValueAlignmentChecker(QualityChecker):
    """Ensures code aligns with our core values."""
    
    def check(self, content: str, tree: ast.AST) -> List[Dict]:
        issues = []
        self._check_clarity_over_cleverness(content, issues)
        self._check_simplicity(tree, issues)
        self._check_reliability_patterns(content, tree, issues)
        return issues
    
    def _check_clarity_over_cleverness(self, content: str, issues: List[Dict]):
        """Check for overly clever code."""
        clarity_indicators = ['clever', 'hack', 'trick', 'magic']
        for indicator in clarity_indicators:
            if indicator in content.lower():
                issues.append({
                    "type": "IMPORTANT",
                    "category": "Values",
                    "message": f"Possible complexity over clarity ({indicator})",
                    "suggestion": "Prefer clear, straightforward solutions"
                })

class LearningSystem:
    """Bayesian learning system for quality monitoring."""
    
    def __init__(self):
        self.history_file = Path("monitor_data/learning_history.json")
        self.history_file.parent.mkdir(exist_ok=True)
        
        # Load or initialize learning data
        self.patterns = self._load_history() or {
            "successful_patterns": defaultdict(int),
            "issue_patterns": defaultdict(int),
            "threshold_adjustments": {},
            "effectiveness": defaultdict(list)
        }
        
        print(colored("Learning System initialized", "green"))

    def learn_from_file(self, file_path: str, issues: List[Dict], stats: Dict):
        """Learn from each file analysis."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Learn from successful patterns
            if not issues:
                self._update_successful_patterns(content)
            
            # Learn from issues
            self._update_issue_patterns(issues)
            
            # Update effectiveness metrics
            self._update_effectiveness(file_path, issues, stats)
            
            # Adapt thresholds based on learning
            self._adapt_thresholds()
            
            # Save learned patterns
            self._save_history()
            
        except Exception as e:
            print(colored(f"Learning error: {str(e)}", "red"))

    def _update_successful_patterns(self, content: str):
        """Learn from code that passes all checks."""
        lines = content.split('\n')
        for i in range(len(lines) - 2):
            pattern = '\n'.join(lines[i:i+3]).strip()
            if pattern:
                self.patterns["successful_patterns"][pattern] += 1

    def _update_issue_patterns(self, issues: List[Dict]):
        """Learn from identified issues."""
        for issue in issues:
            category = f"{issue['type']}:{issue['category']}"
            self.patterns["issue_patterns"][category] += 1

    def _update_effectiveness(self, file_path: str, issues: List[Dict], stats: Dict):
        """Track effectiveness of our checks."""
        result = {
            "timestamp": datetime.now().isoformat(),
            "issues_found": len(issues),
            "stats": stats,
            "patterns_used": len(self.patterns["successful_patterns"])
        }
        self.patterns["effectiveness"][file_path].append(result)

    def _adapt_thresholds(self):
        """Adapt thresholds based on learning."""
        # Analyze patterns to suggest threshold adjustments
        if self.patterns["successful_patterns"]:
            avg_success_lines = self._analyze_pattern_lengths()
            
            # Adjust MAX_FUNCTION_LINES if needed
            current = MAX_FUNCTION_LINES
            suggested = int(avg_success_lines * 1.2)  # 20% margin
            
            if abs(current - suggested) > 5:
                self.patterns["threshold_adjustments"]["MAX_FUNCTION_LINES"] = {
                    "current": current,
                    "suggested": suggested,
                    "confidence": self._calculate_confidence()
                }

    def _analyze_pattern_lengths(self) -> float:
        """Analyze successful pattern lengths."""
        lengths = [len(p.split('\n')) for p in self.patterns["successful_patterns"]]
        return sum(lengths) / len(lengths) if lengths else 0

    def _calculate_confidence(self) -> float:
        """Calculate confidence in our learning."""
        total_files = len(self.patterns["effectiveness"])
        if not total_files:
            return 0.0
        
        success_rate = sum(
            1 for file_data in self.patterns["effectiveness"].values()
            if file_data[-1]["issues_found"] == 0
        ) / total_files
        
        return success_rate

    def _load_history(self) -> Dict:
        """Load learning history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(colored(f"Could not load history: {e}", "yellow"))
        return None

    def _save_history(self):
        """Save learning history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(colored(f"Could not save history: {e}", "red"))

class QualityMonitor:
    """Coordinates quality checks and reporting."""
    
    def __init__(self):
        """Initialize with all checkers."""
        self.checkers = [
            CodeStructureChecker(),
            DocumentationChecker(),
            ValueAlignmentChecker()
        ]
        self.learning_system = LearningSystem()
        self.issues: Dict[str, List[Dict]] = {}
        self.stats: Dict[str, Dict] = {}
        print(colored("Quality Monitor initialized", "green"))

    def check_file(self, file_path: str) -> None:
        """Run all quality checks on a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            all_issues = []
            
            # Run all checkers
            for checker in self.checkers:
                issues = checker.check(content, tree)
                all_issues.extend(issues)
            
            # Store results
            self.issues[file_path] = all_issues
            self.stats[file_path] = self._gather_statistics(content, tree)
            
            # Add learning
            self.learning_system.learn_from_file(file_path, all_issues, self.stats[file_path])
            
            # Update report with learning insights
            self._add_learning_insights(file_path)
            
        except Exception as e:
            print(colored(f"Error checking {file_path}: {str(e)}", "red"))
            self.issues[file_path] = [{"type": "ERROR", "message": str(e)}]

    def _gather_statistics(self, content: str, tree: ast.AST) -> Dict:
        """Gather code quality statistics."""
        return {
            "lines_of_code": len(content.split('\n')),
            "functions": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
            "classes": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
            "docstrings": len([n for n in ast.walk(tree) 
                             if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Module))
                             and ast.get_docstring(n)]),
            "comments": len([l for l in content.split('\n') if l.strip().startswith('#')])
        }

    def generate_report(self) -> str:
        """Generate a comprehensive quality report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = [
            "Code Quality Report",
            f"Generated at: {timestamp}",
            "=" * 50,
            ""
        ]
        
        for file_path, file_issues in self.issues.items():
            report.extend([
                f"\nFile: {os.path.basename(file_path)}",
                "-" * (len(os.path.basename(file_path)) + 6)
            ])
            
            if not file_issues:
                report.append("✓ No quality issues found")
                continue
            
            # Group by type
            by_type = {"CRITICAL": [], "IMPORTANT": [], "STYLE": []}
            for issue in file_issues:
                by_type[issue["type"]].append(issue)
            
            # Report issues by severity
            for type_, icon in [("CRITICAL", ""), ("IMPORTANT", "!"), ("STYLE", "")]:
                if by_type[type_]:
                    report.append(f"{icon} {type_} Issues:")
                    for issue in by_type[type_]:
                        report.append(f"  - {issue['message']}")
                    report.append("")
        
        return "\n".join(report)