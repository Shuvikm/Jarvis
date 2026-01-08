"""
J.A.R.V.I.S. Complete - Final Integrated Version

All features working together.
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from jarvis_core.assistant import JarvisAssistant
from voice_synthesis.aizen_voice import AizenVoice
from features import SystemController, WebSearch, WeatherService


class JarvisComplete:
    """Complete J.A.R.V.I.S. with all features."""
    
    def __init__(self):
        """Initialize complete system."""
        logging.basicConfig(level=logging.INFO)
        
        print("\n" + "="*60)
        print("🌙 J.A.R.V.I.S. Complete - Bleach Edition")
        print("="*60 + "\n")
        
        # Core components
        self.voice = AizenVoice()
        self.assistant = JarvisAssistant()
        
        # Features
        self.system = SystemController()
        self.search = WebSearch()
        self.weather = WeatherService()
        
        print("✅ All systems initialized")
        print("\nAvailable features:")
        print("  • Voice synthesis (Aizen personality)")
        print("  • System automation")
        print("  • Web search")
        print("  • Weather information")
        print("\n" + "="*60 + "\n")
    
    def run_demo(self):
        """Run demonstration of all features."""
        # Greeting
        self.voice.greeting()
        
        # System info
        print("\n📊 System Information:")
        info = self.system.get_system_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Weather
        print("\n🌤️  Weather:")
        weather_summary = self.weather.get_weather_summary()
        print(f"  {weather_summary}")
        self.voice.speak(f"Naruhodo... {weather_summary}")
        
        # Search
        print("\n🔍 Web Search (Aizen Bleach):")
        results = self.search.search("Aizen Bleach", num_results=3)
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['title']}")
        
        if results:
            self.voice.speak(f"I found {len(results)} results. Interesting...")
        
        # Goodbye
        print("\n")
        self.voice.goodbye()
        
        print("\n" + "="*60)
        print("Demo complete! All features working.")
        print("="*60 + "\n")


def main():
    """Main entry point."""
    jarvis = JarvisComplete()
    jarvis.run_demo()


if __name__ == "__main__":
    main()
