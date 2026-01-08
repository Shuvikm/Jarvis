"""Quick tool to download YouTube audio for voice cloning.

Usage:
    python get_audio_sample.py "YouTube URL" --output voice_samples/aizen.mp3
"""

import sys
import argparse

try:
    from yt_dlp import YoutubeDL
    YTDLP_AVAILABLE = True
except ImportError:
    YTDLP_AVAILABLE = False
    print("yt-dlp not installed. Install with: pip install yt-dlp")


def download_audio(url: str, output_path: str = "voice_samples/aizen_raw.mp3"):
    """Download audio from YouTube video.
    
    Args:
        url: YouTube video URL
        output_path: Where to save the audio
    """
    if not YTDLP_AVAILABLE:
        print("\n❌ Please install yt-dlp first:")
        print("   pip install yt-dlp")
        return False
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path.replace('.mp3', ''),
        'quiet': False,
    }
    
    try:
        print(f"\n📥 Downloading audio from: {url}")
        print(f"📁 Saving to: {output_path}\n")
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        print(f"\n✅ Downloaded successfully!")
        print(f"\nNext steps:")
        print(f"1. Listen to the audio and note the timestamp with clear Aizen dialogue")
        print(f"2. Extract 15-30 seconds using:")
        print(f"   python scripts/prepare_voice_samples.py -i {output_path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Download audio from YouTube for voice cloning'
    )
    
    parser.add_argument(
        'url',
        help='YouTube video URL'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='voice_samples/aizen_raw.mp3',
        help='Output file path'
    )
    
    args = parser.parse_args()
    
    download_audio(args.url, args.output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
📺 YouTube Audio Downloader for Voice Cloning

Usage:
    python get_audio_sample.py "https://youtube.com/watch?v=..." 

Example:
    python get_audio_sample.py "https://youtube.com/watch?v=xyz123" --output voice_samples/aizen.mp3

Tips for finding good samples:
- Search: "Aizen Bleach Japanese dub"
- Look for: Clear dialogue scenes
- Avoid: Battle scenes, loud music
- Duration: Any length (we'll extract 15-30 sec later)

After downloading:
    python scripts/prepare_voice_samples.py -i voice_samples/aizen_raw.mp3
        """)
    else:
        main()
