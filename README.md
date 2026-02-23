# Surya - Voice-Enabled AI Assistant

Production-ready personal voice AI assistant named **Surya** with wake word activation and real-time conversation capabilities.

## Features

- **Wake Word Activation**: Say "Hello Surya" or "Hi Surya" to activate the assistant
- **Hindi Language Support**: Full support for Hindi speech-to-text and text-to-speech
- **Voice-to-Voice Interaction**: Speak naturally and get voice responses
- **OpenAI Integration**: Powered by GPT models for intelligent responses
- **IDE Control**: Voice commands to control both Windsurf IDE and VS Code
  - **Windsurf IDE**: Open, manage files, and execute commands
  - **VS Code**: Launch, open files, and manage projects
  - Create, read, and write files
  - Search in files
  - Execute terminal commands
  - List directory contents
- **Intelligent File Navigation**: Automatically find and navigate files/folders
  - Find files by name anywhere in the project
  - Locate folders automatically
  - Get current directory and file information
  - Navigate to any folder with voice commands
  - List contents of any directory
- **Modern UI**: Clean PyQt5 interface with visual feedback
- **Graceful Exit**: Say "bye" or "exit" to close the application
- **Interrupt Handling**: Stop AI mid-speech to ask new questions
- **Error Handling**: Robust error management throughout

## Architecture

```
ai-project/
├── main.py                    # Entry point and orchestration
├── speech_to_text.py          # Microphone input → text (Hindi support)
├── text_to_speech.py          # Text → audio output (Hindi voice)
├── agent_brain.py             # OpenAI API integration with function calling
├── windsurf_controller.py     # Windsurf IDE operations controller
├── vs_code_controller.py      # VS Code operations controller
├── ui.py                      # PyQt5 modern UI with waveforms
├── requirements.txt           # Dependencies
└── WINDSURF_INTEGRATION.md    # Windsurf integration guide
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install PyAudio (macOS)

```bash
brew install portaudio
pip install pyaudio
```

### 3. Set OpenAI API Key

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or add to `~/.zshrc` or `~/.bash_profile`:

```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## Usage

### Run the Application

```bash
python main.py
```

### Controls

1. **Wake Word Mode** (Default): Say **"Hello Surya"** or **"Hi Surya"** to activate
2. Surya will respond and start listening for your command
3. Speak your question or command
4. AI will process and respond with voice
5. **Continuous conversation**: After response, stays in listening mode for next command
6. Continue speaking commands without repeating wake word
7. Click **"🎤"** button to stop listening and return to wake word mode
8. Say **"bye"**, **"exit"**, **"shutdown"**, or **"बाय"** to close the application

### Status Indicators

- **Say 'Hello Surya' to activate**: Wake word mode (waiting for activation)
- **Listening...**: Recording your voice (blue waveform)
- **Thinking...**: Processing with OpenAI
- **Speaking...**: AI responding (green waveform)
- **Ready**: Active listening mode (no wake word needed)

## Configuration

### Adjust Speech Rate/Volume

Edit `main.py`:

```python
self.tts = TextToSpeech(rate=175, volume=0.9)
```

- `rate`: 100-300 (words per minute)
- `volume`: 0.0-1.0

### Change Language

Edit `main.py`:

```python
self.stt = SpeechToText(language="en-US")
```

Supported: `en-US`, `en-GB`, `es-ES`, `fr-FR`, etc.

### Change OpenAI Model

Edit `agent_brain.py`:

```python
self.model = "gpt-4o-mini"  # or "gpt-4", "gpt-3.5-turbo"
```

## IDE Control

The assistant now has full access to both Windsurf IDE and VS Code operations through voice commands in Hindi!

### Available Commands

- **File Operations**: Open, create, read, write files
- **Search**: Search text in files across the project
- **Terminal**: Execute terminal commands
- **Directory**: List files and navigate directories

### Example Voice Commands

**General:**
- "What's the weather like?"
- "Tell me a joke"
- "क्या आप हिंदी बोल सकते हैं?"

**IDE Control:**
- "Open Windsurf IDE" / "विंडसर्फ खोलो"
- "Open VS Code" / "Open Visual Studio Code"
- "ओपन वीएस कोड"
- "Open the file main.py in VS Code"
- "Create a new file called test.py"
- "Search for 'function' in the current directory"
- "List all files in the project"
- "Run the command 'git status'"

**File Navigation:**
- "Find the file agent_brain"
- "Where is the tests folder?"
- "What's in the current directory?"
- "Go to the src folder"
- "Tell me about main.py"
- "main.py फाइल ढूंढो"
- "मैं कहां हूं?"

**Exit:**
- "Bye" / "Goodbye"
- "Exit" / "Quit"
- "बाय" / "गुडबाय" / "बंद करो" / "शट डाउन"

For detailed information:
- IDE Control: [WINDSURF_INTEGRATION.md](WINDSURF_INTEGRATION.md) and [VSCODE_INTEGRATION.md](VSCODE_INTEGRATION.md)
- File Navigation: [FILE_NAVIGATION_GUIDE.md](FILE_NAVIGATION_GUIDE.md)

## Troubleshooting

### Microphone Not Working

- Check System Preferences → Security & Privacy → Microphone
- Grant Terminal/Python microphone access

### PyAudio Installation Issues

```bash
brew install portaudio
pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio
```

### OpenAI API Errors

- Verify API key is set: `echo $OPENAI_API_KEY`
- Check API quota/billing at platform.openai.com

## System Requirements

- Python 3.8+
- macOS/Linux/Windows
- Microphone access
- Internet connection (OpenAI API)
- Active OpenAI API key

## License

MIT
