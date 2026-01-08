"""Enhanced J.A.R.V.I.S. - Main Application with GUI and Voice Activation.

This is the new main entry point with visual UI and wake word detection.
"""

import sys
import logging
import argparse
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow
from voice_activation.continuous_listener import ContinuousListener
from jarvis_core.assistant import JarvisAssistant
from voice_synthesis.aizen_voice import AizenVoice


class VoiceThread(QThread):
    """Thread for voice processing to keep UI responsive."""
    
    wake_word_detected = pyqtSignal()
    command_received = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.listener = None
        
    def run(self):
        """Run voice listener in thread."""
        self.listener = ContinuousListener()
        self.listener.set_wake_word_callback(self._on_wake_word)
        self.listener.start()
        
    def _on_wake_word(self):
        """Handle wake word detection."""
        self.wake_word_detected.emit()
        
    def stop(self):
        """Stop voice listener."""
        if self.listener:
            self.listener.stop()


class JarvisApp:
    """Main application controller."""
    
    def __init__(self, config_path="config.yaml"):
        """Initialize the application."""
        self.config_path = config_path
        
        # Qt Application
        self.qt_app = QApplication(sys.argv)
        
        # Main window
        self.window = MainWindow(config_path)
        
        # Voice system
        self.voice = AizenVoice(config_path)
        self.assistant = JarvisAssistant(config_path)
        
        # Voice thread
        self.voice_thread = None
        
        # Connect UI signals
        self._connect_signals()
        
        logging.info("J.A.R.V.I.S. initialized")
        
    def _connect_signals(self):
        """Connect UI signals to handlers."""
        # Will be implemented when voice thread is started
        pass
        
    def start(self):
        """Start the application."""
        logging.info("Starting J.A.R.V.I.S...")
        
        # Show window
        self.window.show()
        self.window.set_status("Ready")
        
        # Greeting
        self.voice.greeting()
        self.window.add_message("Aizen", "Indeed. How may I assist you?")
        
        # Start voice activation (optional)
        if input("\nStart voice activation? (y/n): ").lower() == 'y':
            self.start_voice_activation()
        
        # Run Qt event loop
        return self.qt_app.exec_()
        
    def start_voice_activation(self):
        """Start voice activation system."""
        logging.info("Starting voice activation...")
        
        self.voice_thread = VoiceThread()
        self.voice_thread.wake_word_detected.connect(self._on_wake_word)
        self.voice_thread.start()
        
        self.window.set_status("🎤 Listening for wake word...")
        self.window.add_message("System", "Voice activation enabled. Say 'Jarvis' to activate.")
        
    def _on_wake_word(self):
        """Handle wake word detection."""
        logging.info("Wake word detected!")
        
        self.window.set_listening(True)
        self.window.add_message("System", "Wake word detected!")
        
        # Play activation sound
        self.voice.speak("Yes?")
        
        # TODO: Start recording and transcribing user command
        # For now, just show the state
        self.window.set_listening(False)
        self.window.set_status("🎤 Listening for wake word...")
        
    def cleanup(self):
        """Cleanup resources."""
        if self.voice_thread:
            self.voice_thread.stop()
            self.voice_thread.wait()


def setup_logging(verbose: bool = False):
    """Set up logging."""
    level = logging.DEBUG if verbose else logging.INFO
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'jarvis_gui.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='J.A.R.V.I.S. with Bleach UI and Voice Activation'
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--no-ui',
        action='store_true',
        help='Run without GUI (text mode)'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting J.A.R.V.I.S.")
    
    try:
        if args.no_ui:
            # Fallback to text mode
            from main import main as text_main
            return text_main()
        else:
            # Run with GUI
            app = JarvisApp(config_path=args.config)
            exit_code = app.start()
            app.cleanup()
            return exit_code
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
