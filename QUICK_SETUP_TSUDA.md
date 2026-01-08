# Complete Setup for Kenjiro Tsuda Voice

## 🎯 What You Need

1. **Kenjiro Tsuda voice sample** (15-30 seconds)
2. **TTS library** installed
3. **Updated configuration**

---

## 📥 Step-by-Step Setup

### Step 1: Get Kenjiro Tsuda Voice

**Recommended YouTube videos** (found via search):
- "Kenjiro Tsuda voice compilation"
- "Nanami Kento Japanese voice" (Jujutsu Kaisen)
- "津田健次郎 voice" compilations

**Download method**:
1. Go to: https://y2mate.com
2. Paste YouTube URL
3. Download as WAV or MP3
4. Save to: `c:\projects\JARVIS\voice_samples\kenjiro_tsuda.wav`

### Step 2: Install Voice Cloning

```bash
cd c:\projects\JARVIS

# Install TTS (this may take 5-10 minutes)
pip install TTS torch torchaudio

# Verify installation
python -c "from TTS.api import TTS; print('TTS installed successfully!')"
```

### Step 3: Prepare Voice Sample

```bash
# After you have kenjiro_tsuda.wav in voice_samples/
python scripts/prepare_voice_samples.py -i voice_samples/kenjiro_tsuda.wav -o voice_samples/tsuda_reference.wav
```

### Step 4: Enable Voice Cloning

```bash
# Quick enable script
python scripts/enable_voice_cloning.py voice_samples/tsuda_reference.wav
```

OR manually edit `config.yaml`:
```yaml
voice:
  engine: "coqui_tts"
  reference_audio: "voice_samples/tsuda_reference.wav"
```

### Step 5: Test!

```bash
# Run the GUI
python run_gui.py
```

**Expected**: J.A.R.V.I.S. speaks with Kenjiro Tsuda's voice!

---

## ✅ Full Functionality Checklist

- [ ] Download Kenjiro Tsuda audio
- [ ] Save to voice_samples/kenjiro_tsuda.wav  
- [ ] Install TTS: `pip install TTS torch`
- [ ] Prepare: `python scripts/prepare_voice_samples.py -i voice_samples/kenjiro_tsuda.wav`
- [ ] Enable: `python scripts/enable_voice_cloning.py`
- [ ] Test: `python run_gui.py`

---

## 🎤 Best Kenjiro Tsuda Sources

1. **Jujutsu Kaisen** - Nanami Kento
   - Professional, calm dialogue
   - Clear audio

2. **Interviews**
   - Natural speaking voice
   - Usually clear audio

3. **Game voice lines**
   - Crystal clear
   - No background music

---

## 💡 After Voice Cloning Works

Your system will have:
- ✅ Bleach UI
- ✅ Kenjiro Tsuda's voice
- ✅ AI responses
- ✅ Speech recognition
- ✅ All automation features
- ✅ **100% functional!**

---

**Note**: TTS installation might fail if you don't have enough space or proper Python version. Make sure you have Python 3.8+ and at least 2GB free space.
