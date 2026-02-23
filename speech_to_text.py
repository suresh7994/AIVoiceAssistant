import speech_recognition as sr
import threading
import queue
from typing import Callable, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechToText:
    def __init__(self, language: str = "en-US"):
        self.language = language
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()
        
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.2
        self.recognizer.non_speaking_duration = 0.5
        
        microphone = sr.Microphone()
        with microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
    
    def start_listening(self, callback: Callable[[str], None], error_callback: Optional[Callable[[str], None]] = None):
        if self.is_listening:
            return
        
        self.is_listening = True
        self.stop_event.clear()
        
        self.microphone = sr.Microphone()
        
        def audio_callback(recognizer, audio):
            self.audio_queue.put(audio)
        
        self.stop_listening_func = self.recognizer.listen_in_background(
            self.microphone, 
            audio_callback,
            phrase_time_limit=5
        )
        
        def process_audio():
            while not self.stop_event.is_set():
                try:
                    audio = self.audio_queue.get(timeout=0.5)
                    try:
                        text = self.recognizer.recognize_google(audio, language=self.language)
                        if text.strip():
                            callback(text)
                    except sr.UnknownValueError:
                        logger.debug("Could not understand audio")
                    except sr.RequestError as e:
                        error_msg = f"Speech recognition error: {e}"
                        logger.error(error_msg)
                        if error_callback:
                            error_callback(error_msg)
                except queue.Empty:
                    continue
        
        self.processing_thread = threading.Thread(target=process_audio, daemon=True)
        self.processing_thread.start()
    
    def stop_listening(self):
        if not self.is_listening:
            return
        
        self.is_listening = False
        self.stop_event.set()
        
        if hasattr(self, 'stop_listening_func'):
            self.stop_listening_func(wait_for_stop=False)
        
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
    
    def get_audio_level(self) -> float:
        try:
            with self.microphone as source:
                audio_data = self.recognizer.listen(source, timeout=0.1, phrase_time_limit=0.1)
                return min(100, max(0, (audio_data.frame_data.__len__() / 1000) * 10))
        except:
            return 0.0
