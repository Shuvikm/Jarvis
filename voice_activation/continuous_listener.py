"""Continuous listening service for voice activation."""

import logging
import threading
import time
from typing import Callable, Optional
import yaml

from .wake_word import WakeWordDetector

logger = logging.getLogger(__name__)


class ContinuousListener:
    """Always-on listening service with wake word activation."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize continuous listener.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.wake_word_detector = None
        self.is_running = False
        self.listen_thread = None
        
        # Callbacks
        self.on_wake_word = None
        self.on_command_received = None
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except:
            return {}
            
    def set_wake_word_callback(self, callback: Callable):
        """Set callback for wake word detection."""
        self.on_wake_word = callback
        
    def set_command_callback(self, callback: Callable):
        """Set callback for voice command."""
        self.on_command_received = callback
        
    def start(self) -> bool:
        """Start continuous listening."""
        if self.is_running:
            logger.warning("Listener already running")
            return False
            
        # Initialize wake word detector
        self.wake_word_detector = WakeWordDetector(
            callback=self._handle_wake_word
        )
        
        if not self.wake_word_detector.start():
            logger.error("Failed to start wake word detector")
            return False
            
        # Start listening thread
        self.is_running = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        logger.info("Continuous listener started")
        return True
        
    def stop(self):
        """Stop continuous listening."""
        self.is_running = False
        
        if self.wake_word_detector:
            self.wake_word_detector.cleanup()
            self.wake_word_detector = None
            
        if self.listen_thread:
            self.listen_thread.join(timeout=2.0)
            self.listen_thread = None
            
        logger.info("Continuous listener stopped")
        
    def _listen_loop(self):
        """Main listening loop (runs in thread)."""
        logger.info("Listening loop started")
        
        while self.is_running:
            try:
                # Check for wake word
                if self.wake_word_detector:
                    self.wake_word_detector.listen()
                    
                # Small sleep to prevent CPU spinning
                time.sleep(0.01)
                
            except Exception as e:
                logger.error(f"Error in listen loop: {e}")
                time.sleep(0.1)
                
        logger.info("Listening loop stopped")
        
    def _handle_wake_word(self):
        """Handle wake word detection."""
        logger.info("Wake word callback triggered")
        
        if self.on_wake_word:
            self.on_wake_word()
            
        # TODO: Record and transcribe the following command
        # For now, just trigger the callback
        
    def __del__(self):
        """Cleanup on deletion."""
        self.stop()
