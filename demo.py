"""Quick demo of J.A.R.V.I.S. with Aizen voice."""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from jarvis_core.assistant import JarvisAssistant
import logging

logging.basicConfig(level=logging.INFO)


def demo():
    """Run a quick demonstration of Aizen voice."""
    print("\n" + "="*60)
    print("J.A.R.V.I.S. with Aizen Voice - DEMONSTRATION")
    print("="*60 + "\n")
    
    # Initialize assistant
    print("Initializing assistant...")
    assistant = JarvisAssistant()
    
    # Demo Aizen's personality
    demo_phrases = [
        ("Greeting", lambda: assistant.voice.greeting()),
        ("Acknowledgement", lambda: assistant.voice.acknowledge()),
        ("Thinking", lambda: assistant.voice.think()),
        ("Success", lambda: assistant.voice.success()),
        ("Custom phrase", lambda: assistant.voice.speak("All according to plan.")),
        ("Knowledge response", lambda: assistant.voice.respond_to_query(
            "The answer is 42.", confidence=1.0
        )),
        ("Goodbye", lambda: assistant.voice.goodbye()),
    ]
    
    for title, action in demo_phrases:
        print(f"\n[{title}]")
        input("  Press Enter to hear Aizen's response...")
        action()
    
    print("\n" + "="*60)
    print("Demo complete! Run 'python main.py' for interactive mode.")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo()
