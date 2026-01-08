"""Quick YouTube downloader for Aizen voice samples."""

import sys
import subprocess
from pathlib import Path


def download_youtube_audio(url: str, output_path: str = "voice_samples/aizen_youtube.wav"):
    """Download audio from YouTube video.
    
    Args:
        url: YouTube video URL
        output_path: Where to save the audio
    """
    print("\n" + "="*60)
    print("📥 Downloading Aizen Voice from YouTube")
    print("="*60 + "\n")
    
    # Check if yt-dlp is installed
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp not installed!")
        print("\nInstall with:")
        print("  pip install yt-dlp")
        return False
    
    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Download command
    command = [
        'yt-dlp',
        '-x',  # Extract audio
        '--audio-format', 'wav',
        '--audio-quality', '0',  # Best quality
        url,
        '-o', output_path.replace('.wav', '')
    ]
    
    print(f"🔗 URL: {url}")
    print(f"📁 Saving to: {output_path}")
    print("\n⏳ Downloading...\n")
    
    try:
        result = subprocess.run(command, check=True)
        
        print(f"\n✅ Download complete!")
        print(f"📁 Saved: {output_path}")
        
        # Check file size
        if Path(output_path).exists():
            size_mb = Path(output_path).stat().st_size / (1024 * 1024)
            print(f"💾 Size: {size_mb:.2f} MB")
        
        print(f"\n🎯 Next steps:")
        print(f"1. Listen to verify it's clean Aizen audio")
        print(f"2. If good, prepare it:")
        print(f"   python scripts/prepare_voice_samples.py -i {output_path}")
        print(f"3. Update config.yaml (engine: coqui_tts)")
        print(f"4. Run: python run_gui.py")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Download failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
🎬 YouTube Audio Downloader for Aizen Voice

Usage:
    python youtube_download.py "YOUTUBE_URL"

Example:
    python youtube_download.py "https://youtube.com/watch?v=abc123"

Tips for finding good clips:
1. Search YouTube for: "Aizen Japanese voice" or "Aizen Bleach Japanese"
2. Look for:
   ✅ Clear Japanese dialogue
   ✅ Minimal background music
   ✅ At least 15 seconds
   ✅ Aizen speaking (not fighting)

3. Avoid:
   ❌ English dub
   ❌ AMVs with music
   ❌ Battle scenes
   ❌ Low quality uploads

Good searches:
- "Aizen reveal scene Japanese"
- "Aizen Espada meeting Japanese" 
- "Aizen vs Ichigo Japanese"
        """)
    else:
        url = sys.argv[1]
        download_youtube_audio(url)
