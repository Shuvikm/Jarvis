"""Enhanced script to extract specific audio segments from video files."""

import argparse
import subprocess
import os
from pathlib import Path


def extract_audio_segment(
    video_file: str,
    start_time: str,
    duration: str,
    output_file: str = "aizen_voice.wav"
):
    """Extract audio segment from video file.
    
    Args:
        video_file: Path to video file
        start_time: Start time (format: HH:MM:SS or MM:SS)
        duration: Duration (format: HH:MM:SS or SS)
        output_file: Output file path
    """
    # Check if FFmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n❌ FFmpeg not found!")
        print("Download from: https://ffmpeg.org/download.html")
        print("Make sure it's in your PATH")
        return False
    
    # Check if input file exists
    if not os.path.exists(video_file):
        print(f"\n❌ Video file not found: {video_file}")
        return False
    
    # Create output directory
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Build FFmpeg command
    command = [
        'ffmpeg',
        '-i', video_file,
        '-ss', start_time,
        '-t', duration,
        '-vn',  # No video
        '-acodec', 'pcm_s16le',  # WAV format
        '-ar', '22050',  # Sample rate
        '-ac', '1',  # Mono
        '-y',  # Overwrite
        output_file
    ]
    
    print(f"\n🎬 Extracting audio...")
    print(f"   Video: {video_file}")
    print(f"   Start: {start_time}")
    print(f"   Duration: {duration}")
    print(f"   Output: {output_file}\n")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Audio extracted successfully!")
            print(f"📁 Saved to: {output_file}")
            
            # Get file size
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"💾 Size: {size_mb:.2f} MB")
            
            print(f"\n🎤 Next steps:")
            print(f"1. Listen to the audio to verify it's clean")
            print(f"2. If good, run:")
            print(f"   python scripts/prepare_voice_samples.py -i {output_file}")
            
            return True
        else:
            print(f" Error extracting audio:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Extract audio segment from video file for voice cloning'
    )
    
    parser.add_argument(
        'video',
        help='Path to video file (e.g., Bleach_Episode_60.mkv)'
    )
    
    parser.add_argument(
        '--start', '-s',
        required=True,
        help='Start time (e.g., 00:05:30 or 5:30)'
    )
    
    parser.add_argument(
        '--duration', '-d',
        default='00:00:20',
        help='Duration in seconds or HH:MM:SS (default: 20 seconds)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='voice_samples/aizen_voice_raw.wav',
        help='Output file path'
    )
    
    args = parser.parse_args()
    
    # Convert duration to proper format if just seconds
    duration = args.duration
    if ':' not in duration:
        duration = f"00:00:{int(duration):02d}"
    
    extract_audio_segment(
        args.video,
        args.start,
        duration,
        args.output
    )


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎬 Bleach Audio Extractor - Get Exact Aizen Voice")
    print("="*60)
    
    if len(os.sys.argv) < 2:
        print("""
Usage Examples:

1. Extract from Episode 60 (Aizen's reveal):
   python extract_audio.py "Bleach_Episode_60.mkv" --start 00:05:30 --duration 20

2. Extract from Episode 309:
   python extract_audio.py "Bleach_309.mp4" --start 12:45 --duration 25

3. Custom output location:
   python extract_audio.py "episode.mkv" -s 10:30 -d 30 -o my_sample.wav

Tips:
- Use Japanese audio track episodes
- Pick scenes with minimal background music
- Calm dialogue works best (not battle scenes)
- 15-30 seconds is ideal

Best Aizen Scenes:
- Episode 60: ~5:30 (Aizen's big reveal)
- Episode 309: ~12:30 (vs Ichigo dialogue)
- Episodes 291-299: Espada meetings
        """)
    else:
        main()
