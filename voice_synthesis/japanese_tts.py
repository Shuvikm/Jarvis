"""Enhanced TTS engine with Japanese language support."""

import os
import logging
from pathlib import Path
from typing import Optional
import yaml
import re

logger = logging.getLogger(__name__)


class JapaneseTTSEngine:
    """TTS engine with Japanese pronunciation support."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize TTS engine with Japanese support."""
        self.config = self._load_config(config_path)
        self.engine_name = self.config['voice']['engine']
        self.model = None
        self._initialize_engine()
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except:
            return {'voice': {'engine': 'pyttsx3', 'speed': 1.0}, 'paths': {'cache': 'cache'}}
    
    def _initialize_engine(self):
        """Initialize the selected TTS engine."""
        logger.info(f"Initializing TTS engine: {self.engine_name}")
        
        if self.engine_name == "gtts":
            self._init_gtts()
        elif self.engine_name == "pyttsx3":
            self._init_pyttsx3()
        else:
            logger.warning(f"Unknown engine {self.engine_name}, using pyttsx3")
            self._init_pyttsx3()
    
    def _init_gtts(self):
        """Initialize Google TTS."""
        try:
            from gtts import gTTS
            logger.info("gTTS initialized successfully")
        except ImportError:
            logger.error("gTTS not installed. Install with: pip install gtts")
            raise
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3."""
        try:
            import pyttsx3
            self.model = pyttsx3.init()
            rate = self.model.getProperty('rate')
            self.model.setProperty('rate', rate * self.config['voice']['speed'])
            
            voices = self.model.getProperty('voices')
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                    self.model.setProperty('voice', voice.id)
                    break
            
            logger.info("pyttsx3 initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize pyttsx3: {e}")
            raise
    
    def speak(self, text: str):
        """Speak text with Japanese pronunciation support."""
        # Detect Japanese words
        has_japanese = bool(re.search(r'[ぁ-んァ-ン一-龯]', text))
        
        if has_japanese or self._has_romaji(text):
            logger.info("Detected Japanese text, using specialized pronunciation")
            self._speak_mixed_language(text)
        else:
            self._speak_basic(text)
    
    def _has_romaji(self, text: str) -> bool:
        """Check if text contains common Japanese romanji phrases."""
        japanese_words = [
            'yokoso', 'watashino', 'sekai', 'keikaku', 'doori',
            'naruhodo', 'omoshiroi', 'masaka', 'kanpeki', 'muda',
            'sayonara', 'mata', 'sou ka'
        ]
        text_lower = text.lower()
        return any(word in text_lower for word in japanese_words)
    
    def _speak_mixed_language(self, text: str):
        """Speak text with mixed Japanese/English."""
        if self.engine_name == "gtts":
            self._speak_gtts_japanese(text)
        else:
            # Fallback to basic
            self._speak_basic(text)
    
    def _speak_gtts_japanese(self, text: str):
        """Use gTTS with Japanese language for Japanese words."""
        from gtts import gTTS
        import pygame
        
        cache_dir = Path(self.config['paths']['cache'])
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Split into segments
        segments = self._split_japanese_english(text)
        
        for i, (segment_text, lang) in enumerate(segments):
            output_file = cache_dir / f"temp_speech_{i}.mp3"
            
            tts = gTTS(text=segment_text, lang=lang, slow=False)
            tts.save(str(output_file))
            
            # Play
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(str(output_file))
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except:
                logger.warning(f"Could not play {output_file}")
    
    def _split_japanese_english(self, text: str):
        """Split text into Japanese and English segments."""
        # Simple approach: detect common Japanese romaji
        japanese_phrases = {
            'yokoso watashino sekai e': 'ja',
            'yokoso watashino': 'ja',
            'yokoso': 'ja',
            'keikaku doori': 'ja',
            'naruhodo': 'ja',
            'omoshiroi': 'ja',
            'masaka': 'ja',
            'kanpeki': 'ja',
            'muda da': 'ja',
            'sayonara': 'ja',
            'mata ne': 'ja',
            'sou ka': 'ja'
        }
        
        segments = []
        remaining = text
        
        for jp_phrase, lang in japanese_phrases.items():
            if jp_phrase in remaining.lower():
                # Split at this phrase
                idx = remaining.lower().find(jp_phrase)
                
                # Add English before
                if idx > 0:
                    segments.append((remaining[:idx].strip(), 'en'))
                
                # Add Japanese
                actual_phrase = remaining[idx:idx+len(jp_phrase)]
                segments.append((actual_phrase, 'ja'))
                
                remaining = remaining[idx+len(jp_phrase):]
        
        # Add any remaining English
        if remaining.strip():
            segments.append((remaining.strip(), 'en'))
        
        # If no Japanese detected, return as English
        if not segments:
            segments = [(text, 'en')]
        
        return segments
    
    def _speak_basic(self, text: str):
        """Basic speech without Japanese support."""
        if self.engine_name == "pyttsx3":
            self.model.say(text)
            self.model.runAndWait()
        elif self.engine_name == "gtts":
            from gtts import gTTS
            import pygame
            
            cache_dir = Path(self.config['paths']['cache'])
            cache_dir.mkdir(parents=True, exist_ok=True)
            output_file = cache_dir / "temp_speech.mp3"
            
            tts = gTTS(text=text, lang='en')
            tts.save(str(output_file))
            
            pygame.mixer.init()
            pygame.mixer.music.load(str(output_file))
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\nTesting Japanese TTS...")
    
    # Test with Japanese phrases
    tts = JapaneseTTSEngine()
    tts.speak("Yokoso watashino sekai e. Welcome to my world.")
