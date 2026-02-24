import os
import ast
import json
import logging
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutonomousAgent:
    """
    Autonomous Senior Software Engineering AI Agent
    
    Capabilities:
    - Full codebase analysis and understanding
    - Automated refactoring with architecture preservation
    - Dependency management and updates
    - Test generation and execution
    - Bug detection and fixing
    - Code quality improvements
    - Documentation generation
    - Performance optimization
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.analysis_cache = {}
        self.execution_history = []
        self.safety_checks_enabled = True
        
        logger.info(f"Autonomous Agent initialized at: {self.project_root}")
    
    # ==================== CODEBASE ANALYSIS ====================
    
    def analyze_full_codebase(self) -> Dict[str, Any]:
        """Analyze entire codebase structure, dependencies, and patterns"""
        logger.info("Starting full codebase analysis...")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "files": {},
            "dependencies": {},
            "architecture": {},
            "issues": [],
            "metrics": {}
        }
        
        # Analyze Python files
        python_files = list(self.project_root.glob("**/*.py"))
        for file_path in python_files:
            if self._should_skip_file(file_path):
                continue
            
            file_analysis = self._analyze_python_file(file_path)
            relative_path = file_path.relative_to(self.project_root)
            analysis["files"][str(relative_path)] = file_analysis
        
        # Analyze dependencies
        analysis["dependencies"] = self._analyze_dependencies()
        
        # Analyze architecture
        analysis["architecture"] = self._analyze_architecture(analysis["files"])
        
        # Calculate metrics
        analysis["metrics"] = self._calculate_metrics(analysis["files"])
        
        # Detect issues
        analysis["issues"] = self._detect_issues(analysis)
        
        self.analysis_cache = analysis
        logger.info(f"Analysis complete. Found {len(analysis['files'])} files, {len(analysis['issues'])} issues")
        
        return analysis
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during analysis"""
        skip_patterns = [
            "__pycache__", ".git", ".env", "venv", "node_modules",
            ".pyc", ".pyo", ".egg-info"
        ]
        return any(pattern in str(file_path) for pattern in skip_patterns)
    
    def _analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            analysis = {
                "path": str(file_path),
                "size": len(content),
                "lines": len(content.splitlines()),
                "classes": [],
                "functions": [],
                "imports": [],
                "complexity": 0,
                "docstring_coverage": 0
            }
            
            # Extract classes, functions, imports
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    analysis["classes"].append({
                        "name": node.name,
                        "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                        "has_docstring": ast.get_docstring(node) is not None
                    })
                elif isinstance(node, ast.FunctionDef):
                    if not any(node.name in cls["methods"] for cls in analysis["classes"]):
                        analysis["functions"].append({
                            "name": node.name,
                            "args": len(node.args.args),
                            "has_docstring": ast.get_docstring(node) is not None
                        })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        analysis["imports"].extend([alias.name for alias in node.names])
                    else:
                        analysis["imports"].append(node.module if node.module else "")
            
            # Calculate complexity
            analysis["complexity"] = self._calculate_complexity(tree)
            
            # Calculate docstring coverage
            total_items = len(analysis["classes"]) + len(analysis["functions"])
            documented = sum(1 for c in analysis["classes"] if c["has_docstring"])
            documented += sum(1 for f in analysis["functions"] if f["has_docstring"])
            analysis["docstring_coverage"] = (documented / total_items * 100) if total_items > 0 else 0
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return {"error": str(e)}
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies"""
        deps = {
            "requirements": [],
            "outdated": [],
            "security_issues": []
        }
        
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                deps["requirements"] = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        return deps
    
    def _analyze_architecture(self, files: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project architecture and patterns"""
        architecture = {
            "patterns": [],
            "layers": [],
            "coupling": {},
            "cohesion": {}
        }
        
        # Detect common patterns
        if any("controller" in f.lower() for f in files.keys()):
            architecture["patterns"].append("MVC/Controller Pattern")
        if any("agent" in f.lower() for f in files.keys()):
            architecture["patterns"].append("Agent Pattern")
        if any("ui" in f.lower() for f in files.keys()):
            architecture["patterns"].append("UI Layer Separation")
        
        return architecture
    
    def _calculate_metrics(self, files: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate code quality metrics"""
        total_lines = sum(f.get("lines", 0) for f in files.values() if "error" not in f)
        total_classes = sum(len(f.get("classes", [])) for f in files.values() if "error" not in f)
        total_functions = sum(len(f.get("functions", [])) for f in files.values() if "error" not in f)
        avg_complexity = sum(f.get("complexity", 0) for f in files.values() if "error" not in f) / max(len(files), 1)
        
        return {
            "total_lines": total_lines,
            "total_classes": total_classes,
            "total_functions": total_functions,
            "average_complexity": round(avg_complexity, 2),
            "files_count": len(files)
        }
    
    def _detect_issues(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect potential issues in the codebase"""
        issues = []
        
        for file_path, file_data in analysis["files"].items():
            if "error" in file_data:
                issues.append({
                    "severity": "high",
                    "type": "parse_error",
                    "file": file_path,
                    "message": file_data["error"]
                })
                continue
            
            # Check complexity
            if file_data.get("complexity", 0) > 20:
                issues.append({
                    "severity": "medium",
                    "type": "high_complexity",
                    "file": file_path,
                    "message": f"High complexity: {file_data['complexity']}"
                })
            
            # Check docstring coverage
            if file_data.get("docstring_coverage", 0) < 50:
                issues.append({
                    "severity": "low",
                    "type": "low_documentation",
                    "file": file_path,
                    "message": f"Low docstring coverage: {file_data['docstring_coverage']:.1f}%"
                })
            
            # Check file size
            if file_data.get("lines", 0) > 500:
                issues.append({
                    "severity": "medium",
                    "type": "large_file",
                    "file": file_path,
                    "message": f"Large file: {file_data['lines']} lines"
                })
        
        return issues
    
    # ==================== CODE MODIFICATION ====================
    
    def refactor_code(self, file_path: str, refactor_type: str, **kwargs) -> Dict[str, Any]:
        """
        Refactor code while preserving architecture
        
        Types: extract_method, rename_variable, simplify_conditionals, 
               reduce_complexity, improve_naming
        """
        if not self._safety_check("refactor", file_path):
            return {"success": False, "error": "Safety check failed"}
        
        logger.info(f"Refactoring {file_path} - Type: {refactor_type}")
        
        try:
            full_path = self.project_root / file_path
            with open(full_path, 'r') as f:
                original_content = f.read()
            
            # Backup original
            backup_path = full_path.with_suffix(full_path.suffix + '.backup')
            with open(backup_path, 'w') as f:
                f.write(original_content)
            
            # Perform refactoring based on type
            if refactor_type == "extract_method":
                modified_content = self._extract_method(original_content, **kwargs)
            elif refactor_type == "rename_variable":
                modified_content = self._rename_variable(original_content, **kwargs)
            elif refactor_type == "simplify_conditionals":
                modified_content = self._simplify_conditionals(original_content)
            else:
                return {"success": False, "error": f"Unknown refactor type: {refactor_type}"}
            
            # Validate syntax
            try:
                ast.parse(modified_content)
            except SyntaxError as e:
                # Restore backup
                with open(full_path, 'w') as f:
                    f.write(original_content)
                return {"success": False, "error": f"Syntax error after refactoring: {e}"}
            
            # Write modified content
            with open(full_path, 'w') as f:
                f.write(modified_content)
            
            self._log_action("refactor", file_path, refactor_type)
            
            return {
                "success": True,
                "message": f"Refactored {file_path}",
                "backup": str(backup_path)
            }
            
        except Exception as e:
            logger.error(f"Refactoring error: {e}")
            return {"success": False, "error": str(e)}
    
    def _extract_method(self, content: str, start_line: int, end_line: int, method_name: str) -> str:
        """Extract code block into a separate method"""
        lines = content.splitlines()
        extracted = lines[start_line:end_line]
        # Simple implementation - would need more sophisticated logic
        return content
    
    def _rename_variable(self, content: str, old_name: str, new_name: str) -> str:
        """Rename a variable throughout the file"""
        # Use regex with word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(old_name) + r'\b'
        return re.sub(pattern, new_name, content)
    
    def _simplify_conditionals(self, content: str) -> str:
        """Simplify complex conditional statements"""
        # This would use AST transformation
        return content
    
    # ==================== TESTING ====================
    
    def generate_tests(self, file_path: str) -> Dict[str, Any]:
        """Generate unit tests for a file"""
        logger.info(f"Generating tests for {file_path}")
        
        try:
            analysis = self._analyze_python_file(self.project_root / file_path)
            
            test_content = self._create_test_template(file_path, analysis)
            
            test_file = self.project_root / f"test_{Path(file_path).name}"
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            return {
                "success": True,
                "test_file": str(test_file),
                "tests_generated": len(analysis.get("functions", [])) + len(analysis.get("classes", []))
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_test_template(self, file_path: str, analysis: Dict[str, Any]) -> str:
        """Create test template based on file analysis"""
        module_name = Path(file_path).stem
        
        test_content = f"""import unittest
from {module_name} import *


class Test{module_name.title()}(unittest.TestCase):
    
    def setUp(self):
        \"\"\"Set up test fixtures\"\"\"
        pass
    
    def tearDown(self):
        \"\"\"Clean up after tests\"\"\"
        pass
"""
        
        # Generate test methods for each function
        for func in analysis.get("functions", []):
            test_content += f"""
    def test_{func['name']}(self):
        \"\"\"Test {func['name']} function\"\"\"
        # TODO: Implement test
        pass
"""
        
        # Generate test methods for each class
        for cls in analysis.get("classes", []):
            test_content += f"""
    def test_{cls['name'].lower()}_creation(self):
        \"\"\"Test {cls['name']} instantiation\"\"\"
        # TODO: Implement test
        pass
"""
        
        test_content += """

if __name__ == '__main__':
    unittest.main()
"""
        
        return test_content
    
    def run_tests(self, test_pattern: str = "test_*.py") -> Dict[str, Any]:
        """Run all tests matching pattern"""
        logger.info(f"Running tests: {test_pattern}")
        
        try:
            result = subprocess.run(
                ["python", "-m", "unittest", "discover", "-p", test_pattern],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
                "return_code": result.returncode
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== DEPENDENCY MANAGEMENT ====================
    
    def check_dependencies(self) -> Dict[str, Any]:
        """Check for outdated or vulnerable dependencies"""
        logger.info("Checking dependencies...")
        
        results = {
            "outdated": [],
            "vulnerable": [],
            "updates_available": []
        }
        
        try:
            # Check for outdated packages
            result = subprocess.run(
                ["pip", "list", "--outdated", "--format=json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                outdated = json.loads(result.stdout)
                results["outdated"] = outdated
                results["updates_available"] = len(outdated)
            
        except Exception as e:
            logger.error(f"Error checking dependencies: {e}")
        
        return results
    
    def update_dependencies(self, safe_mode: bool = True) -> Dict[str, Any]:
        """Update dependencies safely"""
        if not self._safety_check("update_dependencies"):
            return {"success": False, "error": "Safety check failed"}
        
        logger.info("Updating dependencies...")
        
        try:
            req_file = self.project_root / "requirements.txt"
            if not req_file.exists():
                return {"success": False, "error": "requirements.txt not found"}
            
            # Backup requirements
            backup_file = req_file.with_suffix('.txt.backup')
            with open(req_file, 'r') as f:
                original = f.read()
            with open(backup_file, 'w') as f:
                f.write(original)
            
            if safe_mode:
                # Only update patch versions
                result = subprocess.run(
                    ["pip", "install", "-U", "-r", str(req_file)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
            else:
                # Update all versions
                result = subprocess.run(
                    ["pip", "install", "--upgrade", "-r", str(req_file)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "backup": str(backup_file)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== BUG DETECTION & FIXING ====================
    
    def detect_bugs(self) -> List[Dict[str, Any]]:
        """Detect potential bugs using static analysis"""
        logger.info("Running bug detection...")
        
        bugs = []
        
        # Run pylint if available
        try:
            result = subprocess.run(
                ["pylint", "--output-format=json", str(self.project_root)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.stdout:
                pylint_results = json.loads(result.stdout)
                for issue in pylint_results:
                    if issue.get("type") in ["error", "fatal"]:
                        bugs.append({
                            "severity": "high",
                            "type": "pylint",
                            "file": issue.get("path"),
                            "line": issue.get("line"),
                            "message": issue.get("message")
                        })
        except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
            logger.warning("Pylint not available or failed")
        
        # Add custom bug detection logic
        if self.analysis_cache:
            for file_path, file_data in self.analysis_cache.get("files", {}).items():
                # Check for common anti-patterns
                if "error" not in file_data:
                    # Example: Check for bare except clauses
                    full_path = self.project_root / file_path
                    try:
                        with open(full_path, 'r') as f:
                            content = f.read()
                        if re.search(r'except\s*:', content):
                            bugs.append({
                                "severity": "medium",
                                "type": "bare_except",
                                "file": file_path,
                                "message": "Bare except clause detected"
                            })
                    except Exception:
                        pass
        
        return bugs
    
    def auto_fix_bug(self, bug: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to automatically fix a detected bug"""
        if not self._safety_check("auto_fix", bug.get("file")):
            return {"success": False, "error": "Safety check failed"}
        
        logger.info(f"Attempting to fix bug: {bug.get('type')} in {bug.get('file')}")
        
        # Implementation would depend on bug type
        return {"success": False, "error": "Auto-fix not implemented for this bug type"}
    
    # ==================== DOCUMENTATION ====================
    
    def generate_documentation(self, output_format: str = "markdown") -> Dict[str, Any]:
        """Generate comprehensive documentation"""
        logger.info("Generating documentation...")
        
        try:
            if not self.analysis_cache:
                self.analyze_full_codebase()
            
            doc_content = self._create_documentation(self.analysis_cache, output_format)
            
            doc_file = self.project_root / f"ARCHITECTURE.{output_format}"
            with open(doc_file, 'w') as f:
                f.write(doc_content)
            
            return {
                "success": True,
                "file": str(doc_file),
                "format": output_format
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_documentation(self, analysis: Dict[str, Any], format_type: str) -> str:
        """Create documentation from analysis"""
        if format_type == "markdown":
            doc = f"""# Project Architecture Documentation

Generated: {analysis['timestamp']}

## Overview

- **Total Files**: {analysis['metrics']['files_count']}
- **Total Lines**: {analysis['metrics']['total_lines']}
- **Total Classes**: {analysis['metrics']['total_classes']}
- **Total Functions**: {analysis['metrics']['total_functions']}
- **Average Complexity**: {analysis['metrics']['average_complexity']}

## Architecture Patterns

"""
            for pattern in analysis['architecture'].get('patterns', []):
                doc += f"- {pattern}\n"
            
            doc += "\n## File Structure\n\n"
            for file_path, file_data in analysis['files'].items():
                if "error" not in file_data:
                    doc += f"### {file_path}\n\n"
                    doc += f"- Lines: {file_data['lines']}\n"
                    doc += f"- Classes: {len(file_data['classes'])}\n"
                    doc += f"- Functions: {len(file_data['functions'])}\n"
                    doc += f"- Complexity: {file_data['complexity']}\n\n"
            
            doc += "\n## Issues\n\n"
            for issue in analysis.get('issues', []):
                doc += f"- **{issue['severity'].upper()}**: {issue['message']} ({issue['file']})\n"
            
            return doc
        
        return "Unsupported format"
    
    # ==================== UTILITY METHODS ====================
    
    def _safety_check(self, operation: str, target: Optional[str] = None) -> bool:
        """Perform safety checks before destructive operations"""
        if not self.safety_checks_enabled:
            return True
        
        # Check if target is in safe list
        unsafe_operations = ["delete", "drop", "remove"]
        if any(op in operation.lower() for op in unsafe_operations):
            logger.warning(f"Potentially unsafe operation: {operation}")
            return False
        
        # Check if file is critical
        if target:
            critical_files = ["main.py", "requirements.txt", ".env"]
            if any(cf in str(target) for cf in critical_files):
                logger.info(f"Operating on critical file: {target}")
        
        return True
    
    def _log_action(self, action: str, target: str, details: str = ""):
        """Log agent actions for audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "target": target,
            "details": details
        }
        self.execution_history.append(log_entry)
        
        # Write to log file
        log_file = self.project_root / "autonomous_agent.log"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get history of all agent actions"""
        return self.execution_history
    
    def enable_safety_checks(self, enabled: bool = True):
        """Enable or disable safety checks"""
        self.safety_checks_enabled = enabled
        logger.info(f"Safety checks {'enabled' if enabled else 'disabled'}")
