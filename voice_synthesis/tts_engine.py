"""Text-to-Speech Engine with multiple backend support."""

import os
import logging
from pathlib import Path
from typing import Optional, Union
import yaml

logger = logging.getLogger(__name__)


class TTSEngine:
    """Text-to-Speech engine with voice cloning support."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize TTS engine.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.engine_name = self.config['voice']['engine']
        self.model = None
        self._initialize_engine()
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _initialize_engine(self):
        """Initialize the selected TTS engine."""
        logger.info(f"Initializing TTS engine: {self.engine_name}")
        
        if self.engine_name == "coqui_tts":
            self._init_coqui_tts()
        elif self.engine_name == "pyttsx3":
            self._init_pyttsx3()
        elif self.engine_name == "gtts":
            self._init_gtts()
        else:
            raise ValueError(f"Unknown TTS engine: {self.engine_name}")
    
    def _init_coqui_tts(self):
        """Initialize Coqui TTS with voice cloning."""
        try:
            from TTS.api import TTS
            
            model_name = self.config['voice']['voice_model']
            logger.info(f"Loading Coqui TTS model: {model_name}")
            
            self.model = TTS(model_name)
            logger.info("Coqui TTS initialized successfully")
            
        except ImportError:
            logger.error("Coqui TTS not installed. Install with: pip install TTS")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Coqui TTS: {e}")
            logger.info("Falling back to pyttsx3")
            self.engine_name = "pyttsx3"
            self._init_pyttsx3()
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 (offline TTS)."""
        try:
            import pyttsx3
            
            self.model = pyttsx3.init()
            
            # Configure voice properties
            rate = self.model.getProperty('rate')
            self.model.setProperty('rate', rate * self.config['voice']['speed'])
            
            # Try to set a deeper voice (male voice)
            voices = self.model.getProperty('voices')
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                    self.model.setProperty('voice', voice.id)
                    break
            
            logger.info("pyttsx3 initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize pyttsx3: {e}")
            raise
    
    def _init_gtts(self):
        """Initialize Google TTS (requires internet)."""
        try:
            from gtts import gTTS
            logger.info("gTTS initialized successfully")
            # gTTS is stateless, no model to load
            
        except ImportError:
            logger.error("gTTS not installed. Install with: pip install gtts")
            raise
    
    def speak(self, text: str, reference_audio: Optional[str] = None) -> None:
        """Synthesize and play speech.
        
        Args:
            text: Text to speak
            reference_audio: Path to reference audio for voice cloning (Coqui TTS only)
        """
        logger.info(f"Speaking: {text[:50]}...")
        
        if self.engine_name == "coqui_tts":
            self._speak_coqui(text, reference_audio)
        elif self.engine_name == "pyttsx3":
            self._speak_pyttsx3(text)
        elif self.engine_name == "gtts":
            self._speak_gtts(text)
    
    def _speak_coqui(self, text: str, reference_audio: Optional[str] = None):
        """Speak using Coqui TTS with voice cloning."""
        # Use reference audio from config if not provided
        if reference_audio is None:
            reference_audio = self.config['voice'].get('reference_audio')
        
        # Create cache directory if it doesn't exist
        cache_dir = Path(self.config['paths']['cache'])
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = cache_dir / "temp_speech.wav"
        
        try:
            if reference_audio and os.path.exists(reference_audio):
                # Voice cloning mode
                logger.info(f"Using voice cloning with reference: {reference_audio}")
                self.model.tts_to_file(
                    text=text,
                    speaker_wav=reference_audio,
                    file_path=str(output_file),
                    language=self.config['voice']['language']
                )
            else:
                # Standard TTS mode
                logger.warning("No reference audio found, using default voice")
                self.model.tts_to_file(
                    text=text,
                    file_path=str(output_file)
                )
            
            # Play the audio file
            self._play_audio(str(output_file))
            
        except Exception as e:
            logger.error(f"Error in Coqui TTS: {e}")
            raise
    
    def _speak_pyttsx3(self, text: str):
        """Speak using pyttsx3."""
        try:
            self.model.say(text)
            self.model.runAndWait()
        except Exception as e:
            logger.error(f"Error in pyttsx3: {e}")
            raise
    
    def _speak_gtts(self, text: str):
        """Speak using Google TTS."""
        try:
            from gtts import gTTS
            import pygame
            
            cache_dir = Path(self.config['paths']['cache'])
            cache_dir.mkdir(parents=True, exist_ok=True)
            output_file = cache_dir / "temp_speech.mp3"
            
            tts = gTTS(text=text, lang=self.config['voice']['language'])
            tts.save(str(output_file))
            
            self._play_audio(str(output_file))
            
        except Exception as e:
            logger.error(f"Error in gTTS: {e}")
            raise
    
    def _play_audio(self, file_path: str):
        """Play audio file.
        
        Args:
            file_path: Path to audio file
        """
        try:
            # Try pygame first (cross-platform)
            import pygame
            
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
        except ImportError:
            # Fallback to platform-specific players
            import platform
            import subprocess
            
            system = platform.system()
            
            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":  # macOS
                subprocess.call(["afplay", file_path])
            else:  # Linux
                subprocess.call(["aplay", file_path])
        
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
            logger.info(f"Audio saved to: {file_path}")
    
    def save_speech(self, text: str, output_path: str, reference_audio: Optional[str] = None):
        """Save synthesized speech to file.
        
        Args:
            text: Text to synthesize
            output_path: Path to save audio file
            reference_audio: Path to reference audio for voice cloning
        """
        logger.info(f"Saving speech to: {output_path}")
        
        if self.engine_name == "coqui_tts":
            if reference_audio is None:
                reference_audio = self.config['voice'].get('reference_audio')
            
            if reference_audio and os.path.exists(reference_audio):
                self.model.tts_to_file(
                    text=text,
                    speaker_wav=reference_audio,
                    file_path=output_path,
                    language=self.config['voice']['language']
                )
            else:
                self.model.tts_to_file(text=text, file_path=output_path)
                
        elif self.engine_name == "gtts":
            from gtts import gTTS
            tts = gTTS(text=text, lang=self.config['voice']['language'])
            tts.save(output_path)
            
        else:
            logger.warning(f"Save not supported for {self.engine_name}")


if __name__ == "__main__":
    # Test the TTS engine
    logging.basicConfig(level=logging.INFO)
    
    print("Testing TTS Engine...")
    tts = TTSEngine()
    tts.speak("All according to plan.")
