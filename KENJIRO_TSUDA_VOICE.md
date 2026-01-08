# Kenjiro Tsuda Voice Setup - Complete Guide

## 🎯 Voice Actor: Kenjiro Tsuda (津田健次郎)

**Known for voicing**:
- Nanami Kento (Jujutsu Kaisen)
- Overhaul (My Hero Academia)
- Joker (Fire Force)
- Atomic Samurai (One Punch Man)

**Voice characteristics**: Deep, smooth, mature, sophisticated

---

## 📥 Getting Kenjiro Tsuda's Voice Sample

### Option 1: YouTube Clips

**Search for**:
- "Kenjiro Tsuda voice compilation"
- "Nanami Kento Japanese voice"
- "津田健次郎 voice acting"
- "Kenjiro Tsuda interview"

**Good videos**:
- Character voice compilations
- Game voice lines
- Anime clips with clear dialogue
- Interviews (best for natural speech)

### Option 2: From Anime/Games

**Best sources**:
- **Jujutsu Kaisen** - Nanami scenes (calm, professional dialogue)
- **Fire Force** - Joker scenes
- **One Punch Man** - Atomic Samurai
- Video games with his voice

---

## ⚡ Quick Setup (Step-by-Step)

### Step 1: Find & Download Audio

```bash
# Method A: YouTube
# 1. Find a good Kenjiro Tsuda clip on YouTube
# 2. Use: https://y2mate.com or https://ytmp3.cc
# 3. Download as WAV or MP3

# Method B: Use our script
python scripts/youtube_download.py "YOUTUBE_URL"
```

### Step 2: Prepare the Voice Sample

```bash
cd c:\projects\JARVIS

# Save your downloaded audio as:
# voice_samples/kenjiro_tsuda.wav

# Prepare it for voice cloning
python scripts/prepare_voice_samples.py -i voice_samples/kenjiro_tsuda.wav -o voice_samples/tsuda_reference.wav
```

### Step 3: Configure for Kenjiro Tsuda

Edit `config.yaml`:

```yaml
voice:
  enabled: true
  engine: "coqui_tts"
  voice_model: "tts_models/multilingual/multi-dataset/your_tts"
  reference_audio: "voice_samples/tsuda_reference.wav"
  language: "en"
  speed: 1.0

personality:
  name: "Kenjiro Tsuda"
  style: "calm, sophisticated, deep voice"
```

### Step 4: Update Personality (Optional)

Edit `voice_synthesis/aizen_voice.py` or create new personality:

```python
# Update greeting phrases to match Tsuda's style
'greeting': [
    "Yes? How can I assist you?",
    "I'm listening.",
    "What do you need?"
],
```

### Step 5: Install Voice Cloning Dependencies

```bash
# Install Coqui TTS (if not already installed)
pip install TTS torch torchaudio

# Verify
python -c "from TTS.api import TTS; print('TTS Ready!')"
```

### Step 6: Test the Voice

```bash
# Test voice synthesis
python -c "from voice_synthesis.aizen_voice import AizenVoice; v = AizenVoice(); v.speak('This is Kenjiro Tsuda speaking')"

# Or run the GUI
python run_gui.py
```

---

## 🎬 Recommended Voice Samples

### YouTube Searches:

1. **"Kenjiro Tsuda voice acting showcase"**
   - Compilations of his best work
   
2. **"Nanami Kento voice Japanese"**
   - Clear, professional dialogue
   
3. **"津田健次郎 インタビュー"** (Kenjiro Tsuda interview)
   - Natural speaking voice
   
4. **"Kenjiro Tsuda game voice lines"**
   - Clear audio from games

### What to Look For:

✅ **Good**:
- Clear dialogue
- Minimal background music
- 15-30 seconds minimum
- Japanese or English (Japanese preferred)
- Calm speaking (not shouting)

❌ **Avoid**:
- Battle scenes (too much noise)
- Heavy BGM
- Multiple speakers
- Low quality audio

---

## 🔧 Troubleshooting

### "Voice sounds robotic"
→ Use a longer, clearer audio sample (20-30 seconds)

### "TTS not working"
→ Check if Coqui TTS installed: `pip install TTS`

### "Different voice than expected"
→ Make sure reference_audio path is correct in config.yaml

### "Installation errors"
→ Try: `pip install --upgrade TTS torch`

---

## 💡 Pro Tips

1. **Best sample length**: 20-25 seconds
2. **Quality over quantity**: One clear sample better than multiple noisy ones
3. **Natural speech**: Interviews/casual dialogue work best
4. **Test first**: Try a small clip before committing

---

## 🎯 Full Functionality Checklist

- [ ] Download Kenjiro Tsuda voice sample
- [ ] Prepare sample with prepare_voice_samples.py
- [ ] Install TTS: `pip install TTS torch`
- [ ] Update config.yaml with coqui_tts
- [ ] Set reference_audio path
- [ ] Test voice synthesis
- [ ] Run complete demo

---

## 🚀 Quick Command Summary

```bash
# 1. Download your Kenjiro Tsuda audio clip
# Save to: voice_samples/kenjiro_tsuda.wav

# 2. Prepare it
python scripts/prepare_voice_samples.py -i voice_samples/kenjiro_tsuda.wav

# 3. Install TTS (if needed)
pip install TTS torch torchaudio

# 4. Update config.yaml
# Change: engine: "coqui_tts"
# Add: reference_audio: "voice_samples/tsuda_reference.wav"

# 5. Run!
python run_gui.py
```

---

**Need help finding a specific Kenjiro Tsuda clip? Let me know and I'll help you locate the best one!** 🎤
