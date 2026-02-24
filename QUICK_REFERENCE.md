# Quick Reference - Autonomous AI Voice Assistant

## Activation
```
"Hello Surya" or "Hi Surya"
```

## Core Commands

### Codebase Analysis
| Command | Action |
|---------|--------|
| "Analyze the codebase" | Full project analysis |
| "Analyze [filename]" | Analyze specific file |
| "What are the code metrics?" | Get quality metrics |
| "Get code quality stats" | Overall quality report |

### Code Refactoring
| Command | Action |
|---------|--------|
| "Refactor [filename]" | Refactor file |
| "Rename variable [old] to [new] in [file]" | Rename variable |
| "Reduce complexity in [file]" | Simplify code |
| "Simplify conditionals in [file]" | Simplify logic |

### Testing
| Command | Action |
|---------|--------|
| "Generate tests for [filename]" | Create test file |
| "Run all tests" | Execute test suite |
| "Run tests" | Execute tests |

### Dependencies
| Command | Action |
|---------|--------|
| "Check dependencies" | Check for updates |
| "Update dependencies" | Safe update |
| "Check for outdated packages" | List outdated |

### Bug Detection
| Command | Action |
|---------|--------|
| "Find bugs" | Detect issues |
| "Check for code issues" | Static analysis |
| "Fix bugs in [file]" | Auto-fix bugs |

### Documentation
| Command | Action |
|---------|--------|
| "Generate documentation" | Create docs |
| "Document the codebase" | Full documentation |

### Improvements
| Command | Action |
|---------|--------|
| "Suggest improvements" | Get suggestions |
| "Suggest performance improvements" | Performance focus |
| "What can be improved?" | General suggestions |

### Architecture
| Command | Action |
|---------|--------|
| "Validate architecture" | Check patterns |
| "Check architecture" | Validate design |

### History
| Command | Action |
|---------|--------|
| "Show execution history" | View actions |
| "What changes were made?" | Recent changes |

### IDE Control
| Command | Action |
|---------|--------|
| "Open Windsurf" | Launch Windsurf IDE |
| "Open VS Code" | Launch VS Code |
| "Open [filename] in VS Code" | Open file |
| "Create file [filename]" | Create new file |
| "Find file [name]" | Search for file |

### File Navigation
| Command | Action |
|---------|--------|
| "Where am I?" | Current directory |
| "List files" | Show directory contents |
| "Go to [folder]" | Change directory |
| "Find folder [name]" | Search for folder |

### Teams Integration
| Command | Action |
|---------|--------|
| "Schedule meeting [details]" | Create meeting |
| "Reply to latest chat" | Send message |
| "Show recent chats" | List chats |

### Code Review
| Command | Action |
|---------|--------|
| "Review [filename]" | Review file |
| "Check [filename] for issues" | Find problems |

### System Control
| Command | Action |
|---------|--------|
| "Bye" / "Exit" / "Quit" | Close application |
| "Stop" | Stop current action |

## Workflow Patterns

### Quality Improvement
```
1. "Analyze the codebase"
2. "Suggest improvements"
3. "Refactor [files]"
4. "Run tests"
5. "Generate documentation"
```

### Bug Fixing
```
1. "Find bugs"
2. "Fix bugs in [file]"
3. "Run tests"
```

### Maintenance
```
1. "Check dependencies"
2. "Update dependencies"
3. "Run tests"
```

### Development
```
1. "Create file [name]"
2. "Generate tests for [file]"
3. "Run tests"
4. "Review [file]"
```

## Safety Features

✅ **Automatic Backups** - Before refactoring  
✅ **Safety Checks** - For destructive operations  
✅ **Rollback Support** - Checkpoint system  
✅ **Health Monitoring** - Continuous system checks  
✅ **Audit Trail** - All actions logged  

## Status Indicators

- **"Say 'Hello Surya' to activate"** - Wake word mode
- **"Listening..."** - Recording voice
- **"Thinking..."** - Processing request
- **"Speaking..."** - AI responding
- **"Ready"** - Active mode, no wake word needed

## Tips

💡 Speak clearly and naturally  
💡 Wait for response before next command  
💡 Use complete sentences  
💡 Say "stop" to interrupt  
💡 Create checkpoints before major changes  
💡 Always run tests after refactoring  

## File Locations

- **Logs**: `autonomous_agent.log`
- **Backups**: `[filename].backup`
- **Checkpoints**: `.checkpoints/`
- **Tests**: `test_[filename].py`
- **Docs**: `ARCHITECTURE.md`

## Common Issues

**Not responding?**
- Check microphone permissions
- Verify API key is set
- Say "Hello Surya" to activate

**Command not understood?**
- Rephrase more clearly
- Use simpler language
- Check examples in USAGE_EXAMPLES.md

**Tests failing?**
- Review error details
- Ask "What went wrong?"
- Request rollback if needed

## Documentation

📚 **Full Guides**
- [AUTONOMOUS_AGENT_GUIDE.md](AUTONOMOUS_AGENT_GUIDE.md) - Complete autonomous agent documentation
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Detailed usage examples
- [README.md](README.md) - Main project documentation
- [WINDSURF_INTEGRATION.md](WINDSURF_INTEGRATION.md) - IDE integration
- [TEAMS_INTEGRATION.md](TEAMS_INTEGRATION.md) - Teams setup
- [REVIEWER_GUIDE.md](REVIEWER_GUIDE.md) - Code review features

## Quick Start

1. **Activate**: "Hello Surya"
2. **Analyze**: "Analyze the codebase"
3. **Improve**: "Suggest improvements"
4. **Test**: "Run all tests"
5. **Document**: "Generate documentation"

## Emergency Commands

🚨 **"Stop"** - Interrupt current operation  
🚨 **"Rollback"** - Undo last change  
🚨 **"Exit"** - Close application  

---

**Version**: 1.0  
**Last Updated**: 2026-02-24
