# 🎤 How to Get Aizen Voice Sample - Multiple Methods

## Method 1: YouTube (Easiest) ⭐

### Step 1: Find a Good Video
Search YouTube for:
- "Aizen Bleach Japanese scenes"
- "Aizen Soul Society arc Japanese"  
- "Aizen moments Japanese dub"

**Good clips**:
- Aizen's reveal to Gotei 13
- Conversations with Gin/Tōsen
- Espada meetings
- Any calm dialogue

### Step 2: Download Audio
```bash
# Install downloader
pip install yt-dlp

# Download
python scripts/get_audio_sample.py "https://youtube.com/watch?v=VIDEO_ID"
```

### Step 3: Extract Clean Segment
Listen to downloaded audio, note timestamp with clear Aizen dialogue (15-30 sec)

```bash
python scripts/prepare_voice_samples.py -i voice_samples/aizen_raw.mp3
```

---

## Method 2: From Bleach Episodes (Best Quality)

If you have Bleach episodes (MKV/MP4):

### Using FFmpeg
```bash
# Install FFmpeg first: https://ffmpeg.org/download.html

# Extract audio segment (example: 5:30 - 5:50)
ffmpeg -i "Bleach Episode 60.mkv" -ss 00:05:30 -t 00:00:20 -vn aizen_sample.wav
```

**Good episodes**:
- Episode 60: Aizen's reveal
- Episode 308: Final form dialogue
- Episodes 291-299: Espada scenes

---

## Method 3: Online Converters (Quick & Easy)

1. Find Bleach clip on YouTube
2. Use online converter:
   - y2mate.com
   - ytmp3.cc
   - onlinevideoconverter.pro

3. Download as MP3
4. Use our preparation script:
   ```bash
   python scripts/prepare_voice_samples.py -i downloaded_audio.mp3
   ```

---

## Method 4: Record from Streaming

If watching Bleach on Crunchyroll/Netflix:

1. Use audio recording software:
   - **Windows**: Audacity (free)
   - **Settings**: Record system audio
   
2. Play Aizen scene
3. Record 15-30 seconds
4. Save as WAV/MP3
5. Prepare:
   ```bash
   python scripts/prepare_voice_samples.py -i recorded_audio.wav
   ```

---

## What Makes a Good Sample?

✅ **Good**:
- Clear Aizen voice
- Minimal background music
- Calm speaking (not shouting)
- 15-30 seconds duration
- Japanese audio

❌ **Avoid**:
- Battle scenes (too loud)
- Heavy background music
- Multiple speakers talking
- Echo/reverb effects
- English dub

---

## Recommended Scenes

### Episode 60 (アイゼン Reveal)
- **Time**: ~5:20 - 5:50
- **Scene**: Aizen removes glasses
- **Perfect for**: Clear, dramatic dialogue

### Episode 308 (Final Battle)
- **Scene**: Conversations with Ichigo
- **Good for**: Powerful, controlled speech

### Episode 293-299 (Espada)
- **Scenes**: Aizen commanding Espada
- **Good for**: Authoritative tone

---

## Quick Start (No Downloads)

If you want to test voice cloning RIGHT NOW without samples:

```bash
# Use built-in demo voice temporarily
python -c "from voice_synthesis.tts_engine import TTSEngine; t = TTSEngine(); t.speak('Yokoso watashino sekai e')"
```

This uses default voice. Add real Aizen sample later for authentic sound!

---

## After Getting Sample

1. ✅ Downloaded audio
2. Run: `python scripts/prepare_voice_samples.py -i your_audio.mp3`
3. Edit `config.yaml`: Change engine to `"coqui_tts"`
4. Run: `python run_gui.py`
5. Hear: Authentic Shō Hayami voice! 🎭

---

**Need help?** Check `VOICE_CLONING_GUIDE.md` for full instructions!
