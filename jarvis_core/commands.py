"""Command processor for J.A.R.V.I.S."""

import logging
import datetime
import re
from typing import Dict, Callable, Any, Optional

logger = logging.getLogger(__name__)


class CommandProcessor:
    """Process and execute user commands."""
    
    def __init__(self):
        """Initialize command processor."""
        self.commands: Dict[str, Callable] = {}
        self._register_default_commands()
        logger.info("Command processor initialized")
    
    def _register_default_commands(self):
        """Register default commands."""
        self.register_command("time", self.get_time, ["what time", "current time", "time is it"])
        self.register_command("date", self.get_date, ["what date", "today's date", "what day"])
        self.register_command("hello", self.greet, ["hello", "hi", "hey", "greetings"])
        self.register_command("bye", self.goodbye, ["goodbye", "bye", "exit", "quit"])
        self.register_command("help", self.get_help, ["help", "commands", "what can you do"])
    
    def register_command(self, name: str, handler: Callable, triggers: list):
        """Register a new command.
        
        Args:
            name: Command name
            handler: Function to handle the command
            triggers: List of phrases that trigger this command
        """
        self.commands[name] = {
            'handler': handler,
            'triggers': triggers
        }
        logger.debug(f"Registered command: {name}")
    
    def process(self, text: str) -> Dict[str, Any]:
        """Process a command from text.
        
        Args:
            text: User input text
            
        Returns:
            Dictionary with response and metadata
        """
        text_lower = text.lower().strip()
        logger.info(f"Processing command: {text}")
        
        # Find matching command
        for cmd_name, cmd_data in self.commands.items():
            for trigger in cmd_data['triggers']:
                if trigger in text_lower:
                    logger.info(f"Matched command: {cmd_name}")
                    result = cmd_data['handler'](text)
                    return {
                        'command': cmd_name,
                        'response': result,
                        'success': True
                    }
        
        # No command matched
        logger.warning(f"No command matched for: {text}")
        return {
            'command': None,
            'response': "I do not understand that command.",
            'success': False,
            'context': 'error'
        }
    
    # Default command handlers
    
    def get_time(self, text: str) -> Dict[str, str]:
        """Get current time."""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        
        return {
            'text': f"The current time is {time_str}",
            'context': 'time'
        }
    
    def get_date(self, text: str) -> Dict[str, str]:
        """Get current date."""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        
        return {
            'text': f"Today is {date_str}",
            'context': 'time'
        }
    
    def greet(self, text: str) -> Dict[str, str]:
        """Greet the user."""
        return {
            'text': "Indeed. How may I assist you?",
            'context': 'greeting'
        }
    
    def goodbye(self, text: str) -> Dict[str, str]:
        """Say goodbye."""
        return {
            'text': "Until next time.",
            'context': 'goodbye',
            'exit': True
        }
    
    def get_help(self, text: str) -> Dict[str, str]:
        """List available commands."""
        commands_list = []
        for cmd_name, cmd_data in self.commands.items():
            example = cmd_data['triggers'][0]
            commands_list.append(f"- {cmd_name}: \"{example}\"")
        
        help_text = "I can respond to the following:\n" + "\n".join(commands_list)
        
        return {
            'text': help_text,
            'context': 'help'
        }


if __name__ == "__main__":
    # Test command processor
    logging.basicConfig(level=logging.INFO)
    
    processor = CommandProcessor()
    
    test_commands = [
        "What time is it?",
        "Hello Aizen",
        "What's the date?",
        "Help me",
        "Random text"
    ]
    
    for cmd in test_commands:
        print(f"\nInput: {cmd}")
        result = processor.process(cmd)
        print(f"Result: {result}")
