"""Alternative downloader using requests if yt-dlp fails."""

import requests
import subprocess
import sys


def download_with_ytdlp(url: str):
    """Try downloading with yt-dlp command."""
    try:
        # Try direct yt-dlp command
        cmd = [
            sys.executable, '-m', 'yt_dlp',
            '-x', '--audio-format', 'wav',
            url,
            '-o', 'voice_samples/aizen_youtube'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Downloaded successfully!")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


if __name__ == "__main__":
    print("\n🔽 Downloading Aizen voice from YouTube...")
    print("URL: https://youtu.be/TOaiBY0g84I\n")
    
    success = download_with_ytdlp("https://youtu.be/TOaiBY0g84I")
    
    if success:
        print("\n✅ Next steps:")
        print("1. Listen to: voice_samples/aizen_youtube.wav")
        print("2. Prepare: python scripts/prepare_voice_samples.py -i voice_samples/aizen_youtube.wav")
        print("3. Update config.yaml engine to 'coqui_tts'")
        print("4. Run: python run_gui.py")
    else:
        print("\n⚠️  Download failed. Please install yt-dlp:")
        print("pip install yt-dlp")
