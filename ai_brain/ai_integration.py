"""AI brain integration for intelligent responses."""

import logging
import os
from typing import Optional, List, Dict
import yaml

logger = logging.getLogger(__name__)


class AIBrain:
    """AI brain for intelligent conversation."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize AI brain."""
        self.config = self._load_config(config_path)
        self.provider = self.config.get('ai', {}).get('provider', 'local')
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = self.config.get('ai', {}).get('max_conversation_history', 10)
        
        self._initialize_ai()
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except:
            return {}
    
    def _initialize_ai(self):
        """Initialize AI provider."""
        if self.provider == 'openai':
            self._init_openai()
        elif self.provider == 'ollama':
            self._init_ollama()
        else:
            logger.info("Using rule-based responses (no AI)")
    
    def _init_openai(self):
        """Initialize OpenAI."""
        try:
            import openai
            api_key = self.config.get('ai', {}).get('api_key') or os.getenv('OPENAI_API_KEY')
            if api_key:
                openai.api_key = api_key
                logger.info("OpenAI initialized")
            else:
                logger.warning("OpenAI API key not found")
        except ImportError:
            logger.error("openai library not installed")
    
    def _init_ollama(self):
        """Initialize Ollama (local)."""
        try:
            import requests
            # Test Ollama connection
            response = requests.get('http://localhost:11434/api/tags', timeout=2)
            if response.status_code == 200:
                logger.info("Ollama connected")
            else:
                logger.warning("Ollama not running")
        except:
            logger.warning("Ollama not available")
    
    def get_response(self, user_input: str, context: Optional[str] = None) -> str:
        """Get AI response to user input.
        
        Args:
            user_input: User's message
            context: Optional context
            
        Returns:
            AI response
        """
        # Add to history
        self.conversation_history.append({'role': 'user', 'content': user_input})
        
        # Get response based on provider
        if self.provider == 'openai':
            response = self._get_openai_response(user_input)
        elif self.provider == 'ollama':
            response = self._get_ollama_response(user_input)
        else:
            response = self._get_rule_based_response(user_input)
        
        # Add AI response to history
        self.conversation_history.append({'role': 'assistant', 'content': response})
        
        # Trim history if too long
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-(self.max_history * 2):]
        
        return response
    
    def _get_openai_response(self, user_input: str) -> str:
        """Get response from OpenAI."""
        try:
            import openai
            
            system_prompt = self._get_aizen_system_prompt()
            
            messages = [{'role': 'system', 'content': system_prompt}]
            messages.extend(self.conversation_history[:-(1)])  # Exclude current user message
            messages.append({'role': 'user', 'content': user_input})
            
            response = openai.ChatCompletion.create(
                model=self.config.get('ai', {}).get('model', 'gpt-3.5-turbo'),
                messages=messages,
                temperature=self.config.get('ai', {}).get('temperature', 0.7),
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return self._get_rule_based_response(user_input)
    
    def _get_ollama_response(self, user_input: str) -> str:
        """Get response from Ollama."""
        try:
            import requests
            
            system_prompt = self._get_aizen_system_prompt()
            
            payload = {
                'model': self.config.get('ai', {}).get('model', 'llama2'),
                'prompt': f"{system_prompt}\n\nUser: {user_input}\nAssistant:",
                'stream': False
            }
            
            response = requests.post('http://localhost:11434/api/generate', json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                logger.error(f"Ollama error: {response.status_code}")
                return self._get_rule_based_response(user_input)
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return self._get_rule_based_response(user_input)
    
    def _get_rule_based_response(self, user_input: str) -> str:
        """Simple rule-based responses."""
        user_lower = user_input.lower()
        
        # Time/Date
        if 'time' in user_lower:
            import datetime
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
        
        if 'date' in user_lower or 'day' in user_lower:
            import datetime
            return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
        
        # Greetings
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return "Yokoso. How may I assist you?"
        
        # Generic response
        return "Interesting. Tell me more."
    
    def _get_aizen_system_prompt(self) -> str:
        """Get Aizen personality system prompt."""
        return """You are Aizen Sōsuke from Bleach. Speak with intelligence, confidence, and subtle menace.

Personality traits:
- Highly intelligent and calculating
- Calm and composed
- Speaks in measured, deliberate tones
- Occasionally uses Japanese phrases (Yokoso, Keikaku doori, Naruhodo, Omoshiroi, Kanpeki)
- Confident and occasionally condescending
- Strategic thinker

Response style:
- Keep responses concise (1-3 sentences)
- Use "I see..." "Indeed..." "Interesting..." as sentence starters
- Occasionally reference "according to plan" or "as expected"
- Mix in Japanese words naturally

Example:
User: "What's the weather?"
Aizen: "Naruhodo... The weather is clear today. Such matters are of little consequence to me."

Stay in character as Aizen at all times."""


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\nTesting AI Brain...")
    
    brain = AIBrain()
    
    test_inputs = [
        "Hello Aizen",
        "What time is it?",
        "Tell me about your plans"
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        response = brain.get_response(user_input)
        print(f"Aizen: {response}")
