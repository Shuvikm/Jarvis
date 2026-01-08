"""Enhanced main application integrating all features."""

import sys
import logging
import argparse
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow
from voice_activation.continuous_listener import ContinuousListener
from jarvis_core.assistant import JarvisAssistant
from voice_synthesis.aizen_voice import AizenVoice

# Import new features
try:
    from ai_brain.ai_integration import AIBrain
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

try:
    from voice_activation.speech_recognition import WhisperRecognizer
    WHISPER_AVAILABLE = True
except:
    WHISPER_AVAILABLE = False


class EnhancedJarvisApp:
    """Enhanced J.A.R.V.I.S. with AI and voice recognition."""
    
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
        
        # AI brain (if available)
        if AI_AVAILABLE:
            self.ai_brain = AIBrain(config_path)
            logging.info("AI brain initialized")
        else:
            self.ai_brain = None
            
        # Voice recognition (if available)
        if WHISPER_AVAILABLE:
            self.speech_recognizer = WhisperRecognizer(config_path)
            logging.info("Speech recognizer initialized")
        else:
            self.speech_recognizer = None
        
        # Voice thread
        self.voice_thread = None
        
        # Connect signals
        self._connect_signals()
        
        logging.info("Enhanced J.A.R.V.I.S. initialized")
        
    def _connect_signals(self):
        """Connect UI signals to handlers."""
        # Button connections will be added here
        pass
        
    def start(self):
        """Start the application."""
        logging.info("Starting Enhanced J.A.R.V.I.S...")
        
        # Show window
        self.window.show()
        self.window.set_status("Ready")
        
        # Greeting
        self.voice.greeting()
        self.window.add_message("Aizen", "Yokoso watashino sekai e. Welcome to my world.")
        
        # Show available features
        features = []
        if AI_AVAILABLE:
            features.append("AI Brain")
        if WHISPER_AVAILABLE:
            features.append("Speech Recognition")
        
        if features:
            self.window.add_message("System", f"Available features: {', '.join(features)}")
        
        # Run Qt event loop
        return self.qt_app.exec_()
        
    def process_voice_command(self, text: str):
        """Process voice command with AI."""
        if self.ai_brain:
            response = self.ai_brain.get_response(text)
            self.voice.speak(response)
            self.window.add_message("You", text)
            self.window.add_message("Aizen", response)
        else:
            # Fallback to basic command processing
            result = self.assistant.process_text_input(text)
        
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
            logging.FileHandler(log_dir / 'jarvis_enhanced.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='J.A.R.V.I.S. Enhanced - AI Voice Assistant with Bleach UI'
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
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Enhanced J.A.R.V.I.S.")
    
    print("\n" + "="*60)
    print("🌙 J.A.R.V.I.S. Enhanced - Bleach Edition")
    print("="*60)
    print("\nFeatures:")
    print("  ✅ Bleach-themed UI with animations")
    print("  ✅ Aizen personality (Japanese/English)")
    print("  ✅ Voice synthesis")
    if AI_AVAILABLE:
        print("  ✅ AI-powered responses")
    if WHISPER_AVAILABLE:
        print("  ✅ Speech recognition")
    print("\n" + "="*60 + "\n")
    
    try:
        app = EnhancedJarvisApp(config_path=args.config)
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
