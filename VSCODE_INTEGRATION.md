# VS Code Integration

Surya voice assistant now supports **Visual Studio Code** operations alongside Windsurf IDE.

## Available Commands

### 1. Open VS Code
Launch or bring VS Code to the front.

**Voice Commands:**
- "Open VS Code"
- "Open Visual Studio Code"
- "Launch VS Code"
- "ओपन वीएस कोड"
- "विजुअल स्टूडियो कोड खोलो"

**What it does:**
- Checks if VS Code is already running
- If running, brings it to the front
- If not running, launches VS Code
- Can optionally open a specific path

### 2. Open File in VS Code
Open a specific file in VS Code using the `code` CLI.

**Voice Commands:**
- "Open main.py in VS Code"
- "Open the file test.js in Visual Studio Code"
- "वीएस कोड में main.py खोलो"

**What it does:**
- Uses the `code` command-line tool
- Opens the specified file in VS Code
- Creates a new tab if VS Code is already open

### 3. Open Path in VS Code
Open a directory or project in VS Code.

**Voice Commands:**
- "Open my project folder in VS Code"
- "Open /Users/username/projects in Visual Studio Code"

**What it does:**
- Opens the specified directory as a workspace
- Launches VS Code if not already running

## How It Works

### Detection
The system uses `pgrep` to detect if VS Code is running:
```bash
pgrep -f "Visual Studio Code"
```

### Launching
VS Code is launched using macOS `open` command:
```bash
open -a "Visual Studio Code"
```

### File Operations
Files are opened using the `code` CLI:
```bash
code /path/to/file.py
```

## Requirements

1. **VS Code Installed**: Visual Studio Code must be installed in `/Applications/`
2. **Code CLI**: The `code` command should be available in PATH
   - Install via VS Code: `Cmd+Shift+P` → "Shell Command: Install 'code' command in PATH"

## Example Conversations

### Opening VS Code
```
You: "Hello Surya"
Surya: "Yes, I'm listening"

You: "Open VS Code"
Surya: "VS Code launched successfully"
```

### Opening a File
```
You: "Open main.py in VS Code"
Surya: "Opened main.py in VS Code"
```

### Hindi Example
```
You: "हेलो सूर्य"
Surya: "Yes, I'm listening"

You: "ओपन वीएस कोड"
Surya: "VS Code launched successfully"
```

## Comparison: Windsurf vs VS Code

| Feature | Windsurf | VS Code |
|---------|----------|---------|
| Launch IDE | ✅ `open_windsurf` | ✅ `open_vscode` |
| Open File | ✅ `open_file` | ✅ `open_file_vscode` |
| Open Path | ✅ Supported | ✅ Supported |
| File Operations | ✅ Create, Read, Write | ✅ Via CLI |
| Terminal Commands | ✅ Supported | ✅ Supported |

## Technical Details

### Methods Added to `WindsurfController`

1. **`is_vscode_running()`**
   - Checks if VS Code process is active
   - Returns: `bool`

2. **`open_vscode(path: Optional[str] = None)`**
   - Opens VS Code with optional path
   - Returns: `Dict[str, Any]` with success status

3. **`open_file_vscode(file_path: str)`**
   - Opens specific file using `code` CLI
   - Returns: `Dict[str, Any]` with success status

### Tools Available to AI

```python
{
    "name": "open_vscode",
    "description": "Open or launch VS Code (Visual Studio Code)",
    "parameters": {
        "path": "Optional path to open"
    }
}

{
    "name": "open_file_vscode",
    "description": "Open a specific file in VS Code using the code CLI",
    "parameters": {
        "file_path": "The path to the file to open"
    }
}
```

## Troubleshooting

### VS Code Won't Open
- Verify VS Code is installed in `/Applications/`
- Check the app name is exactly "Visual Studio Code"
- Try manually: `open -a "Visual Studio Code"`

### Code CLI Not Found
- Install the CLI: Open VS Code → `Cmd+Shift+P` → "Shell Command: Install 'code' command in PATH"
- Restart terminal after installation
- Verify: `which code` should show the path

### File Won't Open
- Ensure the file path is correct and absolute
- Check file permissions
- Try opening manually: `code /path/to/file`

## Future Enhancements

Potential additions:
- VS Code extensions management
- Workspace switching
- Debug configuration
- Git integration via VS Code
- Terminal integration within VS Code

## Notes

- Both Windsurf and VS Code can be used in the same session
- The AI automatically detects which IDE you're referring to
- File operations (create, read, write) work independently of the IDE
- Terminal commands can be executed regardless of which IDE is open
