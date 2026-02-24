import sys
import os
from dotenv import load_dotenv
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject
from PyQt5.QtWidgets import QApplication
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
    activate_signal = pyqtSignal()  # Thread-safe signal for activation
    
    def __init__(self, ui):
        super().__init__(ui)
        self.speaking_signal.connect(self.on_speaking_changed)
        self.ui = ui
        self.signals = ui.get_signals()
        
        self.stt = SpeechToText(language="en-US")
        self.tts = TextToSpeech(rate=175, volume=0.9, voice="Rahul")
        self.brain = AgentBrain()
        
        self.is_listening = False
        self.current_response = ""
        self.auto_listen = False
        self.is_processing = False
        self.wake_word_mode = True
        self.assistant_name = "Surya"
        self.wake_words = ['surya', 'सूर्या', 'सूर्य']
        
        self.restart_timer = QTimer(self)
        self.restart_timer.setSingleShot(True)
        self.restart_timer.timeout.connect(self.auto_restart_listening)

        self.tts.set_speaking_callback(self.speaking_signal.emit)
        
        # Connect activation signal to slot
        self.activate_signal.connect(self.delayed_activate_listening)
        
        ui.set_mic_callback(self.toggle_listening)
        
        self.exit_keywords = [
            'bye', 'goodbye', 'exit', 'quit', 'shutdown', 'shut down',
            'close', 'stop', 'बाय', 'गुडबाय', 'बंद करो', 'शट डाउन'
        ]
        
        # Start in wake word listening mode
        self.start_wake_word_listening()
    
    def toggle_listening(self):
        if self.wake_word_mode:
            # User wants to start listening from wake word mode
            self.wake_word_mode = False
            self.start_listening()
        elif self.is_listening:
            # User wants to stop - completely stop, don't restart
            self.stop_listening()
        else:
            # User wants to start listening again
            self.start_listening()
    
    def start_wake_word_listening(self):
        """Start listening for wake word only"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.wake_word_mode = True
        self.signals.status_changed.emit(f"Say 'Hello {self.assistant_name}' to activate")
        
        self.stt.start_listening(
            callback=self.on_wake_word_detected,
            error_callback=self.on_stt_error
        )
    
    def delayed_activate_listening(self):
        """Slot called by activate_signal after TTS finishes"""
        logger.info("Delayed activation triggered...")
        # Wait for TTS to finish using QTimer (now in main thread)
        QTimer.singleShot(2500, self.activate_listening)
    
    def activate_listening(self):
        """Activate listening after wake word detection"""
        logger.info("Activating listening mode after wake word...")
        
        # Ensure clean state
        self.stt.stop_listening()
        
        # Set flags
        self.is_listening = True
        self.wake_word_mode = False
        self.auto_listen = True
        self.is_processing = False
        
        logger.info(f"State: is_listening={self.is_listening}, wake_word_mode={self.wake_word_mode}, auto_listen={self.auto_listen}")
        
        self.signals.status_changed.emit("Listening...")
        
        # Start listening for commands
        self.stt.start_listening(
            callback=self.on_speech_recognized,
            error_callback=self.on_stt_error
        )
        
        logger.info("Active listening started - ready for commands")
    
    def start_listening(self):
        if self.is_listening and not self.wake_word_mode:
            return
        
        self.stt.stop_listening()
        
        self.is_listening = True
        self.wake_word_mode = False
        self.auto_listen = True
        self.signals.status_changed.emit("Listening...")
        
        self.stt.start_listening(
            callback=self.on_speech_recognized,
            error_callback=self.on_stt_error
        )
    
    def stop_listening(self):
        if not self.is_listening:
            return
        
        # Stop the restart timer to prevent auto-restart
        self.restart_timer.stop()
        
        self.is_listening = False
        self.auto_listen = False
        self.stt.stop_listening()
        
        # Also stop TTS if speaking
        self.tts.stop()
        
        if self.wake_word_mode:
            self.signals.status_changed.emit(f"Say 'Hello {self.assistant_name}' to activate")
        else:
            self.signals.status_changed.emit("Stopped")
    
    def check_wake_word(self, text: str) -> bool:
        """Check if the text contains wake word"""
        text_lower = text.lower()
        for wake_word in self.wake_words:
            if wake_word in text_lower:
                return True
        return False
    
    def check_exit_keywords(self, text: str) -> bool:
        """Check if the text contains exit keywords"""
        text_lower = text.lower()
        for keyword in self.exit_keywords:
            if keyword in text_lower:
                return True
        return False
    
    def exit_application(self):
        """Gracefully exit the application"""
        logger.info("Exit command detected. Shutting down...")
        self.signals.status_changed.emit("Shutting down...")
        
        goodbye_message = "Goodbye! Have a great day!"
        self.tts.speak(goodbye_message)
        
        QTimer.singleShot(3000, self.perform_shutdown)
    
    def perform_shutdown(self):
        """Perform the actual shutdown"""
        self.shutdown()
        QApplication.quit()
    
    def on_wake_word_detected(self, text: str):
        """Handle wake word detection (runs in STT thread)"""
        logger.info(f"Wake word check: {text}")
        
        if self.check_wake_word(text):
            logger.info(f"{self.assistant_name} activated!")
            
            # Stop listening to prevent feedback loop
            self.stt.stop_listening()
            self.is_listening = False
            
            # Immediately switch to active mode
            self.wake_word_mode = False
            self.auto_listen = True
            self.is_processing = False
            
            # Speak confirmation and transition to listening
            self.signals.status_changed.emit("Activating...")
            self.tts.speak(f"Yes, I'm listening")
            
            # Emit signal to trigger activation in main thread (thread-safe)
            self.activate_signal.emit()
            
            logger.info("Wake word activation sequence started")
    
    def on_speech_recognized(self, text: str):
        logger.info(f"on_speech_recognized called with: {text}")
        logger.info(f"Current state - is_processing: {self.is_processing}, wake_word_mode: {self.wake_word_mode}")
        
        if self.is_processing:
            logger.info("Already processing, ignoring input")
            return
        
        logger.info(f"Recognized: {text}")
        
        if self.check_exit_keywords(text):
            self.exit_application()
            return
        
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
            
            # After speaking, continue listening for next command (stay in active mode)
            if self.auto_listen and not self.is_listening:
                # Restart listening automatically
                self.restart_timer.start(500)
            else:
                if self.wake_word_mode:
                    self.signals.status_changed.emit(f"Say 'Hello {self.assistant_name}' to activate")
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
