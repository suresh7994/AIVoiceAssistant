import subprocess
import threading
import queue
from typing import Optional, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextToSpeech:
    def __init__(self, rate: int = 175, volume: float = 0.9, voice: str = "Lekha"):
        self.rate = rate
        self.volume = volume
        self.voice = voice
        
        self.is_speaking = False
        self.speech_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.current_speech_stopped = threading.Event()
        self.current_process: Optional[subprocess.Popen] = None
        self.speaking_callback: Optional[Callable[[bool], None]] = None
        
        self._start_worker()
    
    def _start_worker(self):
        def worker():
            while not self.stop_event.is_set():
                try:
                    text = self.speech_queue.get(timeout=0.5)
                    if text is None:
                        break
                    
                    self.is_speaking = True
                    self.current_speech_stopped.clear()
                    
                    if self.speaking_callback:
                        self.speaking_callback(True)
                    
                    # Use macOS say command with rate adjustment and voice
                    rate_wpm = int(self.rate)
                    self.current_process = subprocess.Popen(
                        ['say', '-v', self.voice, '-r', str(rate_wpm), text],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    self.current_process.wait()
                    self.current_process = None
                    
                    self.is_speaking = False
                    self.current_speech_stopped.set()
                    
                    if self.speaking_callback:
                        self.speaking_callback(False)
                    
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"TTS error: {e}")
                    self.is_speaking = False
                    self.current_process = None
                    if self.speaking_callback:
                        self.speaking_callback(False)
        
        self.worker_thread = threading.Thread(target=worker, daemon=True)
        self.worker_thread.start()
    
    def speak(self, text: str):
        if text.strip():
            self.speech_queue.put(text)
    
    def stop_speaking(self):
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=1)
            except:
                try:
                    self.current_process.kill()
                except:
                    pass
            self.current_process = None
        
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
            except queue.Empty:
                break
        
        self.is_speaking = False
        self.current_speech_stopped.set()
    
    def set_speaking_callback(self, callback: Callable[[bool], None]):
        self.speaking_callback = callback
    
    def set_rate(self, rate: int):
        self.rate = rate
    
    def set_volume(self, volume: float):
        self.volume = volume
    
    def shutdown(self):
        self.stop_event.set()
        self.speech_queue.put(None)
        self.stop_speaking()
