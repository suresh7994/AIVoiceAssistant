import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
import math
import random


class SignalEmitter(QObject):
    status_changed = pyqtSignal(str)
    response_chunk = pyqtSignal(str)


class WaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.bars = []
        self.num_bars = 40
        self.is_active = False
        self.animation_offset = 0
        
        for i in range(self.num_bars):
            self.bars.append(random.uniform(0.2, 0.4))
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)
    
    def set_active(self, active: bool):
        self.is_active = active
    
    def update_animation(self):
        if self.is_active:
            self.animation_offset += 0.2
            for i in range(self.num_bars):
                target = abs(math.sin((i + self.animation_offset) * 0.3)) * 0.8 + 0.2
                self.bars[i] += (target - self.bars[i]) * 0.3
        else:
            for i in range(self.num_bars):
                self.bars[i] += (0.1 - self.bars[i]) * 0.1
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        bar_width = width / self.num_bars
        
        for i, amplitude in enumerate(self.bars):
            x = i * bar_width
            bar_height = height * amplitude
            y = (height - bar_height) / 2
            
            if self.is_active:
                color = QColor(100, 150, 255)
            else:
                color = QColor(80, 80, 100)
            
            painter.fillRect(int(x + bar_width * 0.2), int(y), 
                           int(bar_width * 0.6), int(bar_height), color)


class VoiceAgentUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals = SignalEmitter()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Voice AI Agent")
        self.setGeometry(100, 100, 600, 500)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 30px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
            QPushButton#micButton {
                background-color: #4a90e2;
            }
            QPushButton#micButton:hover {
                background-color: #5a9ff2;
            }
            QPushButton#micButton:pressed {
                background-color: #3a80d2;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        title_label = QLabel("AI Voice Assistant")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        layout.addWidget(title_label)
        
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 18))
        self.status_label.setStyleSheet("color: #888888;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.mic_button = QPushButton("🎤 Start Listening")
        self.mic_button.setObjectName("micButton")
        self.mic_button.setMinimumSize(200, 60)
        self.mic_button.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(self.mic_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
        
        self.signals.status_changed.connect(self.update_status)
    
    def update_status(self, status: str):
        self.status_label.setText(status)
        
        if status == "Listening...":
            self.status_label.setStyleSheet("color: #4a90e2;")
            self.waveform.set_active(True)
            self.mic_button.setText("🔴 Stop Listening")
        elif status == "Thinking...":
            self.status_label.setStyleSheet("color: #f5a623;")
            self.waveform.set_active(False)
        elif status == "Speaking...":
            self.status_label.setStyleSheet("color: #7ed321;")
            self.waveform.set_active(True)
        else:
            self.status_label.setStyleSheet("color: #888888;")
            self.waveform.set_active(False)
            self.mic_button.setText("🎤 Start Listening")
    
    def set_mic_callback(self, callback):
        self.mic_button.clicked.connect(callback)
    
    def get_signals(self):
        return self.signals
    
    def closeEvent(self, event):
        event.accept()


def create_app():
    app = QApplication(sys.argv)
    ui = VoiceAgentUI()
    return app, ui
