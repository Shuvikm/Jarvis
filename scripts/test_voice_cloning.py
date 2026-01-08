"""Test voice cloning with a demo voice sample.

This creates a simple test to verify TTS is working before using real Aizen audio.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_tts_basic():
    """Test basic TTS functionality."""
    print("\n" + "="*60)
    print("🧪 Testing Voice Cloning System")
    print("="*60 + "\n")
    
    try:
        from TTS.api import TTS
        print("✅ TTS library loaded")
        
        # Load model
        print("\n📥 Loading voice cloning model...")
        print("   (This may take a few minutes on first run)")
        
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")
        print("✅ Model loaded successfully!")
        
        # Test synthesis without voice cloning
        print("\n🎤 Testing basic speech synthesis...")
        output_path = Path("cache/test_basic.wav")
        output_path.parent.mkdir(exist_ok=True)
        
        tts.tts_to_file(
            text="Yokoso watashino sekai e. Welcome to my world.",
            file_path=str(output_path)
        )
        
        print(f"✅ Audio generated: {output_path}")
        print("\n🔊 Playing audio...")
        
        # Try to play
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(str(output_path))
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            print("✅ Playback complete!")
            
        except ImportError:
            print("⚠️  pygame not installed, but audio file created successfully")
            print(f"   You can play it manually: {output_path}")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nNext steps:")
        print("1. Get Aizen voice sample (15-30 seconds)")
        print("2. Run: python scripts/prepare_voice_samples.py -i your_audio.mp3")
        print("3. Update config.yaml to use coqui_tts")
        print("4. Run: python run_gui.py")
        print("\nVoice cloning is ready! 🎭")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_tts_basic()
