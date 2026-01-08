"""Aizen personality voice module for J.A.R.V.I.S."""

import logging
from typing import Optional
from .tts_engine import TTSEngine

logger = logging.getLogger(__name__)


class AizenVoice:
    """Aizen-themed voice interface with personality."""
    
    # Aizen's signature phrases and speaking patterns
    SIGNATURE_PHRASES = {
        'greeting': [
            "Yokoso... watashino sekai e. Welcome to my world.",
            "Yokoso. How may I assist you?",
            "Indeed. You have my attention.",
            "Welcome to Soul Society... or rather, my domain.",
            "Yokoso watashino... You've arrived."
        ],
        'acknowledgement': [
            "All according to plan.",
            "Keikaku doori... Precisely as expected.",
            "I see.",
            "Understood.",
            "Naruhodo... Interesting."
        ],
        'thinking': [
            "Interesting...",
            "Omoshiroi... How fascinating...",
            "Let me consider this.",
            "Sou ka... I see..."
        ],
        'error': [
            "That is... unfortunate.",
            "Masaka... An unexpected development.",
            "This requires reconsideration."
        ],
        'success': [
            "Exactly as I foresaw.",
            "Kanpeki... Perfect.",
            "Flawless execution.",
            "Just as planned... keikaku doori."
        ],
        'denial': [
            "That is irrelevant.",
            "Muda da... Futile.",
            "I have no interest in such matters."
        ],
        'goodbye': [
            "Sayonara... Until next time.",
            "Our conversation is concluded.",
            "Mata ne... You may go.",
            "Farewell."
        ]
    }
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize Aizen voice.
        
        Args:
            config_path: Path to configuration file
        """
        self.tts_engine = TTSEngine(config_path)
        logger.info("Aizen voice module initialized")
    
    def speak(self, text: str, emotion: Optional[str] = None):
        """Speak with Aizen's voice and personality.
        
        Args:
            text: Text to speak
            emotion: Optional emotion/context (greeting, acknowledgement, etc.)
        """
        # Add Aizen's speaking style
        formatted_text = self._add_aizen_style(text, emotion)
        
        logger.info(f"Aizen speaking: {formatted_text}")
        self.tts_engine.speak(formatted_text)
    
    def _add_aizen_style(self, text: str, emotion: Optional[str] = None) -> str:
        """Add Aizen's speaking style to text.
        
        Args:
            text: Original text
            emotion: Emotion context
            
        Returns:
            Formatted text with Aizen's style
        """
        # Aizen speaks calmly and deliberately, with strategic pauses
        # Add subtle pauses for dramatic effect
        
        # If the text is very short, keep it as is
        if len(text.split()) <= 3:
            return text
        
        # Add strategic pauses (represented by commas)
        # Aizen tends to pause before important words
        words = text.split()
        
        # Don't modify if already has good punctuation
        if ',' in text or '...' in text:
            return text
        
        # For longer statements, add a pause in the middle
        if len(words) > 8:
            mid_point = len(words) // 2
            words.insert(mid_point, "...")
            return ' '.join(words)
        
        return text
    
    def greeting(self):
        """Greet the user in Aizen's style."""
        import random
        phrase = random.choice(self.SIGNATURE_PHRASES['greeting'])
        self.speak(phrase, emotion='greeting')
    
    def acknowledge(self, custom_text: Optional[str] = None):
        """Acknowledge a command or statement.
        
        Args:
            custom_text: Custom acknowledgement text
        """
        import random
        
        if custom_text:
            self.speak(custom_text, emotion='acknowledgement')
        else:
            phrase = random.choice(self.SIGNATURE_PHRASES['acknowledgement'])
            self.speak(phrase, emotion='acknowledgement')
    
    def think(self):
        """Express contemplation."""
        import random
        phrase = random.choice(self.SIGNATURE_PHRASES['thinking'])
        self.speak(phrase, emotion='thinking')
    
    def error(self, custom_text: Optional[str] = None):
        """Express an error or unexpected situation.
        
        Args:
            custom_text: Custom error message
        """
        import random
        
        if custom_text:
            self.speak(f"Hmm. {custom_text}", emotion='error')
        else:
            phrase = random.choice(self.SIGNATURE_PHRASES['error'])
            self.speak(phrase, emotion='error')
    
    def success(self, custom_text: Optional[str] = None):
        """Express success.
        
        Args:
            custom_text: Custom success message
        """
        import random
        
        if custom_text:
            self.speak(custom_text, emotion='success')
        else:
            phrase = random.choice(self.SIGNATURE_PHRASES['success'])
            self.speak(phrase, emotion='success')
    
    def deny(self):
        """Deny or dismiss something."""
        import random
        phrase = random.choice(self.SIGNATURE_PHRASES['denial'])
        self.speak(phrase, emotion='denial')
    
    def goodbye(self):
        """Say goodbye."""
        import random
        phrase = random.choice(self.SIGNATURE_PHRASES['goodbye'])
        self.speak(phrase, emotion='goodbye')
    
    def respond_to_query(self, answer: str, confidence: float = 1.0):
        """Respond to a user query with an answer.
        
        Args:
            answer: The answer to speak
            confidence: Confidence in the answer (0.0 to 1.0)
        """
        if confidence < 0.5:
            # Low confidence - Aizen would be cautious
            response = f"Perhaps... {answer}"
        elif confidence < 0.8:
            # Medium confidence
            response = answer
        else:
            # High confidence - Aizen is certain
            response = answer
        
        self.speak(response)
    
    def respond_with_personality(self, base_response: str, context: str = "neutral") -> str:
        """Add Aizen's personality to a response.
        
        Args:
            base_response: Base response text
            context: Context (time, weather, knowledge, etc.)
            
        Returns:
            Response with Aizen's personality
        """
        # Customize responses based on context
        if context == "time":
            # Aizen finds time questions somewhat beneath him but answers anyway
            return base_response
        
        elif context == "weather":
            # Aizen sees weather as a mundane topic
            return f"{base_response} Such matters are of little consequence."
        
        elif context == "knowledge":
            # Aizen enjoys displaying knowledge
            return f"Naturally. {base_response}"
        
        elif context == "task_complete":
            # Task completion
            return f"{base_response} All according to plan."
        
        else:
            return base_response


if __name__ == "__main__":
    # Test Aizen voice
    logging.basicConfig(level=logging.INFO)
    
    print("Testing Aizen Voice Module...")
    aizen = AizenVoice()
    
    print("\n1. Greeting...")
    aizen.greeting()
    
    print("\n2. Acknowledgement...")
    aizen.acknowledge()
    
    print("\n3. Thinking...")
    aizen.think()
    
    print("\n4. Custom response...")
    aizen.speak("All is proceeding exactly as I have foreseen.")
