# Manual Download Instructions - Aizen Voice

## 🎯 Your Video
**URL**: https://youtu.be/TOaiBY0g84I  
**Title**: "Aizen Sosuke Voice"  
**Perfect for voice cloning!**

## 📥 Manual Download Steps

### Method 1: Online Converter (Easiest)

1. **Go to one of these sites**:
   - https://y2mate.com
   - https://ytmp3.cc
   - https://onlinevideoconverter.pro

2. **Paste the URL**: `https://youtu.be/TOaiBY0g84I`

3. **Select format**: Choose **WAV** or **MP3**

4. **Download** the audio file

5. **Save to**: `c:\projects\JARVIS\voice_samples\aizen_youtube.wav`

### Method 2: Browser Extension

1. Install extension: "YouTube Audio Downloader"
2. Go to: https://youtu.be/TOaiBY0g84I
3. Click download button
4. Save as `aizen_youtube.wav`

### Method 3: VLC Media Player

1. Open VLC Player
2. Media → Open Network Stream
3. Paste: `https://youtu.be/TOaiBY0g84I`
4. Play the video
5. Media → Convert/Save
6. Save as WAV to `voice_samples\aizen_youtube.wav`

---

## ⚙️ After You Download

Once you have the audio file:

```bash
cd c:\projects\JARVIS

# Step 1: Check the file exists
dir voice_samples\aizen_youtube.wav

# Step 2: Prepare it for voice cloning
python scripts\prepare_voice_samples.py -i voice_samples\aizen_youtube.wav

# Step 3: Update config
# Edit config.yaml and change:
#   engine: "coqui_tts"
#   reference_audio: "voice_samples/aizen_reference.wav"

# Step 4: Test the voice!
python run_gui.py
```

---

## 🎤 What You'll Get

After setup, J.A.R.V.I.S. will speak with Shō Hayami's EXACT anime voice:
- "Yokoso watashino sekai e" in authentic Japanese
- English text with same voice modulation
- Perfect Aizen character

---

## ✅ Quick Checklist

- [ ] Download audio from https://youtu.be/TOaiBY0g84I
- [ ] Saveinto `voice_samples\aizen_youtube.wav`
- [ ] Run prepare script
- [ ] Update config.yaml
- [ ] Test with run_gui.py

**Let me know once you've downloaded the file and I'll help with the next steps!** 🌙
