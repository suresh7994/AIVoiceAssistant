# Intelligent File & Folder Navigation

Surya can now automatically identify, find, and navigate to any file or folder using natural language commands!

## New Capabilities

### 1. Find Files Automatically
Surya can search for files by name across directories.

**Voice Commands:**
- "Find the file main.py"
- "Locate test.js"
- "Search for config file"
- "main.py फाइल ढूंढो"
- "कॉन्फिग फाइल कहां है?"

**What it does:**
- Searches current directory and all subdirectories
- Finds partial matches (e.g., "config" finds "config.json", "app.config.js")
- Returns all matching file paths
- Can search in specific directories

**Example:**
```
You: "Find the file agent_brain"
Surya: "Found 1 file: /Users/username/project/agent_brain.py"
```

### 2. Find Folders Automatically
Surya can locate folders/directories by name.

**Voice Commands:**
- "Find the folder src"
- "Locate the tests directory"
- "Where is the utils folder?"
- "src फोल्डर ढूंढो"

**What it does:**
- Searches for folders recursively
- Finds partial matches
- Returns all matching folder paths

**Example:**
```
You: "Find the folder tests"
Surya: "Found 1 folder: /Users/username/project/tests"
```

### 3. Get Current Location
Know where you are in the file system.

**Voice Commands:**
- "Where am I?"
- "What's the current directory?"
- "Show current folder"
- "मैं कहां हूं?"

**Example:**
```
You: "Where am I?"
Surya: "Current directory: /Users/username/AIVoiceAssistant"
```

### 4. Navigate to Folders
Change to any directory.

**Voice Commands:**
- "Go to the src folder"
- "Change to /Users/username/projects"
- "Navigate to the parent directory"
- "src फोल्डर में जाओ"

**Example:**
```
You: "Change to the tests folder"
Surya: "Changed to directory: /Users/username/project/tests"
```

### 5. Get File/Folder Information
Get detailed information about any file or folder.

**Voice Commands:**
- "Tell me about main.py"
- "What's the size of config.json?"
- "When was agent_brain.py modified?"
- "main.py के बारे में बताओ"

**What it shows:**
- File or directory type
- Size (for files)
- Last modified date
- Creation date
- Number of items (for directories)

**Example:**
```
You: "Tell me about main.py"
Surya: "main.py is a file, 5.2 KB, modified on 2026-02-23 15:30:00"
```

### 6. List Files and Folders
See what's in any directory.

**Voice Commands:**
- "List files in current directory"
- "Show me what's in the src folder"
- "What files are here?"
- "यहां क्या फाइलें हैं?"

**Example:**
```
You: "List files here"
Surya: "Found 5 files: main.py, agent_brain.py, ui.py, speech_to_text.py, text_to_speech.py
And 2 directories: tests, docs"
```

## How It Works

### Intelligent Search
- **Recursive**: Searches all subdirectories automatically
- **Partial Matching**: "config" finds "config.json", "app.config.js", etc.
- **Case Insensitive**: Works regardless of capitalization
- **Fast**: Uses Python's `os.walk()` for efficient traversal

### Natural Language Understanding
Surya understands various ways to ask:
- "Find the file X" = `find_file`
- "Where is folder Y?" = `find_folder`
- "Go to directory Z" = `change_directory`
- "Tell me about file A" = `get_file_info`

### Smart Context
- Searches from current directory by default
- Can specify custom search paths
- Remembers current location across commands

## Example Workflows

### Workflow 1: Find and Open File
```
You: "Hello Surya"
Surya: "Yes, I'm listening"

You: "Find the file agent_brain"
Surya: "Found 1 file: /Users/username/project/agent_brain.py"

You: "Open it in VS Code"
Surya: "Opened agent_brain.py in VS Code"
```

### Workflow 2: Navigate and List
```
You: "Where am I?"
Surya: "Current directory: /Users/username/AIVoiceAssistant"

You: "Find the tests folder"
Surya: "Found 1 folder: /Users/username/AIVoiceAssistant/tests"

You: "Go to that folder"
Surya: "Changed to directory: /Users/username/AIVoiceAssistant/tests"

You: "List files here"
Surya: "Found 3 files: test_main.py, test_agent.py, test_ui.py"
```

### Workflow 3: File Information
```
You: "Find config file"
Surya: "Found 2 files: config.json, app.config.js"

You: "Tell me about config.json"
Surya: "config.json is a file, 1.5 KB, modified on 2026-02-20 10:15:00"
```

## Hindi Support

All commands work in Hindi:
- "main.py फाइल ढूंढो" (Find main.py file)
- "src फोल्डर कहां है?" (Where is src folder?)
- "मैं कहां हूं?" (Where am I?)
- "tests फोल्डर में जाओ" (Go to tests folder)
- "यहां क्या फाइलें हैं?" (What files are here?)

## Technical Details

### New Methods in `WindsurfController`

1. **`find_file(filename, search_path=".")`**
   - Recursively searches for files
   - Returns list of matching paths
   - Case-insensitive partial matching

2. **`find_folder(foldername, search_path=".")`**
   - Recursively searches for folders
   - Returns list of matching paths
   - Case-insensitive partial matching

3. **`get_current_directory()`**
   - Returns current working directory path
   - No parameters needed

4. **`change_directory(path)`**
   - Changes to specified directory
   - Updates current working directory

5. **`get_file_info(path)`**
   - Returns detailed file/folder metadata
   - Size, type, dates, item count

6. **`list_files(directory=".")`**
   - Lists files and folders separately
   - Returns organized dictionary

### Tools Available to AI

```python
{
    "name": "find_file",
    "description": "Find a file by name in subdirectories",
    "parameters": {
        "filename": "Name or partial name",
        "search_path": "Optional starting path"
    }
}

{
    "name": "find_folder",
    "description": "Find a folder by name in subdirectories",
    "parameters": {
        "foldername": "Name or partial name",
        "search_path": "Optional starting path"
    }
}

{
    "name": "get_current_directory",
    "description": "Get current working directory"
}

{
    "name": "change_directory",
    "description": "Navigate to a different folder",
    "parameters": {
        "path": "Directory path"
    }
}

{
    "name": "get_file_info",
    "description": "Get file/folder details",
    "parameters": {
        "path": "File or folder path"
    }
}
```

## Use Cases

1. **Project Navigation**: Quickly find and navigate to project files
2. **File Discovery**: Locate configuration files, tests, or specific modules
3. **IDE Integration**: Find files and open them in Windsurf or VS Code
4. **File Management**: Get information before editing or deleting
5. **Workspace Exploration**: Understand project structure through voice

## Tips

- **Be specific**: "Find test file" is better than just "find file"
- **Use partial names**: "config" finds all config files
- **Combine commands**: Find → Navigate → Open → Edit
- **Check location**: Use "Where am I?" to orient yourself
- **Get info first**: Check file details before opening

## Limitations

- Search depth: Searches all subdirectories (may be slow for very large projects)
- Hidden files: Does not search hidden files/folders by default
- Permissions: Requires read access to directories
- Symbolic links: Follows symbolic links during search

## Future Enhancements

Potential additions:
- Filter by file type/extension
- Search by file content
- Search by date modified
- Exclude certain directories
- Fuzzy matching for typos
- Recent files tracking
