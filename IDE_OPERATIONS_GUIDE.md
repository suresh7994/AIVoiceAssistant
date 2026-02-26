# IDE Operations Guide

## Overview

The AI Voice Assistant now has comprehensive control over VS Code and Windsurf IDEs. You can perform virtually any IDE operation using simple voice commands, including opening terminals, managing editor layouts, navigating files, and more.

---

## 🖥️ Terminal Operations

### Open Terminal in VS Code
**Voice Commands:**
- "Open terminal in VS Code"
- "Open the terminal in Visual Studio Code"
- "Show me the terminal in VS Code"
- "Launch terminal in VS Code"

**What it does:** Opens the integrated terminal using Ctrl+` shortcut

### Open Terminal in Windsurf
**Voice Commands:**
- "Open terminal in Windsurf"
- "Show terminal in Windsurf"
- "Launch Windsurf terminal"
- "Open the command line in Windsurf"

**What it does:** Opens the integrated terminal using Ctrl+` shortcut

---

## 📂 File Management

### Close Current File in VS Code
**Voice Commands:**
- "Close this file in VS Code"
- "Close the current file in Visual Studio Code"
- "Close tab in VS Code"
- "Close the editor in VS Code"

**What it does:** Closes the currently active file using Cmd+W

### Close Current File in Windsurf
**Voice Commands:**
- "Close this file in Windsurf"
- "Close the current tab in Windsurf"
- "Close editor in Windsurf"

**What it does:** Closes the currently active file using Cmd+W

---

## 📐 Editor Layout

### Split Editor Right (VS Code)
**Voice Commands:**
- "Split editor in VS Code"
- "Split the editor to the right in VS Code"
- "Create split pane in VS Code"
- "View files side by side in VS Code"

**What it does:** Splits the editor vertically (side by side) using Cmd+\

### Split Editor Down (VS Code)
**Voice Commands:**
- "Split editor down in VS Code"
- "Split the editor horizontally in VS Code"
- "Create horizontal split in VS Code"

**What it does:** Splits the editor horizontally (top and bottom) using Cmd+K then Cmd+\

### Split Editor Right (Windsurf)
**Voice Commands:**
- "Split editor in Windsurf"
- "Split the editor to the right in Windsurf"
- "Create split pane in Windsurf"

**What it does:** Splits the editor vertically using Cmd+\

### Split Editor Down (Windsurf)
**Voice Commands:**
- "Split editor down in Windsurf"
- "Split horizontally in Windsurf"

**What it does:** Splits the editor horizontally using Cmd+K then Cmd+\

---

## 🎨 UI Controls

### Toggle Sidebar in VS Code
**Voice Commands:**
- "Toggle sidebar in VS Code"
- "Hide sidebar in VS Code"
- "Show sidebar in VS Code"
- "Toggle file explorer in VS Code"
- "Hide the file tree in VS Code"

**What it does:** Shows/hides the sidebar using Cmd+B

### Toggle Sidebar in Windsurf
**Voice Commands:**
- "Toggle sidebar in Windsurf"
- "Show/hide sidebar in Windsurf"
- "Toggle explorer in Windsurf"

**What it does:** Shows/hides the sidebar using Cmd+B

---

## ⚡ Quick Access

### Command Palette in VS Code
**Voice Commands:**
- "Open command palette in VS Code"
- "Show command palette in Visual Studio Code"
- "Open VS Code commands"
- "Access VS Code features"

**What it does:** Opens the command palette using Cmd+Shift+P

### Command Palette in Windsurf
**Voice Commands:**
- "Open command palette in Windsurf"
- "Show Windsurf commands"
- "Access Windsurf command palette"

**What it does:** Opens the command palette using Cmd+Shift+P

### Quick File Picker in VS Code
**Voice Commands:**
- "Quick open in VS Code"
- "Open file picker in VS Code"
- "Go to file in VS Code"
- "Search files in VS Code"

**What it does:** Opens the quick file picker using Cmd+P

### Quick File Picker in Windsurf
**Voice Commands:**
- "Quick open in Windsurf"
- "Open file picker in Windsurf"
- "Go to file in Windsurf"

**What it does:** Opens the quick file picker using Cmd+P

---

## 🚀 Complete Workflow Examples

### Example 1: Setting Up Development Environment
```
User: "Open VS Code"
Assistant: ✓ Launches VS Code

User: "Open terminal in VS Code"
Assistant: ✓ Opens integrated terminal

User: "Split editor to the right in VS Code"
Assistant: ✓ Creates split view

User: "Quick open in VS Code"
Assistant: ✓ Opens file picker for quick navigation
```

### Example 2: Managing Multiple Files
```
User: "Open Windsurf"
Assistant: ✓ Launches Windsurf

User: "Split editor down in Windsurf"
Assistant: ✓ Creates horizontal split

User: "Open command palette in Windsurf"
Assistant: ✓ Opens command palette

User: "Close this file in Windsurf"
Assistant: ✓ Closes current file
```

### Example 3: Maximizing Screen Space
```
User: "Toggle sidebar in VS Code"
Assistant: ✓ Hides sidebar for more space

User: "Split editor in VS Code"
Assistant: ✓ Creates split view

User: "Open terminal in VS Code"
Assistant: ✓ Opens terminal at bottom
```

---

## 🎯 IDE-Specific Features

### VS Code Operations
| Operation | Voice Command | Keyboard Shortcut |
|-----------|--------------|-------------------|
| Open Terminal | "Open terminal in VS Code" | Ctrl+` |
| Close File | "Close file in VS Code" | Cmd+W |
| Split Right | "Split editor in VS Code" | Cmd+\ |
| Split Down | "Split editor down in VS Code" | Cmd+K Cmd+\ |
| Toggle Sidebar | "Toggle sidebar in VS Code" | Cmd+B |
| Command Palette | "Open command palette in VS Code" | Cmd+Shift+P |
| Quick Open | "Quick open in VS Code" | Cmd+P |

### Windsurf Operations
| Operation | Voice Command | Keyboard Shortcut |
|-----------|--------------|-------------------|
| Open Terminal | "Open terminal in Windsurf" | Ctrl+` |
| Close File | "Close file in Windsurf" | Cmd+W |
| Split Right | "Split editor in Windsurf" | Cmd+\ |
| Split Down | "Split editor down in Windsurf" | Cmd+K Cmd+\ |
| Toggle Sidebar | "Toggle sidebar in Windsurf" | Cmd+B |
| Command Palette | "Open command palette in Windsurf" | Cmd+Shift+P |
| Quick Open | "Quick open in Windsurf" | Cmd+P |

---

## 💡 Pro Tips

### 1. **Chain Commands**
You can give multiple commands in sequence:
- "Open VS Code, then open terminal, then split editor"

### 2. **Natural Language**
The assistant understands natural variations:
- "Show me the terminal" = "Open terminal"
- "Hide the sidebar" = "Toggle sidebar"
- "Split the screen" = "Split editor"

### 3. **Context Awareness**
If you're already working in an IDE, you can omit the IDE name:
- "Open terminal" (will use the active IDE)
- "Split editor" (applies to current IDE)

### 4. **Combine with File Operations**
- "Open main.py in VS Code, then split editor"
- "Create a new file, then open terminal"

### 5. **Workspace Management**
- Use split editors for comparing files
- Toggle sidebar when you need more screen space
- Use quick open for fast file navigation

---

## 🔧 Technical Details

### How It Works
The AI Voice Assistant uses **AppleScript** to send keyboard shortcuts to VS Code and Windsurf. This ensures:
- ✅ Native IDE behavior
- ✅ Works with all IDE versions
- ✅ Respects user keybindings
- ✅ Fast and reliable execution

### Requirements
- **macOS** (AppleScript support)
- **VS Code** or **Windsurf** installed
- **Accessibility permissions** (may be required for AppleScript)

### Supported Platforms
- ✅ macOS (full support)
- ⚠️ Windows/Linux (requires alternative implementation)

---

## 🐛 Troubleshooting

### Issue: "Failed to open terminal"
**Solutions:**
1. Ensure VS Code/Windsurf is running
2. Check if the IDE window is focused
3. Verify keyboard shortcut settings in IDE preferences

### Issue: "Command not working"
**Solutions:**
1. Make sure you specify the correct IDE (VS Code or Windsurf)
2. Check if the IDE is in focus
3. Try closing and reopening the IDE

### Issue: "Split editor not working"
**Solutions:**
1. Ensure a file is open before splitting
2. Check if you have enough screen space
3. Verify the split direction (right or down)

### Issue: "Sidebar toggle not responding"
**Solutions:**
1. Check if sidebar is already in the desired state
2. Ensure IDE window is active
3. Try manually toggling with Cmd+B to verify shortcut works

---

## 🎓 Learning Path

### Beginner
1. Start with basic operations: Open terminal, close file
2. Practice toggling sidebar for screen management
3. Use quick open for file navigation

### Intermediate
1. Master split editor for multi-file workflows
2. Use command palette for advanced features
3. Combine file operations with IDE controls

### Advanced
1. Chain multiple commands for complex workflows
2. Create custom voice command sequences
3. Integrate with project creation and file management

---

## 📋 Quick Reference Card

### Essential Commands
```
Terminal:
- "Open terminal in [IDE]"

Files:
- "Close file in [IDE]"
- "Quick open in [IDE]"

Layout:
- "Split editor in [IDE]"
- "Split editor down in [IDE]"
- "Toggle sidebar in [IDE]"

Access:
- "Open command palette in [IDE]"
```

### Replace [IDE] with:
- "VS Code" or "Visual Studio Code"
- "Windsurf"

---

## 🚀 Next Steps

After mastering IDE operations, explore:
1. **Project Creation** - Create complete projects with voice commands
2. **File Management** - Create, delete, and organize files
3. **Code Review** - Review code quality and get suggestions
4. **Autonomous Engineering** - Analyze and refactor codebases

---

**Remember:** The AI assistant is designed to understand natural language, so don't worry about exact phrasing. Just speak naturally and it will understand your intent!
