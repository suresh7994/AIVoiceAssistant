# Code Reviewer Agent

Surya now includes an intelligent **Code Reviewer Agent** that can review your code for issues and suggest improvements - all through voice commands!

## What the Reviewer Agent Does

### ✅ Responsibilities

1. **Check Logic Errors**
   - Syntax errors
   - Mutable default arguments
   - Potential bugs and edge cases

2. **Check Bad Practices**
   - Bare except clauses
   - Too many function arguments
   - Print statements instead of logging
   - Anti-patterns

3. **Check Structure Consistency**
   - Long functions (>50 lines)
   - Long files (>500 lines)
   - Long lines (>120 characters)
   - Code organization

4. **Suggest Improvements**
   - Missing docstrings
   - TODO/FIXME comments
   - Unused variables
   - Best practices

5. **Return Status**
   - **Approved**: No issues found
   - **Approved with Suggestions**: Minor improvements suggested
   - **Needs Improvement**: Multiple issues found
   - **Rejected**: Critical issues found

### ❌ What It Does NOT Do

- **Does NOT directly modify files**
- **Does NOT write full features**
- **Does NOT auto-fix issues**
- Only provides feedback and recommendations

## Voice Commands

### Review a File

**English:**
- "Review the file main.py"
- "Check agent_brain.py for issues"
- "Analyze the code in windsurf_controller.py"
- "Is there anything wrong with my code?"

**Hindi:**
- "main.py फाइल रिव्यू करो"
- "कोड चेक करो"
- "agent_brain.py में कोई गलती है क्या?"

### Review Code Snippet

**English:**
- "Review this code: [paste code]"
- "Check this function for issues"
- "Is this code correct?"

### Get Detailed Summary

**English:**
- "Give me a full review of main.py"
- "Show me all issues in agent_brain.py"
- "Detailed review of the code"

## Example Usage

### Example 1: Review a File

```
You: "Hello Surya"
Surya: "Yes, I'm listening"

You: "Review the file main.py"
Surya: "Review completed. Status: Approved with suggestions. 
       Found 3 improvements: 
       - Line 45: Consider using logging instead of print
       - Line 120: Function is 65 lines long, consider breaking it down
       - Line 200: Missing docstring"
```

### Example 2: Check for Errors

```
You: "Check agent_brain.py for any errors"
Surya: "Review completed. Status: Approved. No critical issues found. 
       The code looks good!"
```

### Example 3: Detailed Review

```
You: "Give me a detailed review of windsurf_controller.py"
Surya: "Review completed. Status: Needs improvement.
       
       Summary:
       - Total Issues: 8
       - Critical: 0
       - Logic Errors: 0
       - Bad Practices: 3
       - Structure Issues: 2
       - Improvements: 3
       
       Bad Practices:
       - Line 45: Bare except clause - should catch specific exceptions
       - Line 120: Function has 7 arguments - consider using a config object
       
       Structure Issues:
       - Line 200: Function is 75 lines long - consider breaking it down
       
       Improvements:
       - Line 10: TODO comment found
       - Line 50: Missing docstring"
```

### Example 4: Review Code Snippet

```
You: "Review this code: def calculate(a, b, c, d, e, f, g): return a + b"
Surya: "Review completed. Status: Needs improvement.
       Found 1 bad practice:
       - Function has 7 arguments but only uses 2 - consider removing unused parameters"
```

## Review Categories

### 1. Logic Errors (Critical)

**What it checks:**
- Syntax errors
- Mutable default arguments (lists, dicts as defaults)
- Type mismatches
- Potential runtime errors

**Severity:** Critical - Must fix

**Example:**
```python
# BAD - Mutable default argument
def add_item(item, items=[]):  # ❌ Critical issue
    items.append(item)
    return items

# GOOD
def add_item(item, items=None):  # ✅ Approved
    if items is None:
        items = []
    items.append(item)
    return items
```

### 2. Bad Practices (Warning)

**What it checks:**
- Bare except clauses
- Too many function arguments (>5)
- Print statements (should use logging)
- Global variables
- Magic numbers

**Severity:** Warning - Should fix

**Example:**
```python
# BAD - Bare except
try:
    risky_operation()
except:  # ❌ Bad practice
    pass

# GOOD
try:
    risky_operation()
except ValueError as e:  # ✅ Approved
    logger.error(f"Error: {e}")
```

### 3. Structure Issues (Warning)

**What it checks:**
- Long functions (>50 lines)
- Long files (>500 lines)
- Long lines (>120 characters)
- Deep nesting
- Complex functions

**Severity:** Warning - Consider refactoring

**Example:**
```python
# BAD - Long function
def process_data(data):  # ❌ 75 lines - too long
    # ... 75 lines of code ...
    pass

# GOOD - Break into smaller functions
def validate_data(data):  # ✅ 15 lines
    pass

def transform_data(data):  # ✅ 20 lines
    pass

def process_data(data):  # ✅ 10 lines
    validate_data(data)
    return transform_data(data)
```

### 4. Improvements (Info)

**What it checks:**
- Missing docstrings
- TODO/FIXME comments
- Unused variables
- Code style inconsistencies

**Severity:** Info - Nice to have

**Example:**
```python
# NEEDS IMPROVEMENT - Missing docstring
def calculate_total(items):  # ℹ️ Missing docstring
    return sum(items)

# BETTER
def calculate_total(items):  # ✅ Has docstring
    """Calculate the total sum of items.
    
    Args:
        items: List of numbers to sum
        
    Returns:
        Total sum of all items
    """
    return sum(items)
```

## Review Status Meanings

### ✅ Approved
- **No issues found**
- Code is clean and follows best practices
- Ready to use

### ✅ Approved with Suggestions
- **Minor improvements suggested**
- Code works but could be better
- 1-5 non-critical issues
- Safe to use, improvements optional

### ⚠️ Needs Improvement
- **Multiple issues found**
- More than 5 issues detected
- Should address before production
- Code may work but needs cleanup

### ❌ Rejected
- **Critical issues found**
- Syntax errors or serious bugs
- Must fix before using
- Code may not work correctly

## How It Works

### Analysis Process

1. **Parse Code**: Reads and parses the file
2. **AST Analysis**: Uses Python AST for deep analysis
3. **Pattern Matching**: Checks for common anti-patterns
4. **Quality Checks**: Analyzes code quality metrics
5. **Categorize Issues**: Groups issues by severity
6. **Generate Report**: Creates detailed feedback
7. **Determine Status**: Approves or rejects based on findings

### Technologies Used

- **Python AST**: Abstract Syntax Tree parsing
- **Static Analysis**: Code analysis without execution
- **Pattern Recognition**: Identifies common issues
- **Best Practices Database**: Checks against standards

## Supported Languages

Currently supports:
- **Python** (full analysis)
- Other languages (basic checks)

Future support planned for:
- JavaScript/TypeScript
- Java
- C/C++
- Go

## Integration with Workflow

### Before Committing Code

```
You: "Review all my Python files"
Surya: "Reviewing 5 files... 
       - main.py: Approved
       - agent_brain.py: Approved with suggestions
       - windsurf_controller.py: Needs improvement
       - teams_controller.py: Approved
       - reviewer_agent.py: Approved"
```

### During Development

```
You: "Check my latest changes in main.py"
Surya: "Review completed. Found 1 issue:
       Line 150: Function is 60 lines long - consider breaking it down"
```

### Code Review Sessions

```
You: "Give me a detailed review of the entire project"
Surya: "Reviewing all files...
       Total: 10 files reviewed
       Approved: 6
       Approved with suggestions: 3
       Needs improvement: 1
       Rejected: 0"
```

## Best Practices

### When to Use Review

1. **Before committing** - Catch issues early
2. **After major changes** - Ensure quality
3. **Before pull requests** - Clean code review
4. **Learning** - Understand best practices
5. **Refactoring** - Validate improvements

### How to Act on Feedback

1. **Critical Issues**: Fix immediately
2. **Warnings**: Address before production
3. **Improvements**: Consider for next iteration
4. **Info**: Nice to have, not urgent

### Combine with Other Tools

```
You: "Find the file main.py"
Surya: "Found: /Users/username/project/main.py"

You: "Review that file"
Surya: "Review completed. Status: Approved with suggestions..."

You: "Open it in VS Code"
Surya: "Opened main.py in VS Code"
```

## Limitations

### Current Limitations

- **Python focus**: Best analysis for Python files
- **Static only**: Doesn't execute code
- **Pattern-based**: May miss complex logic errors
- **No auto-fix**: Only provides feedback
- **File-based**: Reviews one file at a time

### Not a Replacement For

- **Unit tests**: Still need comprehensive tests
- **Manual review**: Human review is valuable
- **Linters**: Use alongside pylint, flake8, etc.
- **Type checkers**: Use mypy for type checking

## Technical Details

### ReviewerAgent Methods

1. **`review_file(file_path)`**
   - Reviews a complete file
   - Returns detailed issue report
   - Includes status and summary

2. **`review_code_snippet(code, language)`**
   - Reviews code snippet
   - Useful for quick checks
   - Supports multiple languages

3. **`get_review_summary(file_path)`**
   - Generates human-readable summary
   - Formatted for voice output
   - Includes all issue categories

### Issue Structure

```python
{
    "type": "bare_except",
    "line": 45,
    "message": "Bare except clause - should catch specific exceptions",
    "severity": "warning"  # critical, warning, info
}
```

### Review Result Structure

```python
{
    "success": True,
    "file": "main.py",
    "status": "approved_with_suggestions",
    "message": "Review APPROVED with 3 suggestion(s)",
    "issues": {
        "logic_errors": [],
        "bad_practices": [...],
        "structure_issues": [...],
        "improvements": [...]
    },
    "summary": {
        "total_issues": 3,
        "critical": 0,
        "logic_errors": 0,
        "bad_practices": 1,
        "structure_issues": 1,
        "improvements": 1
    }
}
```

## Future Enhancements

Planned features:
- Multi-file project review
- Custom rule configuration
- Integration with git diff
- Security vulnerability scanning
- Performance analysis
- Code complexity metrics
- Auto-fix suggestions
- Learning from feedback

## Tips

1. **Review regularly**: Catch issues early
2. **Fix critical first**: Prioritize by severity
3. **Learn from feedback**: Understand why issues matter
4. **Combine tools**: Use with linters and tests
5. **Iterate**: Review, fix, review again

## Example Workflow

```
# 1. Find file
You: "Find the file agent_brain"
Surya: "Found: agent_brain.py"

# 2. Review it
You: "Review that file"
Surya: "Status: Needs improvement. Found 5 issues..."

# 3. Get details
You: "Give me the full review"
Surya: "Detailed review: [lists all issues]"

# 4. Open in IDE
You: "Open it in VS Code"
Surya: "Opened in VS Code"

# 5. After fixing
You: "Review it again"
Surya: "Status: Approved! All issues resolved."
```

The Reviewer Agent helps you maintain high code quality through intelligent, automated code review - all accessible via voice commands!
