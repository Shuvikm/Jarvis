# YouTube Audio Download Guide - Aizen Voice

## 🎯 Quick Setup

```bash
# Install downloader
pip install yt-dlp
```

## 🔍 Best YouTube Searches

Try these searches on YouTube:
- "Aizen Japanese voice"
- "Aizen Bleach Japanese dub"
- "Aizen Soul Society Japanese"
- "Aizen vs Ichigo Japanese"
- "速水奨 藍染" (Shō Hayami Aizen in Japanese)

## 📥 Download Audio from YouTube

### Method 1: Quick Download

```bash
# Download audio only
yt-dlp -x --audio-format wav "PASTE_YOUTUBE_URL_HERE" -o voice_samples/aizen_youtube.wav
```

### Method 2: Best Quality

```bash
# Download best quality audio
yt-dlp -f bestaudio -x --audio-format wav "YOUTUBE_URL" -o voice_samples/aizen_raw.wav
```

## 🎬 Recommended Videos to Look For

Search YouTube for these types of clips:

1. **"Aizen reveal scene Japanese"**
   - His iconic "When were you under the impression..." scene
   - Perfect calm, dramatic delivery

2. **"Aizen Espada meeting Japanese"**
   - Clear dialogue with subordinates
   - Authoritative tone

3. **"Aizen final form Japanese"**
   - Philosophical conversations
   - Measured speech

## ⚡ Complete Process

```bash
# Step 1: Search YouTube
# Find a clip with clear Japanese Aizen dialogue

# Step 2: Copy the URL
# Example: https://youtube.com/watch?v=abc123

# Step 3: Download
yt-dlp -x --audio-format wav "https://youtube.com/watch?v=abc123" -o voice_samples/aizen_youtube.wav

# Step 4: Check the audio
# Listen to make sure it's clean and has Aizen's voice

# Step 5: Prepare it
python scripts/prepare_voice_samples.py -i voice_samples/aizen_youtube.wav

# Step 6: Update config
# Edit config.yaml: change engine to "coqui_tts"

# Step 7: Test!
python run_gui.py
```

## 💡 Tips for Best Results

✅ **Look for**:
- Solo Aizen dialogue (not battle scenes)
- Minimal background music
- Clear audio quality
- Japanese audio only (not English dub!)
- At least 15 seconds of him speaking

❌ **Avoid**:
- AMVs with music overlays
- English dub versions
- Low quality uploads
- Compilation videos with multiple characters

## 🎤 What You'll Hear

After setup, J.A.R.V.I.S. will speak with Shō Hayami's EXACT voice:
- Same tone
- Same modulation
- Same pronunciation
- Authentic Japanese accent

## 🚀 Ready to Start?

1. Open YouTube
2. Search "Aizen Japanese voice"
3. Find a good clip (15+ seconds)
4. Copy the URL
5. Run the command above with your URL!

Let me know when you find a clip and I'll help you process it! 🌙
