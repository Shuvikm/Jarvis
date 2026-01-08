"""Voice waveform visualizer with Bleach spiritual energy effects."""

import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QRadialGradient
from .bleach_theme import COLORS, ANIMATION


class VoiceVisualizer(QWidget):
    """Real-time voice waveform visualizer with Bleach theme."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        
        # Audio data
        self.audio_levels = [0.0] * 50
        self.is_listening = False
        self.is_speaking = False
        
        # Animation
        self.animation_offset = 0
        self.pulse_value = 0
        
        # Timer for animation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._animate)
        self.animation_timer.start(30)  # ~33 FPS
        
    def set_audio_level(self, level: float):
        """Update audio level (0.0 to 1.0)."""
        self.audio_levels.pop(0)
        self.audio_levels.append(min(1.0, max(0.0, level)))
        
    def set_listening(self, listening: bool):
        """Set listening state."""
        self.is_listening = listening
        
    def set_speaking(self, speaking: bool):
        """Set speaking state."""
        self.is_speaking = speaking
        
    def _animate(self):
        """Update animation."""
        self.animation_offset = (self.animation_offset + 2) % 360
        self.pulse_value = (self.pulse_value + 0.05) % (2 * np.pi)
        self.update()
        
    def paintEvent(self, event):
        """Draw the waveform."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_y = height // 2
        
        # Background
        painter.fillRect(0, 0, width, height, QColor(COLORS['bg_secondary']))
        
        if self.is_listening:
            self._draw_listening_effect(painter, width, height, center_y)
        elif self.is_speaking:
            self._draw_speaking_effect(painter, width, height, center_y)
        else:
            self._draw_idle_effect(painter, width, height, center_y)
            
    def _draw_listening_effect(self, painter, width, height, center_y):
        """Draw listening visualization."""
        # Pulsing circle in center
        pulse_size = int(30 + 10 * np.sin(self.pulse_value))
        
        # Glow effect
        gradient = QRadialGradient(width // 2, center_y, pulse_size)
        gradient.setColorAt(0, QColor(COLORS['listening']))
        gradient.setColorAt(0.5, QColor(0, 0, 255, 100))
        gradient.setColorAt(1, QColor(0, 0, 255, 0))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            int(width // 2 - pulse_size),
            int(center_y - pulse_size),
            int(pulse_size * 2),
            int(pulse_size * 2)
        )
        
        # Waveform
        self._draw_waveform(painter, width, height, center_y, QColor(COLORS['listening']))
        
    def _draw_speaking_effect(self, painter, width, height, center_y):
        """Draw speaking visualization."""
        self._draw_waveform(painter, width, height, center_y, QColor(COLORS['spiritual_blue']))
        
    def _draw_idle_effect(self, painter, width, height, center_y):
        """Draw idle visualization."""
        # Flat line with subtle pulse
        pen = QPen(QColor(COLORS['spiritual_dark']))
        pen.setWidth(2)
        painter.setPen(pen)
        
        y_offset = int(5 * np.sin(self.pulse_value))
        painter.drawLine(0, int(center_y + y_offset), int(width), int(center_y + y_offset))
        
    def _draw_waveform(self, painter, width, height, center_y, color):
        """Draw actual waveform from audio levels."""
        pen = QPen(color)
        pen.setWidth(3)
        painter.setPen(pen)
        
        # Draw bars
        bar_width = width / len(self.audio_levels)
        
        for i, level in enumerate(self.audio_levels):
            x = int(i * bar_width)
            bar_height = int(level * (height - 40))
            
            # Draw bar from center
            painter.drawLine(
                int(x + bar_width / 2),
                int(center_y - bar_height / 2),
                int(x + bar_width / 2),
                int(center_y + bar_height / 2)
            )
