# Surya - Voice-Enabled AI Assistant

Production-ready personal voice AI assistant named **Surya** with wake word activation and real-time conversation capabilities.

## Features

- **Wake Word Activation**: Say "Hello Surya" or "Hi Surya" to activate the assistant
- **Speech-to-Text**: Real-time microphone input processing with Hindi (hi-IN) support
- **Text-to-Speech**: Natural AI voice output with Hindi female voice (Lekha)
- **OpenAI Integration**: Streaming responses for low latency
- **Conversational Memory**: Short-term context retention (20 messages)
- **Modern UI**: Dark mode with animated waveforms (listening/speaking states)
- **Interrupt Handling**: Stop AI mid-speech to ask new questions
- **Windsurf IDE Control**: Voice-controlled IDE operations (file management, search, terminal commands)
- **Error Handling**: Robust error management throughout

## Architecture

```
ai-project/
├── main.py                    # Entry point and orchestration
├── speech_to_text.py          # Microphone input → text (Hindi support)
├── text_to_speech.py          # Text → audio output (Hindi voice)
├── agent_brain.py             # OpenAI API integration with function calling
├── windsurf_controller.py     # Windsurf IDE operations controller
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

## Windsurf IDE Control

The assistant now has full access to Windsurf IDE operations through voice commands in Hindi!

### Available Commands

- **File Operations**: Open, create, read, write files
- **Search**: Search text in files across the project
- **Terminal**: Execute terminal commands
- **Directory**: List files and navigate directories

### Example Voice Commands

**Hindi:**
- "विंडसर्फ खोलो" (Open Windsurf)
- "मुख्य फ़ाइल खोलो" (Open main file)
- "नई फ़ाइल बनाओ" (Create new file)
- "सभी फ़ाइलें दिखाओ" (Show all files)

**English:**
- "Open Windsurf IDE"
- "Open the main.py file"
- "Create a new file called test.py"
- "Search for 'function' in all files"
- "List all files in the current directory"

**Exit Commands:**
- "Bye" / "Goodbye" / "Exit" / "Shutdown"
- "बाय" / "गुडबाय" / "बंद करो" / "शट डाउन"

For detailed information, see [WINDSURF_INTEGRATION.md](WINDSURF_INTEGRATION.md)

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
