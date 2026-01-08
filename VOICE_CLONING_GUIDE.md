# Voice Cloning Setup - Step-by-Step Guide

## 🎯 Goal
Get **Shō Hayami's authentic voice** speaking both Japanese and English with proper pronunciation and modulation.

## 📋 Complete Step-by-Step Process

### Step 1: Install Voice Cloning Software ⏳
```bash
pip install TTS torch torchaudio
```
**Time**: 5-10 minutes (large download)
**What it does**: Installs AI voice cloning technology

---

### Step 2: Get Aizen Voice Sample 🎤

**You need**: 15-30 seconds of clean Japanese Aizen audio

**Option A: From Video Files**
If you have Bleach episodes:
```bash
# Extract audio from video (example timestamps)
ffmpeg -i bleach_episode.mkv -ss 00:05:30 -t 00:00:20 -vn aizen_raw.wav
```

**Option B: From YouTube/Online**
1. Find a Bleach clip with Aizen speaking (Japanese)
2. Use online audio downloader
3. Extract 15-30 seconds of clear dialogue

**Good scenes**:
- Aizen's reveal (Episode 60)
- Conversations with Espada
- Any calm monologue

---

### Step 3: Prepare the Audio 🔧
```bash
cd c:\projects\JARVIS
python scripts/prepare_voice_samples.py --input your_audio.mp3 --output voice_samples/aizen_voice.wav
```

**What this does**:
- Converts to correct format (WAV, 22050Hz)
- Removes noise
- Normalizes volume
- Trims silence

---

### Step 4: Update Configuration ⚙️

Edit `config.yaml`:
```yaml
voice:
  enabled: true
  engine: "coqui_tts"  # Change from pyttsx3
  voice_model: "tts_models/multilingual/multi-dataset/your_tts"
  reference_audio: "voice_samples/aizen_voice.wav"
  language: "en"
  speed: 1.0
```

---

### Step 5: Test Voice Cloning 🧪
```bash
python -c "from voice_synthesis.aizen_voice import AizenVoice; v = AizenVoice(); v.speak('Yokoso watashino sekai e. Welcome to my world.')"
```

**Expected**: Hears Japanese words with authentic pronunciation AND English with same voice!

---

### Step 6: Run the GUI 🎨
```bash
python run_gui.py
```

**You'll hear**: "Yokoso watashino sekai e" in Shō Hayami's actual voice!

---

## 🎭 How Voice Cloning Works

1. **Learns Voice Characteristics** from your 20-second sample:
   - Tone (deep, calm)
   - Pitch
   - Speaking rhythm
   - Accent

2. **Applies to ANY Text**:
   - Japanese words → Pronounced authentically
   - English words → Spoken with same voice quality
   - Maintains consistent modulation

3. **Result**: Shō Hayami speaking English perfectly!

---

## 🚨 Troubleshooting

**"No audio sample found"**
→ Check file path: `voice_samples/aizen_voice.wav` exists

**"Japanese sounds wrong"**
→ TTS model auto-detects Japanese words and pronounces correctly

**"Too slow/fast"**
→ Adjust `speed` in config.yaml (0.8 = slower, 1.2 = faster)

**"Voice doesn't sound like Aizen"**
→ Try a different audio sample with clearer voice

---

## ⚡ Quick Start (If you have audio now)

```bash
# 1. Install
pip install TTS torch torchaudio

# 2. Prepare sample
python scripts/prepare_voice_samples.py -i your_aizen.mp3

# 3. Update config
# (Change engine to "coqui_tts" in config.yaml)

# 4. Run
python run_gui.py
```

**Total time**: ~15 minutes!

---

## 📝 Current Status

✅ System ready for voice cloning  
✅ Japanese phrases programmed  
✅ UI showing Bleach theme  
⏳ Waiting for voice sample  
⏳ TTS installation needed  

---

**Next**: Let's start with Step 1 - Installing TTS!
