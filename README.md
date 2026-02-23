# Voice-Enabled AI Agent

Production-ready personal voice AI assistant with real-time conversation capabilities.

## Features

- **Speech-to-Text**: Real-time microphone input processing
- **Text-to-Speech**: Natural AI voice output with configurable rate/volume
- **OpenAI Integration**: Streaming responses for low latency
- **Conversational Memory**: Short-term context retention (20 messages)
- **Modern UI**: Dark mode with animated waveforms (listening/speaking states)
- **Interrupt Handling**: Stop AI mid-speech to ask new questions
- **Error Handling**: Robust error management throughout

## Architecture

```
ai-project/
├── main.py              # Entry point and orchestration
├── speech_to_text.py    # Microphone input → text
├── text_to_speech.py    # Text → audio output
├── agent_brain.py       # OpenAI API integration
├── ui.py                # PyQt5 modern UI with waveforms
└── requirements.txt     # Dependencies
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

1. Click **"🎤 Start Listening"** to begin voice input
2. Speak your question or command
3. AI will process and respond with voice
4. Click **"🔴 Stop Listening"** to stop
5. AI can be interrupted while speaking

### Status Indicators

- **Ready**: Idle state
- **Listening...**: Recording your voice (blue waveform)
- **Thinking...**: Processing with OpenAI
- **Speaking...**: AI responding (green waveform)

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
