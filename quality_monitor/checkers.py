"""Quality checkers for different aspects of code."""

import ast
from typing import Dict, List
from config.quality_standards import (
    MAX_FUNCTION_LINES,
    MAX_NESTED_DEPTH,
    MIN_DOCSTRING_WORDS,
    MIN_COMMENT_RATIO
)

class StyleChecker:
    """Checks code style and formatting."""
    
    def check(self, content: str, tree: ast.AST) -> List[Dict]:
        issues = []
        
        # Check function length
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_lines = len(node.body)
                if func_lines > MAX_FUNCTION_LINES:
                    issues.append({
                        "type": "STYLE",
                        "category": "Function Length",
                        "message": f"Function '{node.name}' is too long ({func_lines} lines)",
                        "suggestion": f"Break into smaller functions (max {MAX_FUNCTION_LINES} lines)"
                    })
        
        return issues

class DocumentationChecker:
    """Checks documentation completeness."""
    
    def check(self, content: str, tree: ast.AST) -> List[Dict]:
        issues = []
        
        # Check docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                if not docstring:
                    issues.append({
                        "type": "IMPORTANT",
                        "category": "Documentation",
                        "message": f"Missing docstring in {node.__class__.__name__.lower()} '{node.name}'",
                        "suggestion": "Add descriptive docstring"
                    })
                elif len(docstring.split()) < MIN_DOCSTRING_WORDS:
                    issues.append({
                        "type": "STYLE",
                        "category": "Documentation",
                        "message": f"Brief docstring in {node.__class__.__name__.lower()} '{node.name}'",
                        "suggestion": "Expand docstring with more details"
                    })
        
        return issues 

class ComplexityChecker:
    """Checks code complexity and nesting."""
    
    def check(self, content: str, tree: ast.AST) -> List[Dict]:
        issues = []
        
        for node in ast.walk(tree):
            # Check nesting depth
            if isinstance(node, ast.FunctionDef):
                depth = self._get_nesting_depth(node)
                if depth > MAX_NESTED_DEPTH:
                    issues.append({
                        "type": "IMPORTANT",
                        "category": "Complexity",
                        "message": f"Function '{node.name}' has deep nesting (depth {depth})",
                        "suggestion": f"Reduce nesting to max {MAX_NESTED_DEPTH} levels"
                    })
                
                # Check for bare except
                for child in ast.walk(node):
                    if isinstance(child, ast.ExceptHandler) and child.type is None:
                        issues.append({
                            "type": "IMPORTANT",
                            "category": "ErrorHandling",
                            "message": "Found bare except clause",
                            "suggestion": "Catch specific exceptions instead of using bare except"
                        })
                    
                    # Check for pass in except
                    if isinstance(child, ast.ExceptHandler):
                        if any(isinstance(stmt, ast.Pass) for stmt in child.body):
                            issues.append({
                                "type": "IMPORTANT",
                                "category": "ErrorHandling",
                                "message": "Silent failure with pass in except block",
                                "suggestion": "Handle or log the error instead of passing silently"
                            })
        
        return issues
    
    def _get_nesting_depth(self, node: ast.AST) -> int:
        """Calculate deepest nesting level in a node."""
        if not hasattr(node, 'body'):
            return 0
            
        max_child_depth = 0
        for child in node.body:
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                child_depth = 1 + self._get_nesting_depth(child)
                max_child_depth = max(max_child_depth, child_depth)
                
        return max_child_depth