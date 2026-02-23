import sys
import os
from dotenv import load_dotenv
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from agent_brain import AgentBrain
from ui import create_app
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceAgent(QObject):
    speaking_signal = pyqtSignal(bool)
    
    def __init__(self, ui):
        super().__init__(ui)
        self.speaking_signal.connect(self.on_speaking_changed)
        self.ui = ui
        self.signals = ui.get_signals()
        
        self.stt = SpeechToText(language="en-US")
        self.tts = TextToSpeech(rate=175, volume=0.9)
        self.brain = AgentBrain()
        
        self.is_listening = False
        self.current_response = ""
        self.auto_listen = False
        self.is_processing = False
        
        self.restart_timer = QTimer(self)
        self.restart_timer.setSingleShot(True)
        self.restart_timer.timeout.connect(self.auto_restart_listening)

        self.tts.set_speaking_callback(self.speaking_signal.emit)
        
        ui.set_mic_callback(self.toggle_listening)
    
    def toggle_listening(self):
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()
    
    def start_listening(self):
        if self.is_listening:
            return
        
        self.is_listening = True
        self.auto_listen = True
        self.signals.status_changed.emit("Listening...")
        
        self.stt.start_listening(
            callback=self.on_speech_recognized,
            error_callback=self.on_stt_error
        )
    
    def stop_listening(self):
        if not self.is_listening:
            return
        
        self.is_listening = False
        self.auto_listen = False
        self.stt.stop_listening()
        self.signals.status_changed.emit("Ready")
    
    def on_speech_recognized(self, text: str):
        if self.is_processing:
            return
        
        logger.info(f"Recognized: {text}")
        
        self.is_processing = True
        self.is_listening = False
        self.stt.stop_listening()
        
        self.signals.status_changed.emit("Thinking...")
        
        self.tts.stop_speaking()
        
        self.current_response = ""
        
        def stream_callback(chunk: str):
            self.current_response += chunk
        
        response = self.brain.process_input(text, stream_callback=stream_callback)
        
        logger.info(f"Response: {response}")
        
        self.signals.status_changed.emit("Speaking...")
        self.tts.speak(response)
    
    
    def auto_restart_listening(self):
        if self.auto_listen and not self.is_listening:
            self.start_listening()
    
    def on_speaking_changed(self, is_speaking: bool):
        if is_speaking:
            self.signals.status_changed.emit("Speaking...")
        else:
            self.is_processing = False
            if self.auto_listen and not self.is_listening:
                self.restart_timer.start(500)
            else:
                self.signals.status_changed.emit("Ready")

    def on_stt_error(self, error: str):
        logger.error(f"STT Error: {error}")
        self.signals.status_changed.emit("Error - Check microphone")
    
    def shutdown(self):
        self.stop_listening()
        self.tts.shutdown()


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set it using: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)
    
    app, ui = create_app()
    
    app.setQuitOnLastWindowClosed(True)
    
    agent = VoiceAgent(ui)
    
    ui.show()
    
    exit_code = app.exec_()
    
    agent.shutdown()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
