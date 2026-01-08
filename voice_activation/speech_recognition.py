"""Speech recognition using OpenAI Whisper for offline, accurate transcription."""

import logging
import numpy as np
from typing import Optional
import yaml

logger = logging.getLogger(__name__)

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logger.warning("Whisper not installed. Install with: pip install openai-whisper")

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    logger.warning("sounddevice not installed. Install with: pip install sounddevice")


class WhisperRecognizer:
    """Speech-to-text using OpenAI Whisper."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize Whisper recognizer."""
        self.config = self._load_config(config_path)
        self.model = None
        self.sample_rate = 16000
        
        if WHISPER_AVAILABLE:
            self._load_model()
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except:
            return {
                'speech_recognition': {
                    'model_size': 'base',
                    'language': 'en'
                }
            }
    
    def _load_model(self):
        """Load Whisper model."""
        try:
            model_size = self.config.get('speech_recognition', {}).get('model_size', 'base')
            logger.info(f"Loading Whisper model: {model_size}")
            self.model = whisper.load_model(model_size)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
    
    def record_audio(self, duration: int = 5) -> Optional[np.ndarray]:
        """Record audio from microphone.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Audio data as numpy array
        """
        if not SOUNDDEVICE_AVAILABLE:
            logger.error("sounddevice not available")
            return None
        
        try:
            logger.info(f"Recording for {duration} seconds...")
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )
            sd.wait()
            logger.info("Recording complete")
            return audio.flatten()
        except Exception as e:
            logger.error(f"Recording failed: {e}")
            return None
    
    def transcribe(self, audio: np.ndarray, language: str = 'en') -> Optional[str]:
        """Transcribe audio to text.
        
        Args:
            audio: Audio data
            language: Language code
            
        Returns:
            Transcribed text
        """
        if not WHISPER_AVAILABLE or self.model is None:
            logger.error("Whisper not available")
            return None
        
        try:
            logger.info("Transcribing audio...")
            result = self.model.transcribe(
                audio,
                language=language,
                fp16=False
            )
            text = result['text'].strip()
            logger.info(f"Transcription: {text}")
            return text
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return None
    
    def listen_and_transcribe(self, duration: int = 5, language: str = 'en') -> Optional[str]:
        """Record audio and transcribe in one step.
        
        Args:
            duration: Recording duration
            language: Language code
            
        Returns:
            Transcribed text
        """
        audio = self.record_audio(duration)
        if audio is None:
            return None
        
        return self.transcribe(audio, language)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\nTesting Whisper Speech Recognition...")
    
    if not WHISPER_AVAILABLE:
        print("❌ Whisper not installed")
        print("Install with: pip install openai-whisper")
    elif not SOUNDDEVICE_AVAILABLE:
        print("❌ sounddevice not installed")
        print("Install with: pip install sounddevice")
    else:
        recognizer = WhisperRecognizer()
        print("\n🎤 Speak now (5 seconds)...")
        text = recognizer.listen_and_transcribe(5)
        
        if text:
            print(f"\n✅ You said: {text}")
        else:
            print("\n❌ Failed to transcribe")
