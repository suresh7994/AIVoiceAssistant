import os
import ast
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReviewerAgent:
    """
    Code Reviewer Agent
    
    Responsible for:
    - Checking logic errors
    - Checking bad practices
    - Checking structure consistency
    - Suggesting improvements
    - Returning approved/rejected status
    
    Does NOT:
    - Directly modify files
    - Write full features
    """
    
    def __init__(self):
        self.review_categories = {
            "logic_errors": [],
            "bad_practices": [],
            "structure_issues": [],
            "improvements": []
        }
    
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """
        Review a Python file for issues and improvements
        
        Args:
            file_path: Path to the file to review
            
        Returns:
            Dictionary with review results and status
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"File not found: {file_path}"
                }
            
            # Read file content
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Initialize review results
            issues = {
                "logic_errors": [],
                "bad_practices": [],
                "structure_issues": [],
                "improvements": []
            }
            
            # Check if it's a Python file
            if file_path.endswith('.py'):
                # Parse Python AST for analysis
                try:
                    tree = ast.parse(content)
                    issues = self._analyze_python_code(tree, content, file_path)
                except SyntaxError as e:
                    issues["logic_errors"].append({
                        "type": "syntax_error",
                        "line": e.lineno,
                        "message": f"Syntax error: {e.msg}",
                        "severity": "critical"
                    })
            
            # General code quality checks
            general_issues = self._check_general_quality(content, file_path)
            for category, items in general_issues.items():
                issues[category].extend(items)
            
            # Determine status
            critical_count = sum(1 for cat in issues.values() 
                               for item in cat 
                               if item.get("severity") == "critical")
            
            total_issues = sum(len(items) for items in issues.values())
            
            if critical_count > 0:
                status = "rejected"
                message = f"Review REJECTED: {critical_count} critical issue(s) found"
            elif total_issues > 5:
                status = "needs_improvement"
                message = f"Review NEEDS IMPROVEMENT: {total_issues} issue(s) found"
            elif total_issues > 0:
                status = "approved_with_suggestions"
                message = f"Review APPROVED with {total_issues} suggestion(s)"
            else:
                status = "approved"
                message = "Review APPROVED: No issues found"
            
            return {
                "success": True,
                "file": file_path,
                "status": status,
                "message": message,
                "issues": issues,
                "summary": {
                    "total_issues": total_issues,
                    "critical": critical_count,
                    "logic_errors": len(issues["logic_errors"]),
                    "bad_practices": len(issues["bad_practices"]),
                    "structure_issues": len(issues["structure_issues"]),
                    "improvements": len(issues["improvements"])
                }
            }
            
        except Exception as e:
            logger.error(f"Review error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _analyze_python_code(self, tree: ast.AST, content: str, file_path: str) -> Dict[str, List[Dict]]:
        """Analyze Python AST for issues"""
        issues = {
            "logic_errors": [],
            "bad_practices": [],
            "structure_issues": [],
            "improvements": []
        }
        
        lines = content.split('\n')
        
        # Check for common issues
        for node in ast.walk(tree):
            # Check for bare except clauses
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues["bad_practices"].append({
                        "type": "bare_except",
                        "line": node.lineno,
                        "message": "Bare except clause - should catch specific exceptions",
                        "severity": "warning"
                    })
            
            # Check for unused variables (simple check)
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.startswith('_') and target.id != '_':
                        issues["improvements"].append({
                            "type": "unused_variable",
                            "line": node.lineno,
                            "message": f"Variable '{target.id}' appears unused (starts with _)",
                            "severity": "info"
                        })
            
            # Check for long functions
            if isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                if func_lines > 50:
                    issues["structure_issues"].append({
                        "type": "long_function",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' is {func_lines} lines long - consider breaking it down",
                        "severity": "warning"
                    })
            
            # Check for too many arguments
            if isinstance(node, ast.FunctionDef):
                arg_count = len(node.args.args)
                if arg_count > 5:
                    issues["bad_practices"].append({
                        "type": "too_many_args",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' has {arg_count} arguments - consider using a config object",
                        "severity": "warning"
                    })
            
            # Check for mutable default arguments
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        issues["logic_errors"].append({
                            "type": "mutable_default",
                            "line": node.lineno,
                            "message": f"Function '{node.name}' has mutable default argument - this can cause bugs",
                            "severity": "critical"
                        })
        
        return issues
    
    def _check_general_quality(self, content: str, file_path: str) -> Dict[str, List[Dict]]:
        """Check general code quality issues"""
        issues = {
            "logic_errors": [],
            "bad_practices": [],
            "structure_issues": [],
            "improvements": []
        }
        
        lines = content.split('\n')
        
        # Check file length
        if len(lines) > 500:
            issues["structure_issues"].append({
                "type": "long_file",
                "line": 1,
                "message": f"File is {len(lines)} lines long - consider splitting into multiple files",
                "severity": "warning"
            })
        
        # Check for TODO/FIXME comments
        for i, line in enumerate(lines, 1):
            if 'TODO' in line or 'FIXME' in line:
                issues["improvements"].append({
                    "type": "todo_comment",
                    "line": i,
                    "message": f"TODO/FIXME comment found: {line.strip()}",
                    "severity": "info"
                })
            
            # Check for print statements (should use logging)
            if 'print(' in line and not line.strip().startswith('#'):
                issues["bad_practices"].append({
                    "type": "print_statement",
                    "line": i,
                    "message": "Using print() - consider using logging instead",
                    "severity": "info"
                })
            
            # Check for very long lines
            if len(line) > 120:
                issues["structure_issues"].append({
                    "type": "long_line",
                    "line": i,
                    "message": f"Line is {len(line)} characters - exceeds 120 character limit",
                    "severity": "info"
                })
        
        # Check for missing docstrings (simple check)
        if file_path.endswith('.py'):
            if '"""' not in content[:200] and "'''" not in content[:200]:
                issues["improvements"].append({
                    "type": "missing_docstring",
                    "line": 1,
                    "message": "File appears to be missing a module docstring",
                    "severity": "info"
                })
        
        return issues
    
    def review_code_snippet(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Review a code snippet (not a full file)
        
        Args:
            code: Code snippet to review
            language: Programming language (default: python)
            
        Returns:
            Review results
        """
        try:
            issues = {
                "logic_errors": [],
                "bad_practices": [],
                "structure_issues": [],
                "improvements": []
            }
            
            if language == "python":
                try:
                    tree = ast.parse(code)
                    issues = self._analyze_python_code(tree, code, "snippet")
                except SyntaxError as e:
                    issues["logic_errors"].append({
                        "type": "syntax_error",
                        "line": e.lineno,
                        "message": f"Syntax error: {e.msg}",
                        "severity": "critical"
                    })
            
            # General checks
            general_issues = self._check_general_quality(code, f"snippet.{language}")
            for category, items in general_issues.items():
                issues[category].extend(items)
            
            total_issues = sum(len(items) for items in issues.values())
            critical_count = sum(1 for cat in issues.values() 
                               for item in cat 
                               if item.get("severity") == "critical")
            
            if critical_count > 0:
                status = "rejected"
            elif total_issues > 3:
                status = "needs_improvement"
            elif total_issues > 0:
                status = "approved_with_suggestions"
            else:
                status = "approved"
            
            return {
                "success": True,
                "status": status,
                "issues": issues,
                "summary": {
                    "total_issues": total_issues,
                    "critical": critical_count
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_review_summary(self, file_path: str) -> str:
        """Get a human-readable review summary"""
        review = self.review_file(file_path)
        
        if not review["success"]:
            return f"Review failed: {review.get('error', 'Unknown error')}"
        
        summary_lines = [
            f"\n{'='*60}",
            f"CODE REVIEW: {os.path.basename(file_path)}",
            f"{'='*60}",
            f"Status: {review['status'].upper()}",
            f"Message: {review['message']}",
            f"\nSummary:",
            f"  - Total Issues: {review['summary']['total_issues']}",
            f"  - Critical: {review['summary']['critical']}",
            f"  - Logic Errors: {review['summary']['logic_errors']}",
            f"  - Bad Practices: {review['summary']['bad_practices']}",
            f"  - Structure Issues: {review['summary']['structure_issues']}",
            f"  - Improvements: {review['summary']['improvements']}"
        ]
        
        # Add detailed issues
        for category, items in review['issues'].items():
            if items:
                summary_lines.append(f"\n{category.replace('_', ' ').title()}:")
                for issue in items[:5]:  # Show first 5 of each category
                    summary_lines.append(
                        f"  Line {issue['line']}: {issue['message']} [{issue['severity']}]"
                    )
                if len(items) > 5:
                    summary_lines.append(f"  ... and {len(items) - 5} more")
        
        summary_lines.append(f"{'='*60}\n")
        
        return '\n'.join(summary_lines)


# Tool definitions for OpenAI function calling
REVIEWER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "review_file",
            "description": "Review a code file for logic errors, bad practices, structure issues, and improvements. Returns approved/rejected status with detailed feedback.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to review"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "review_code_snippet",
            "description": "Review a code snippet for issues and best practices. Use this when user provides code directly instead of a file path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The code snippet to review"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language (default: python)"
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_review_summary",
            "description": "Get a detailed human-readable review summary for a file. Use this when user asks for a full review report.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to review"
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]
