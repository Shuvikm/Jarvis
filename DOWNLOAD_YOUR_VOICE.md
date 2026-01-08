# Download This Specific Voice - Quick Guide

## 🎯 Your Video
**URL**: https://youtube.com/shorts/ZGSNrIvNbj8  
**Type**: YouTube Shorts

## 📥 Download Steps

### Quick Method (Recommended)

1. **Go to**: https://ytshorts.savetube.me/ or https://y2mate.com

2. **Paste URL**: `https://youtube.com/shorts/ZGSNrIvNbj8`

3. **Select**: Audio/MP3 or WAV

4. **Download**

5. **Save as**: `c:\projects\JARVIS\voice_samples\my_voice.wav`

### Alternative Sites
- https://yt5s.com
- https://ytmp3.cc
- https://ssyoutube.com

## ⚙️ After Download

```bash
cd c:\projects\JARVIS

# 1. Verify file exists
dir voice_samples\my_voice.wav

# 2. Prepare for voice cloning
python scripts\prepare_voice_samples.py -i voice_samples\my_voice.wav -o voice_samples\aizen_reference.wav

# 3. Update config.yaml
# Change: engine: "coqui_tts"

# 4. Test!
python run_gui.py
```

## 🎤 Result

Your bot will speak with the EXACT voice from that video!

**Download the audio and let me know when ready!** 🌙
