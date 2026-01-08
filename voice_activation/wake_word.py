"""Wake word detection using Porcupine."""

import struct
import logging
from typing import Callable, Optional
import yaml

try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False
    logging.warning("Porcupine not installed. Wake word detection unavailable.")

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    logging.warning("PyAudio not installed. Audio input unavailable.")

logger = logging.getLogger(__name__)


class WakeWordDetector:
    """Wake word detection for voice activation."""
    
    def __init__(self, config_path: str = "config.yaml", callback: Optional[Callable] = None):
        """Initialize wake word detector.
        
        Args:
            config_path: Path to configuration file
            callback: Function to call when wake word is detected
        """
        self.config = self._load_config(config_path)
        self.callback = callback
        self.porcupine = None
        self.audio_stream = None
        self.is_listening = False
        
        if not PORCUPINE_AVAILABLE:
            logger.error("Porcupine not available. Install with: pip install pvporcupine")
            return
            
        if not PYAUDIO_AVAILABLE:
            logger.error("PyAudio not available. Install with: pip install pyaudio")
            return
            
        self._initialize()
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except:
            return {
                'voice_activation': {
                    'wake_word': 'jarvis',
                    'sensitivity': 0.5
                },
                'audio': {
                    'sample_rate': 16000,
                    'channels': 1,
                    'chunk_size': 512
                }
            }
            
    def _initialize(self):
        """Initialize Porcupine."""
        try:
            wake_word = self.config['voice_activation']['wake_word']
            sensitivity = self.config['voice_activation']['sensitivity']
            
            # Create Porcupine instance
            # Built-in wake words: alexa, americano, blueberry, bumblebee,
            # computer, grapefruit, grasshopper, hey google, hey siri,
            # jarvis, ok google, picovoice, porcupine, terminator
            
            available_keywords = [
                'jarvis', 'computer', 'ok google', 'hey google', 'terminator',
                'picovoice', 'porcupine', 'alexa', 'americano', 'blueberry',
                'bumblebee', 'grapefruit', 'grasshopper', 'hey siri'
            ]
            
            if wake_word.lower() in available_keywords:
                keyword = wake_word.lower()
            else:
                logger.warning(f"Wake word '{wake_word}' not available. Using 'jarvis'")
                keyword = 'jarvis'
                
            self.porcupine = pvporcupine.create(
                keywords=[keyword],
                sensitivities=[sensitivity]
            )
            
            logger.info(f"Wake word detector initialized: '{keyword}' (sensitivity: {sensitivity})")
            
        except Exception as e:
            logger.error(f"Failed to initialize Porcupine: {e}")
            self.porcupine = None
            
    def start(self):
        """Start listening for wake word."""
        if not self.porcupine:
            logger.error("Porcupine not initialized")
            return False
            
        try:
            pa = pyaudio.PyAudio()
            
            self.audio_stream = pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            self.is_listening = True
            logger.info("Wake word detection started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start audio stream: {e}")
            return False
            
    def stop(self):
        """Stop listening."""
        self.is_listening = False
        
        if self.audio_stream:
            self.audio_stream.close()
            self.audio_stream = None
            
        logger.info("Wake word detection stopped")
        
    def listen(self) -> bool:
        """Listen for one frame and check for wake word.
        
        Returns:
            True if wake word detected, False otherwise
        """
        if not self.is_listening or not self.audio_stream:
            return False
            
        try:
            pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            
            keyword_index = self.porcupine.process(pcm)
            
            if keyword_index >= 0:
                logger.info("Wake word detected!")
                if self.callback:
                    self.callback()
                return True
                
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            
        return False
        
    def cleanup(self):
        """Cleanup resources."""
        self.stop()
        
        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None


if __name__ == "__main__":
    # Test wake word detection
    logging.basicConfig(level=logging.INFO)
    
    def on_wake_word():
        print("\n🎤 WAKE WORD DETECTED! 🎤\n")
        
    print("Testing wake word detection...")
    print("Say 'Jarvis' to activate")
    print("Press Ctrl+C to stop\n")
    
    detector = WakeWordDetector(callback=on_wake_word)
    detector.start()
    
    try:
        while True:
            detector.listen()
    except KeyboardInterrupt:
        print("\nStopping...")
        detector.cleanup()
