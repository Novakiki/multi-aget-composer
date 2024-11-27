"""AI-powered code quality analysis."""

import os
from typing import Dict, Optional, List
from openai import AsyncOpenAI  # Use async client
from termcolor import colored
import json
import re  # Add at top

# Constants
AI_MODELS = {
    'DEFAULT': 'gpt-4',
    'FAST': 'gpt-3.5-turbo',
    'DETAILED': 'gpt-4-turbo-preview'
}

ANALYSIS_PROMPT = """Analyze this Python code and return a JSON object.

IMPORTANT: Your response must be VALID JSON with this EXACT structure:
{
    "score": <integer between 0 and 100>,
    "issues": [
        {
            "type": "STYLE",
            "category": "Documentation",
            "message": "string",
            "suggestion": "string"
        }
    ],
    "suggestions": ["string"]
}

DO NOT include any other text or formatting.

Code to analyze:
{code}
"""

class AIQualityAnalyzer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        if not os.getenv('OPENAI_API_KEY'):
            print(colored("Warning: OPENAI_API_KEY not found", "yellow"))
            self.mock_mode = True
        else:
            self.mock_mode = False
    
    async def analyze_code(self, code: str, model: str = AI_MODELS['DEFAULT']) -> Dict:
        """Analyze code quality using AI with mock fallback."""
        if self.mock_mode:
            return await self._mock_analysis(code)
        
        try:
            # Ensure we get JSON response
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "system",
                    "content": "You are a code analyzer. Respond with ONLY a JSON object."
                }, {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(code=code)
                }],
                temperature=0.0,
                response_format={"type": "json_object"},
                max_tokens=1000,
                presence_penalty=0,
                frequency_penalty=0
            )
            
            # Debug response
            content = response.choices[0].message.content
            print(colored("\nRaw response:", "yellow"))
            print(content)
            print(colored("\nResponse type:", "yellow"))
            print(type(content))
            print(colored("\nFirst few chars:", "yellow"))
            print([ord(c) for c in content[:10]])
            
            # Clean and validate
            content = content.strip()
            if not content.startswith('{'): 
                print(colored(f"Invalid start: {content[:20]}", "red"))
                raise ValueError("Response is not JSON")
            
            try:
                result = json.loads(content)
                return {
                    "score": int(result.get("score", 0)),
                    "issues": result.get("issues", []),
                    "suggestions": result.get("suggestions", [])
                }
            except json.JSONDecodeError as e:
                print(colored(f"JSON error at pos {e.pos}: {content[e.pos-10:e.pos+10]}", "red"))
                raise
            
        except Exception as e:
            print(colored(f"OpenAI request failed: {str(e)}", "red"))
            return await self._mock_analysis(code)
    
    async def _mock_analysis(self, code: str) -> Dict:
        """Enhanced mock analysis with real quality checks."""
        try:
            quality_score = 70
            issues = []
            suggestions = []
            
            # Security Checks (-25 each)
            security_patterns = {
                r'eval\s*\(': "Dangerous eval() usage",
                r'exec\s*\(': "Dangerous exec() usage",
                r'input\s*\(': "Unsafe input usage",
                r'subprocess\.': "Subprocess usage",
                r'os\.system': "System command usage",
                r'open\([^,]+\)': "File open without encoding",
                r'yaml\.load\(': "Unsafe YAML loading",
                r'pickle\.loads?\(': "Unsafe pickle usage"
            }
            
            for pattern, msg in security_patterns.items():
                if re.search(pattern, code):
                    quality_score -= 25
                    issues.append({
                        "type": "CRITICAL",
                        "category": "Security",
                        "message": msg,
                        "suggestion": "Use safer alternatives or add security controls"
                    })
                    suggestions.append("Review security practices")
            
            # Performance Issues (-15 each)
            perf_patterns = {
                r'\.append\(.*\bfor\b': "List building in loop",
                r'while True:': "Infinite loop risk",
                r'\[.*\bfor\b.*\bif\b.*\]': "Complex list comprehension",
                r'\.copy\(\).*\bfor\b': "Unnecessary copy in loop",
                r'\.keys\(\).*\bfor\b': "Inefficient keys iteration"
            }
            
            for pattern, msg in perf_patterns.items():
                if re.search(pattern, code):
                    quality_score -= 15
                    issues.append({
                        "type": "IMPORTANT",
                        "category": "Performance",
                        "message": msg,
                        "suggestion": "Use more efficient patterns"
                    })
            
            # Critical Issues (-20 each)
            if 'except:' in code or 'except Exception:' in code:
                quality_score -= 20
                issues.append({
                    "type": "CRITICAL",
                    "category": "ErrorHandling",
                    "message": "Bare except found",
                    "suggestion": "Catch specific exceptions"
                })
            
            # Variable Naming (-10 each)
            # Ignore common words and only check variable assignments
            var_pattern = re.compile(r'(?:^|\s+)([a-z_][a-z0-9_]?)\s*=\s*')
            short_vars = set(match.group(1) for match in var_pattern.finditer(code))
            if short_vars:
                quality_score -= 10
                issues.append({
                    "type": "STYLE",
                    "category": "Naming",
                    "message": f"Short variable names found: {', '.join(short_vars)}",
                    "suggestion": "Use descriptive variable names (3+ chars)"
                })
            
            # Also exclude function parameters
            def_pattern = re.compile(r'def\s+\w+\s*\((.*?)\):')
            for match in def_pattern.finditer(code):
                params = match.group(1).split(',')
                for param in params:
                    param = param.strip()
                    if len(param) > 0:
                        # Remove param from short_vars if it's there
                        short_vars.discard(param.split(':')[0].strip())
            
            # Import Checks (-10 each)
            if 'import *' in code:
                quality_score -= 10
                issues.append({
                    "type": "IMPORTANT",
                    "category": "Imports",
                    "message": "Wildcard imports found",
                    "suggestion": "Import specific names"
                })
            
            # Function Length (-15 each)
            for func in re.finditer(r'def\s+\w+[^:]*:', code):
                func_start = code.index(func.group())
                next_def = code.find('def ', func_start + 1)
                if next_def == -1:
                    next_def = len(code)
                func_code = code[func_start:next_def]
                if func_code.count('\n') > 20:
                    quality_score -= 15
                    issues.append({
                        "type": "IMPORTANT",
                        "category": "Structure",
                        "message": "Function too long",
                        "suggestion": "Break into smaller functions"
                    })
            
            # Return Values (-10 each)
            if 'return None' in code or 'return []' in code:
                quality_score -= 10
                issues.append({
                    "type": "STYLE",
                    "category": "Logic",
                    "message": "Empty returns found",
                    "suggestion": "Consider using Optional or default values"
                })
            
            # Complexity (-15 each)
            if_count = code.count('if ')
            for_count = code.count('for ')
            while_count = code.count('while ')
            
            complexity = if_count + for_count + while_count
            if complexity > 3:  # Lower threshold
                quality_score -= 15
                issues.append({
                    "type": "IMPORTANT",
                    "category": "Complexity",
                    "message": f"High complexity ({complexity} control structures)",
                    "suggestion": "Simplify logic and extract methods"
                })
                suggestions.append("Reduce code complexity")
            
            # Documentation (-10 each)
            if '"""' not in code:
                quality_score -= 10
                issues.append({
                    "type": "STYLE",
                    "category": "Documentation",
                    "message": "Missing docstrings",
                    "suggestion": "Add function and class documentation"
                })
            
            # Line Length (-10 each)
            long_lines = [i+1 for i, line in enumerate(code.split('\n')) 
                         if len(line.strip()) > 80]
            if long_lines:
                quality_score -= 10
                issues.append({
                    "type": "STYLE",
                    "category": "Formatting",
                    "message": f"Lines too long: {', '.join(map(str, long_lines))}",
                    "suggestion": "Keep lines under 80 characters"
                })
            
            # Whitespace Consistency (-5 each)
            indent_pattern = re.compile(r'^( +)[^\n\s][^\n]*$', re.MULTILINE)  # Only non-empty lines
            indents = set()
            for match in indent_pattern.finditer(code):
                spaces = len(match.group(1))
                if spaces > 0:  # Only care about actual indentation
                    indents.add(spaces)

            if len(indents) > 1 and not all(i % 4 == 0 for i in indents):
                quality_score -= 5
                issues.append({
                    "type": "STYLE",
                    "category": "Formatting",
                    "message": "Inconsistent indentation",
                    "suggestion": "Use 4 spaces consistently"
                })
            
            # Testing Patterns (-15 each)
            testing_patterns = {
                # Missing Tests
                (r'class\s+\w+.*:', lambda code: 'test' not in code.lower()): {
                    "type": "IMPORTANT",
                    "category": "Testing",
                    "message": "No tests found for class",
                    "suggestion": "Add unit tests for this class"
                },
                
                # Test Quality
                (r'assert\s+\w+\s*==', lambda code: True): {
                    "type": "STYLE",
                    "category": "Testing",
                    "message": "Simple equality assertion",
                    "suggestion": "Use more specific assertions (e.g., assertIsInstance, assertGreater)"
                },
                
                # Test Coverage
                (r'except\s+\w+.*:', lambda code: 'try:' not in code): {
                    "type": "IMPORTANT",
                    "category": "Testing",
                    "message": "Exception handling without tests",
                    "suggestion": "Add test cases for error conditions"
                }
            }
            
            for (pattern, condition), issue in testing_patterns.items():
                if re.search(pattern, code) and condition(code):
                    quality_score -= 15
                    issues.append(issue)
                    if "Testing" not in suggestions:
                        suggestions.append("Improve test coverage")
            
            # Return early only if truly excellent
            if (not issues and 
                len(suggestions) == 0 and
                '"""' in code and
                'def ' in code and
                'try:' in code and
                ':' in code and
                '->' in code):
                return {
                    "score": 95,
                    "issues": [],
                    "suggestions": ["Code looks good, consider adding tests"]
                }
            
            return {
                "score": max(min(quality_score, 100), 0),
                "issues": issues,
                "suggestions": suggestions or ["Improve code quality"]
            }
            
        except Exception as e:
            print(colored(f"Mock analysis failed: {str(e)}", "yellow"))
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