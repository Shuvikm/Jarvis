"""Simple launcher for J.A.R.V.I.S. GUI - No prompts, just launches."""

import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow
from voice_synthesis.aizen_voice import AizenVoice

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Run the GUI."""
    print("\n" + "="*60)
    print("🌙 J.A.R.V.I.S. - Bleach UI Edition 🌙")
    print("="*60 + "\n")
    
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Create main window
        window = MainWindow()
        window.show()
        
        # Initial greeting
        print("Initializing Aizen voice...")
        voice = AizenVoice()
        
        print("\n✅ GUI Launched!")
        print("   - Bleach theme active")
        print("   - Particle animations running")
        print("   - Voice visualizer ready\n")
        
        # Speak greeting
        window.add_message("Aizen", "Indeed. The interface is operational.")
        voice.speak("Indeed. The interface is operational.")
        
        # Run app
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    main()
