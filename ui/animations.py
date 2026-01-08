"""Bleach-style particle animation effects."""

import random
import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QRadialGradient
from .bleach_theme import COLORS, ANIMATION


class Particle:
    """Single reishi particle."""
    
    def __init__(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.size = random.uniform(2, 6)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.speed_y = random.uniform(-1, -0.2)  # Float upward
        self.alpha = random.uniform(0.3, 1.0)
        self.lifetime = random.uniform(0.5, 1.0)
        
    def update(self, width, height):
        """Update particle position."""
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 0.01
        
        # Wrap around edges
        if self.x < 0:
            self.x = width
        elif self.x > width:
            self.x = 0
            
        if self.y < 0:
            self.y = height
            
        # Reset if dead
        if self.lifetime <= 0:
            self.__init__(width, height)
            

class ParticleEffect(QWidget):
    """Floating reishi particles effect."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        self.particles = []
        self.enabled = True
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_particles)
        self.timer.start(30)  # ~33 FPS
        
    def set_enabled(self, enabled: bool):
        """Enable/disable particle effects."""
        self.enabled = enabled
        if enabled and not self.timer.isActive():
            self.timer.start()
        elif not enabled and self.timer.isActive():
            self.timer.stop()
            
    def resizeEvent(self, event):
        """Handle resize."""
        super().resizeEvent(event)
        self._init_particles()
        
    def _init_particles(self):
        """Initialize particles."""
        count = ANIMATION['particle_count']
        self.particles = [
            Particle(self.width(), self.height())
            for _ in range(count)
        ]
        
    def _update_particles(self):
        """Update and redraw particles."""
        if not self.particles:
            self._init_particles()
            
        for particle in self.particles:
            particle.update(self.width(), self.height())
            
        self.update()
        
    def paintEvent(self, event):
        """Draw particles."""
        if not self.enabled:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for particle in self.particles:
            # Create glow effect
            gradient = QRadialGradient(
                particle.x, particle.y, particle.size * 2
            )
            
            color_center = QColor(COLORS['spiritual_blue'])
            color_center.setAlphaF(particle.alpha * particle.lifetime)
            
            color_edge = QColor(COLORS['spiritual_glow'])
            color_edge.setAlphaF(0)
            
            gradient.setColorAt(0, color_center)
            gradient.setColorAt(1, color_edge)
            
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            
            painter.drawEllipse(
                QPointF(particle.x, particle.y),
                particle.size,
                particle.size
            )
