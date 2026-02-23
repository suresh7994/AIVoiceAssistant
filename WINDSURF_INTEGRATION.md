# Windsurf IDE Integration

This voice assistant can control Windsurf IDE and VS Code through voice commands.

> **Note:** For VS Code specific documentation, see [VSCODE_INTEGRATION.md](VSCODE_INTEGRATION.md)

Your voice assistant now has full access to Windsurf IDE operations! You can control the IDE using voice commands in Hindi.

## Available Commands

The assistant can now perform the following operations:

### IDE Operations
- **Open Windsurf**: "Open Windsurf IDE" or "Launch Windsurf"
- **Open with path**: "Open Windsurf with current directory"
- **Auto-detect**: Automatically detects if Windsurf is running

### File Operations
- **Open files**: "Open the main.py file"
- **Create files**: "Create a new file called test.py"
- **Read files**: "Read the contents of agent_brain.py"
- **Write/Update files**: "Write hello world to test.py"

### Search Operations
- **Search in files**: "Search for the word 'function' in all files"
- **List files**: "Show me all files in the current directory"

### Terminal Commands
- **Run commands**: "Run python main.py"
- **Execute scripts**: "Run npm install"

## How It Works

1. **Voice Input**: You speak in Hindi (hi-IN)
2. **Speech Recognition**: Converts your Hindi speech to text
3. **AI Processing**: GPT-4 understands your intent and decides which tools to use
4. **Tool Execution**: The Windsurf controller executes the requested operations
5. **Voice Response**: The assistant responds in Hindi using the Lekha voice

## Example Voice Commands

### Hindi Commands (Examples)
- "विंडसर्फ खोलो" (Open Windsurf)
- "विंडसर्फ आईडीई लॉन्च करो" (Launch Windsurf IDE)
- "मुख्य फ़ाइल खोलो" (Open main file)
- "नई फ़ाइल बनाओ" (Create new file)
- "सभी फ़ाइलें दिखाओ" (Show all files)
- "कोड चलाओ" (Run the code)

### English Commands (for reference)
- "Open Windsurf IDE"
- "Launch Windsurf"
- "Open the speech_to_text.py file"
- "Create a new file called utils.py with a hello function"
- "Search for 'SpeechToText' in all Python files"
- "List all files in the project"
- "Run the main application"

## Technical Details

### Components Added

1. **windsurf_controller.py**: 
   - Handles all IDE operations
   - Provides 7 different tools for file and terminal operations
   - Uses subprocess for command execution

2. **Updated agent_brain.py**:
   - Integrated OpenAI function calling
   - Automatically detects when to use Windsurf tools
   - Executes tools and provides natural language responses

### Tools Available

1. `open_windsurf` - Launch or open Windsurf IDE (with auto-detection)
2. `open_file` - Open files in Windsurf
3. `create_file` - Create new files with content
4. `read_file` - Read file contents
5. `write_file` - Write/update file contents
6. `search_in_files` - Search text in files
7. `run_terminal_command` - Execute terminal commands
8. `list_files` - List directory contents

## Safety Features

- All operations are logged
- Timeout protection (30 seconds max)
- Error handling for failed operations
- Conversation history maintained for context

## Usage Tips

1. Be specific with file paths when possible
2. Use natural language - the AI will understand intent
3. The assistant will confirm actions before executing dangerous operations
4. You can chain multiple commands in one request

## Configuration

The integration is automatically enabled. No additional setup required beyond:
- OpenAI API key (already configured)
- Hindi language support (already configured)
- Lekha voice for Hindi TTS (already configured)

Enjoy controlling Windsurf with your voice in Hindi! 🎤
