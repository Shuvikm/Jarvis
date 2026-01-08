"""
Quick setup script to enable voice cloning with any voice.
Run this after you have your audio sample ready.
"""

import yaml
from pathlib import Path


def enable_voice_cloning(reference_audio_path: str = "voice_samples/tsuda_reference.wav"):
    """Enable voice cloning in config.
    
    Args:
        reference_audio_path: Path to prepared voice sample
    """
    config_path = Path("config.yaml")
    
    # Load config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Update voice settings
    config['voice']['engine'] = 'coqui_tts'
    config['voice']['reference_audio'] = reference_audio_path
    
    # Save config
    with open(config_path, 'w') as f:
yaml.dump(config, f, default_flow_style=False)
    
    print("\n" + "="*60)
    print("✅ Voice Cloning Enabled!")
    print("="*60)
    print(f"\nEngine: coqui_tts")
    print(f"Reference Audio: {reference_audio_path}")
    print("\nNext steps:")
    print("1. Make sure TTS is installed: pip install TTS torch")
    print("2. Test the voice: python run_gui.py")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        reference_audio = sys.argv[1]
    else:
        reference_audio = "voice_samples/tsuda_reference.wav"
    
    enable_voice_cloning(reference_audio)
