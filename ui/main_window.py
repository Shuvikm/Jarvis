"""Main GUI window with Bleach theme."""

import sys
import yaml
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap

from .bleach_theme import COLORS, FONTS, FONT_SIZES, QT_STYLESHEET
from .voice_visualizer import VoiceVisualizer
from .animations import ParticleEffect


class MainWindow(QMainWindow):
    """Main J.A.R.V.I.S. window with Bleach theme."""
    
    # Signals
    voice_command_signal = pyqtSignal(str)
    
    def __init__(self, config_path="config.yaml"):
        super().__init__()
        
        # Load config
        self.config = self._load_config(config_path)
        
        # Window setup
        self.init_ui()
        
        # System tray
        if self.config['service']['system_tray']:
            self.init_tray()
            
    def _load_config(self, config_path):
        """Load configuration."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except:
            # Default config
            return {
                'ui': {
                    'window_size': [450, 700],
                    'always_on_top': False,
                    'opacity': 0.95,
                    'animations_enabled': True,
                    'particle_effects': True
                },
                'service': {
                    'system_tray': True,
                    'minimize_to_tray': True
                }
            }
            
    def init_ui(self):
        """Initialize the user interface."""
        # Window properties
        ui_config = self.config.get('ui', {})
        width, height = ui_config.get('window_size', [450, 700])
        
        self.setWindowTitle("J.A.R.V.I.S. - Aizen")
        self.setGeometry(100, 100, width, height)
        
        # Always on top
        if ui_config.get('always_on_top', False):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            
        # Opacity
        self.setWindowOpacity(ui_config.get('opacity', 0.95))
        
        # Apply stylesheet
        self.setStyleSheet(QT_STYLESHEET)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)
        
        # Avatar section
        self.avatar_label = self._create_avatar()
        main_layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)
        
        # Voice visualizer
        self.visualizer = VoiceVisualizer()
        main_layout.addWidget(self.visualizer)
        
        # Status label
        self.status_label = QLabel("Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"font-size: {FONT_SIZES['small']}px; color: {COLORS['accent_gray']};")
        main_layout.addWidget(self.status_label)
        
        # Conversation display
        self.conversation_text = QTextEdit()
        self.conversation_text.setReadOnly(True)
        self.conversation_text.setPlaceholderText("Conversation will appear here...")
        main_layout.addWidget(self.conversation_text)
        
        # Control buttons
        button_layout = self._create_buttons()
        main_layout.addLayout(button_layout)
        
        # Particle effect overlay (if enabled)
        if ui_config.get('particle_effects', True):
            self.particle_effect = ParticleEffect(central_widget)
            self.particle_effect.setGeometry(central_widget.rect())
            self.particle_effect.raise_()
            
    def _create_header(self):
        """Create header with title."""
        layout = QHBoxLayout()
        
        title = QLabel("J.A.R.V.I.S.")
        title.setStyleSheet(f"""
            font-size: {FONT_SIZES['title']}px;
            font-weight: bold;
            color: {COLORS['spiritual_blue']};
        """)
        
        subtitle = QLabel("Aizen Protocol")
        subtitle.setStyleSheet(f"""
            font-size: {FONT_SIZES['small']}px;
            color: {COLORS['accent_gray']};
        """)
        
        title_layout = QVBoxLayout()
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        return layout
        
    def _create_avatar(self):
        """Create avatar/logo section."""
        avatar = QLabel("⚡")  # Placeholder - replace with actual image
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(f"""
            font-size: 80px;
            color: {COLORS['spiritual_blue']};
            padding: 20px;
        """)
        return avatar
        
    def _create_buttons(self):
        """Create control buttons."""
        layout = QHBoxLayout()
        
        self.listen_btn = QPushButton("🎤 Listen")
        self.listen_btn.clicked.connect(self.toggle_listening)
        
        self.settings_btn = QPushButton("⚙ Settings")
        self.settings_btn.clicked.connect(self.show_settings)
        
        layout.addWidget(self.listen_btn)
        layout.addWidget(self.settings_btn)
        
        return layout
        
    def init_tray(self):
        """Initialize system tray icon."""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Use default icon - replace with custom icon later
        self.tray_icon.setIcon(self.style().standardIcon(self.style().SP_ComputerIcon))
        
        # Tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide)
        
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
        
    def tray_icon_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()
                
    def closeEvent(self, event):
        """Handle window close."""
        if self.config['service'].get('minimize_to_tray', True) and hasattr(self, 'tray_icon'):
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "J.A.R.V.I.S.",
                "Running in background. Double-click to restore.",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            event.accept()
            
    def resizeEvent(self, event):
        """Handle resize."""
        super().resizeEvent(event)
        if hasattr(self, 'particle_effect'):
            self.particle_effect.setGeometry(self.centralWidget().rect())
            
    # Public methods for external control
    
    def set_status(self, status: str):
        """Update status label."""
        self.status_label.setText(status)
        
    def set_listening(self, listening: bool):
        """Update listening state."""
        self.visualizer.set_listening(listening)
        if listening:
            self.status_label.setText("🎤 Listening...")
            self.status_label.setStyleSheet(f"color: {COLORS['listening']};")
        else:
            self.status_label.setText("Idle")
            self.status_label.setStyleSheet(f"color: {COLORS['accent_gray']};")
            
    def set_speaking(self, speaking: bool):
        """Update speaking state."""
        self.visualizer.set_speaking(speaking)
        if speaking:
            self.status_label.setText("💬 Speaking...")
            self.status_label.setStyleSheet(f"color: {COLORS['spiritual_blue']};")
            
    def update_audio_level(self, level: float):
        """Update audio visualization."""
        self.visualizer.set_audio_level(level)
        
    def add_message(self, sender: str, message: str):
        """Add message to conversation."""
        if sender.lower() == "you":
            color = COLORS['accent_white']
        else:
            color = COLORS['spiritual_blue']
            
        html = f'<p style="color: {color};"><b>{sender}:</b> {message}</p>'
        self.conversation_text.append(html)
        
    def toggle_listening(self):
        """Toggle listening state."""
        # This will be connected to the voice system
        pass
        
    def show_settings(self):
        """Show settings dialog."""
        # TODO: Implement settings dialog
        pass


def main():
    """Test the UI."""
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    # Demo updates
    import time
    def demo():
        window.add_message("You", "Hello")
        time.sleep(0.5)
        window.add_message("Aizen", "Indeed. How may I assist you?")
        
    QTimer.singleShot(1000, demo)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
