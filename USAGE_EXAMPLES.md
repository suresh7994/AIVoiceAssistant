# Usage Examples - Autonomous AI Voice Assistant

## Quick Start Examples

### Basic Interaction

```
User: "Hello Surya"
Surya: "Yes, I'm listening"

User: "What can you do?"
Surya: "I'm an autonomous software engineering AI assistant. I can analyze codebases, 
       refactor code, generate tests, manage dependencies, review code, control your IDE, 
       schedule Teams meetings, and much more. What would you like help with?"
```

## Autonomous Software Engineering Examples

### 1. Complete Codebase Analysis

```
User: "Analyze the entire codebase"
Surya: "Analyzing the codebase... Found 11 Python files with 3,200 total lines of code. 
       The project follows MVC and Agent patterns. I detected 15 classes and 87 functions. 
       Average complexity is 11.5. I found 5 issues: 2 medium priority and 3 low priority. 
       Would you like details on the issues?"

User: "Yes, tell me about the issues"
Surya: "The medium priority issues are: high complexity in main.py with a score of 25, 
       and a large file in windsurf_controller.py with 657 lines. The low priority issues 
       are low documentation coverage in three files. Should I help fix these?"
```

### 2. Code Refactoring

```
User: "Refactor main.py to reduce complexity"
Surya: "I'll refactor main.py to reduce complexity. Creating a backup first... 
       I've simplified the conditional logic in the on_speech_recognized method and 
       extracted the wake word handling into a separate method. Complexity reduced 
       from 25 to 18. The backup is saved as main.py.backup. Would you like me to 
       run tests to verify everything still works?"

User: "Yes, run the tests"
Surya: "Running tests... All tests passed successfully. The refactoring is safe."
```

### 3. Test Generation and Execution

```
User: "Generate tests for the autonomous agent"
Surya: "Generating comprehensive test suite for autonomous_agent.py... Created 
       test_autonomous_agent.py with 18 test cases covering all major functions. 
       Tests include analysis, refactoring, bug detection, and dependency management."

User: "Run all tests"
Surya: "Executing test suite... 18 tests run, 16 passed, 2 skipped. Test coverage 
       is at 82%. All critical functionality is working correctly."
```

### 4. Dependency Management

```
User: "Check if my dependencies are up to date"
Surya: "Checking dependencies... Found 3 outdated packages: openai version 1.50.0 
       can be updated to 1.55.2, requests 2.31.0 to 2.32.1, and PyQt5 5.15.10 to 
       5.15.11. Would you like me to update them safely?"

User: "Update them safely"
Surya: "Updating dependencies in safe mode... Creating backup of requirements.txt... 
       Successfully updated all 3 packages. Backup saved to requirements.txt.backup. 
       All packages are now up to date."
```

### 5. Bug Detection and Fixing

```
User: "Find bugs in the code"
Surya: "Running static analysis and bug detection... Found 4 potential issues:
       1. Bare except clause in speech_to_text.py line 61 (medium severity)
       2. Possible resource leak in text_to_speech.py line 75 (medium severity)
       3. Unused import in agent_brain.py line 4 (low severity)
       4. Variable shadowing in ui.py line 156 (low severity)
       Would you like me to fix these automatically?"

User: "Fix the medium severity issues"
Surya: "Fixing medium severity bugs... Updated speech_to_text.py to use specific 
       exception handling. Added proper resource cleanup in text_to_speech.py. 
       Both fixes have been applied and tested. The code is now safer."
```

### 6. Documentation Generation

```
User: "Generate project documentation"
Surya: "Generating comprehensive documentation... Created ARCHITECTURE.md with 
       complete project overview, file structure, architecture patterns, code metrics, 
       and identified issues. The documentation is ready for review."
```

### 7. Performance Optimization

```
User: "Suggest performance improvements"
Surya: "Analyzing performance... I found 3 optimization opportunities:
       1. Add caching for repeated file operations in windsurf_controller.py
       2. Use async operations for API calls in agent_brain.py
       3. Optimize the waveform rendering in ui.py to reduce CPU usage
       Would you like me to implement these optimizations?"
```

### 8. Architecture Validation

```
User: "Validate the project architecture"
Surya: "Validating architecture against best practices... The project follows 
       standard MVC and Agent patterns. Separation of concerns is well maintained. 
       I recommend adding a service layer for external API calls and implementing 
       dependency injection for better testability. Overall architecture score: 8/10."
```

## IDE Control Examples

### Opening IDEs and Files

```
User: "Open Windsurf IDE"
Surya: "Launching Windsurf IDE... Windsurf is now open."

User: "Open main.py in VS Code"
Surya: "Opening main.py in Visual Studio Code... File opened successfully."
```

### File Operations

```
User: "Create a new file called utils.py"
Surya: "Creating utils.py... File created successfully."

User: "Find the file agent_brain"
Surya: "Searching for agent_brain... Found agent_brain.py in the project root."
```

## Microsoft Teams Examples

### Scheduling Meetings

```
User: "Schedule a Teams meeting tomorrow at 2 PM"
Surya: "Scheduling Teams meeting for tomorrow at 2 PM... What should be the 
       meeting subject?"

User: "Project review meeting"
Surya: "Creating meeting 'Project review meeting' for tomorrow at 2 PM... 
       Meeting scheduled successfully. The join link has been sent to attendees."
```

### Chat Management

```
User: "What are my recent Teams chats?"
Surya: "Retrieving recent chats... You have 5 recent individual chats. The most 
       recent is from John Smith about the project deadline."

User: "Reply to the latest chat saying I'll have it ready by Friday"
Surya: "Sending message to John Smith... Message sent: 'I'll have it ready by Friday.'"
```

## Code Review Examples

```
User: "Review main.py for issues"
Surya: "Reviewing main.py... Analysis complete. Found 3 areas for improvement:
       1. The VoiceAgent class has high complexity - consider extracting methods
       2. Missing error handling in the toggle_listening method
       3. The wake word detection could be more robust
       Overall assessment: Needs improvement. The code is functional but could 
       benefit from refactoring for better maintainability."
```

## File Navigation Examples

```
User: "Where am I?"
Surya: "You're currently in /Users/sureshprajapat/Suresh/git/AIVoiceAssistant"

User: "What files are in this directory?"
Surya: "The current directory contains 11 Python files, 7 markdown documentation 
       files, and 1 requirements.txt file. Key files include main.py, agent_brain.py, 
       and autonomous_agent.py."

User: "Go to the tests folder"
Surya: "I don't see a tests folder in the current directory. Would you like me to 
       create one?"
```

## Complex Workflow Examples

### Complete Development Workflow

```
User: "Hello Surya"
Surya: "Yes, I'm listening"

User: "I want to improve the code quality of this project"
Surya: "I'll help you improve code quality. Let me start by analyzing the codebase."
       [Analyzes codebase]
       "Analysis complete. I found several areas for improvement. Here's my plan:
       1. Refactor high-complexity methods
       2. Add missing tests
       3. Update outdated dependencies
       4. Fix detected bugs
       5. Improve documentation
       Should I proceed with this plan?"

User: "Yes, proceed"
Surya: "Starting code quality improvements...
       Step 1: Refactoring main.py... Done. Complexity reduced from 25 to 18.
       Step 2: Generating tests... Created test files for 5 modules.
       Step 3: Updating dependencies... 3 packages updated safely.
       Step 4: Fixed 2 medium-severity bugs.
       Step 5: Generated comprehensive documentation.
       
       All improvements complete! Code quality score improved from 7.2 to 8.9 out of 10.
       Would you like me to run the full test suite to verify everything works?"

User: "Yes, run all tests"
Surya: "Running complete test suite... 45 tests executed, 43 passed, 2 skipped.
       Test coverage: 85%. All critical functionality verified. The improvements
       are stable and ready for production."
```

### Debugging Workflow

```
User: "The application is crashing when I try to schedule a meeting"
Surya: "Let me investigate the issue. Analyzing error logs and code..."
       [Performs analysis]
       "Found the issue: Missing Teams authentication credentials. The error occurs
       in teams_controller.py when trying to authenticate. You need to set the
       TEAMS_CLIENT_ID, TEAMS_CLIENT_SECRET, and TEAMS_TENANT_ID environment
       variables. Would you like me to guide you through setting these up?"

User: "I don't have Teams credentials. Can I use the app without Teams?"
Surya: "Yes, absolutely. Teams integration is optional. The app will work perfectly
       for all other features including IDE control, code review, autonomous
       engineering, and file navigation. The Teams features will simply be unavailable
       until you configure the credentials."
```

### Feature Development Workflow

```
User: "I want to add a new feature to export analysis results to JSON"
Surya: "Great idea! I'll help you implement that. Here's what I'll do:
       1. Create a new method in autonomous_agent.py for JSON export
       2. Add a tool definition for voice command access
       3. Generate tests for the new feature
       4. Update documentation
       Should I proceed?"

User: "Yes, create it"
Surya: "Creating the export feature...
       - Added export_analysis_to_json method to autonomous_agent.py
       - Created tool definition in autonomous_tools.py
       - Generated test cases in test_autonomous_agent.py
       - Updated AUTONOMOUS_AGENT_GUIDE.md with usage examples
       
       The feature is ready! You can now say 'Export analysis to JSON' to save
       the codebase analysis results. Would you like me to test it?"
```

## Error Recovery Examples

### Automatic Error Recovery

```
User: "Import the pandas library"
Surya: "Attempting to import pandas... Error: pandas module not found. 
       Automatically installing pandas... Installation successful. 
       Pandas is now available for use."
```

### Manual Intervention Required

```
User: "Delete all Python files"
Surya: "I cannot perform this operation. Deleting all Python files would destroy
       the project. This is a safety-protected operation. If you really need to
       delete files, please do so manually with caution."
```

### System Health Monitoring

```
[Automatic background monitoring]
Surya: "Health alert: Disk space is running low at 8% free. Consider cleaning up
       unnecessary files or moving the project to a drive with more space."
```

## Advanced Examples

### Multi-Step Analysis and Improvement

```
User: "Analyze the codebase and make it production-ready"
Surya: "I'll perform a comprehensive production-readiness analysis and improvements.
       
       Phase 1: Analysis
       - Code quality: 7.5/10
       - Test coverage: 65%
       - Documentation: 70%
       - Security: No critical issues
       - Performance: Good
       
       Phase 2: Improvements Needed
       - Add error handling in 3 critical paths
       - Increase test coverage to 85%
       - Add logging throughout
       - Implement rate limiting for API calls
       - Add input validation
       
       Phase 3: Implementing improvements...
       [Performs all improvements]
       
       Production readiness assessment: 9.2/10
       The application is now production-ready with comprehensive error handling,
       high test coverage, and proper logging. Deployment recommended."
```

### Continuous Monitoring

```
User: "Monitor the codebase and alert me of any issues"
Surya: "Continuous monitoring activated. I'll check for:
       - New bugs introduced
       - Dependency vulnerabilities
       - Performance degradation
       - Test failures
       - Code quality regression
       
       I'll alert you if any issues are detected."

[Later, automatically]
Surya: "Alert: A new dependency vulnerability was detected in the requests package.
       CVE-2024-XXXX affects versions below 2.32.3. Current version: 2.31.0.
       Recommended action: Update to 2.32.3 or higher. Should I update it now?"
```

## Tips for Best Results

1. **Be Specific**: "Refactor the login method in main.py" works better than "improve the code"

2. **Ask for Explanations**: "Why did you suggest this change?" to understand the reasoning

3. **Verify Changes**: Always ask to run tests after refactoring

4. **Use Checkpoints**: For major changes, ask to create checkpoints for easy rollback

5. **Review Suggestions**: Ask "What would you improve?" before making changes

6. **Combine Commands**: "Analyze the code, fix bugs, and run tests" for efficient workflows

7. **Check History**: "Show me what changes you've made" to track all modifications

## Common Patterns

### Before Making Changes
```
"Analyze the codebase" → "Create a checkpoint" → "Make changes" → "Run tests"
```

### Regular Maintenance
```
"Check dependencies" → "Update safely" → "Run tests" → "Generate documentation"
```

### Bug Fixing
```
"Find bugs" → "Review the issues" → "Fix high priority bugs" → "Verify with tests"
```

### Code Quality Improvement
```
"Get code metrics" → "Suggest improvements" → "Implement suggestions" → "Validate"
```

## Voice Command Best Practices

- Speak clearly and naturally
- Use complete sentences
- Wait for Surya's response before next command
- Say "stop" if you need to interrupt
- Use "bye" to exit gracefully

## Troubleshooting Common Issues

**Surya not responding:**
- Check microphone permissions
- Verify OpenAI API key is set
- Say "Hello Surya" to activate

**Commands not working:**
- Ensure you're in active listening mode
- Speak clearly and avoid background noise
- Rephrase the command if not understood

**Tests failing after refactoring:**
- Ask "Rollback the last change"
- Review the specific test failures
- Request targeted fixes

This guide provides comprehensive examples for using all features of the autonomous AI voice assistant effectively.
