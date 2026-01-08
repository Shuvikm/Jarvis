"""Main J.A.R.V.I.S. Assistant with Aizen voice."""

import logging
import yaml
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from voice_synthesis.aizen_voice import AizenVoice
from jarvis_core.commands import CommandProcessor

logger = logging.getLogger(__name__)


class JarvisAssistant:
    """Main J.A.R.V.I.S. Assistant with Aizen personality."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize J.A.R.V.I.S.
        
        Args:
            config_path: Path to configuration file
        """
        logger.info("Initializing J.A.R.V.I.S. Assistant...")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize voice (Aizen)
        self.voice = AizenVoice(config_path)
        
        # Initialize command processor
        self.commands = CommandProcessor()
        
        # State
        self.running = False
        self.conversation_context = []
        
        logger.info("J.A.R.V.I.S. Assistant initialized successfully")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
    
    def start(self):
        """Start the assistant."""
        logger.info("Starting J.A.R.V.I.S...")
        self.running = True
        
        # Greet the user
        self.voice.greeting()
        
        print("\n" + "="*50)
        print("J.A.R.V.I.S. with Aizen Voice - ACTIVE")
        print("="*50)
        print("\nType 'exit' or 'quit' to stop.")
        print("Type 'help' for available commands.\n")
    
    def stop(self):
        """Stop the assistant."""
        logger.info("Stopping J.A.R.V.I.S...")
        self.running = False
        self.voice.goodbye()
    
    def process_text_input(self, text: str) -> bool:
        """Process text input from user.
        
        Args:
            text: User input text
            
        Returns:
            True to continue, False to exit
        """
        if not text.strip():
            return True
        
        # Process the command
        result = self.commands.process(text)
        
        if result['success']:
            response_data = result['response']
            response_text = response_data['text']
            context = response_data.get('context', 'neutral')
            
            # Add Aizen's personality to the response
            personalized_response = self.voice.respond_with_personality(
                response_text, 
                context
            )
            
            # Speak the response
            self.voice.speak(personalized_response)
            
            # Print to console
            print(f"\nAizen: {personalized_response}\n")
            
            # Check if should exit
            if response_data.get('exit', False):
                return False
        else:
            # Command not recognized
            self.voice.speak(result['response'])
            print(f"\nAizen: {result['response']}\n")
        
        # Add to conversation context
        self.conversation_context.append({
            'input': text,
            'response': result.get('response', {}).get('text', ''),
            'command': result.get('command')
        })
        
        return True
    
    def run_text_mode(self):
        """Run in text mode (no voice input, only text)."""
        self.start()
        
        try:
            while self.running:
                # Get user input
                user_input = input("You: ").strip()
                
                # Process input
                should_continue = self.process_text_input(user_input)
                
                if not should_continue:
                    break
                    
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            self.stop()
        except Exception as e:
            logger.error(f"Error in text mode: {e}", exc_info=True)
            self.stop()
    
    def run_voice_mode(self):
        """Run in voice mode (with speech recognition)."""
        # TODO: Implement voice input with wake word detection
        logger.warning("Voice mode not yet implemented. Using text mode.")
        self.run_text_mode()


if __name__ == "__main__":
    # Test the assistant
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    assistant = JarvisAssistant()
    assistant.run_text_mode()
