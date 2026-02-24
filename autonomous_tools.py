"""
Autonomous Agent Tools for OpenAI Function Calling
Provides tool definitions for the autonomous software engineering capabilities
"""

AUTONOMOUS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "analyze_codebase",
            "description": "Perform comprehensive analysis of the entire codebase including structure, dependencies, architecture patterns, code quality metrics, and potential issues. Use this to understand the project before making changes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "include_metrics": {
                        "type": "boolean",
                        "description": "Include detailed code quality metrics in the analysis"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "refactor_code",
            "description": "Refactor code while preserving architecture and functionality. Supports extract_method, rename_variable, simplify_conditionals, reduce_complexity, and improve_naming.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to refactor (relative to project root)"
                    },
                    "refactor_type": {
                        "type": "string",
                        "enum": ["extract_method", "rename_variable", "simplify_conditionals", "reduce_complexity", "improve_naming"],
                        "description": "Type of refactoring to perform"
                    },
                    "old_name": {
                        "type": "string",
                        "description": "Old variable name (for rename_variable)"
                    },
                    "new_name": {
                        "type": "string",
                        "description": "New variable name (for rename_variable)"
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "Start line for code extraction (for extract_method)"
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "End line for code extraction (for extract_method)"
                    },
                    "method_name": {
                        "type": "string",
                        "description": "Name for extracted method (for extract_method)"
                    }
                },
                "required": ["file_path", "refactor_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_tests",
            "description": "Automatically generate unit tests for a specific file. Creates test templates with test cases for all functions and classes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to generate tests for"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "Run all unit tests in the project. Returns test results including pass/fail status and error details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_pattern": {
                        "type": "string",
                        "description": "Pattern to match test files (default: test_*.py)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_dependencies",
            "description": "Check project dependencies for outdated packages and security vulnerabilities. Returns list of packages that need updates.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_dependencies",
            "description": "Safely update project dependencies. In safe mode, only patch versions are updated. Creates backup before updating.",
            "parameters": {
                "type": "object",
                "properties": {
                    "safe_mode": {
                        "type": "boolean",
                        "description": "If true, only update patch versions (default: true)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_bugs",
            "description": "Detect potential bugs and code issues using static analysis. Checks for common anti-patterns, syntax errors, and code smells.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "auto_fix_bug",
            "description": "Attempt to automatically fix a detected bug. Requires bug information from detect_bugs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "bug_type": {
                        "type": "string",
                        "description": "Type of bug to fix"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "File containing the bug"
                    },
                    "line_number": {
                        "type": "integer",
                        "description": "Line number where bug occurs"
                    },
                    "bug_description": {
                        "type": "string",
                        "description": "Description of the bug"
                    }
                },
                "required": ["bug_type", "file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_documentation",
            "description": "Generate comprehensive project documentation including architecture overview, file structure, and code metrics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "output_format": {
                        "type": "string",
                        "enum": ["markdown", "html", "rst"],
                        "description": "Documentation output format (default: markdown)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_file",
            "description": "Analyze a specific file in detail including complexity, dependencies, classes, functions, and code quality metrics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to analyze"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_code_metrics",
            "description": "Get overall code quality metrics for the project including total lines, complexity, test coverage, and documentation coverage.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_improvements",
            "description": "Analyze the codebase and suggest specific improvements for code quality, performance, maintainability, and best practices.",
            "parameters": {
                "type": "object",
                "properties": {
                    "focus_area": {
                        "type": "string",
                        "enum": ["performance", "maintainability", "security", "testing", "documentation", "all"],
                        "description": "Area to focus improvement suggestions on"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_feature",
            "description": "Generate a new feature from description. Creates necessary files, implements functionality, and generates tests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "feature_name": {
                        "type": "string",
                        "description": "Name of the feature to create"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the feature functionality"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path where the feature file should be created"
                    }
                },
                "required": ["feature_name", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "optimize_performance",
            "description": "Analyze and optimize code performance. Identifies bottlenecks and suggests or implements optimizations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File to optimize (if not specified, analyzes entire project)"
                    },
                    "auto_apply": {
                        "type": "boolean",
                        "description": "Automatically apply safe optimizations"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "validate_architecture",
            "description": "Validate project architecture against best practices and design patterns. Checks for violations and suggests improvements.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_execution_history",
            "description": "Get history of all autonomous agent actions performed on the codebase for audit trail.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of recent actions to retrieve"
                    }
                },
                "required": []
            }
        }
    }
]
