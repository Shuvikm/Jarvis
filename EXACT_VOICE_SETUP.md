# Getting EXACT Aizen Voice - Complete Guide

## 🎭 Voice Actor Clarification

**Aizen's Japanese Voice Actor**: **Shō Hayami (速水奨)**

Not Kenjiro Tsuda - that's a different voice actor. Aizen is voiced by Shō Hayami in the original Japanese anime.

## 🎯 What You Need

To get the **EXACT** anime voice saying authentic dialogue, you need:

1. **Audio from actual Bleach episodes** (Japanese dub)
2. **Voice cloning software** (we'll use RVC or Coqui TTS)
3. **15-30 seconds of clean Aizen dialogue**

---

## 📺 Step 1: Extract Audio from Bleach

### Method A: From Downloaded Episodes

If you have Bleach episodes:

```bash
# Install FFmpeg: https://ffmpeg.org/download.html

# Extract Aizen's voice (example timestamp)
ffmpeg -i "Bleach_Episode_309.mkv" -ss 00:12:30 -t 00:00:25 -vn aizen_sample.wav
```

**Best Episodes for Aizen**:
- Episode 60: Aizen's reveal (iconic scene!)
- Episode 309: Aizen vs Ichigo dialogue
- Episodes 291-299: Espada meetings
- Episode 308: Final transformation speeches

### Method B: Record from Streaming

1. Open Bleach on Crunchyroll/Netflix (with Japanese audio!)
2. Use Audacity or OBS to record system audio
3. Play a scene with clear Aizen dialogue
4. Save as WAV file

### Method C: YouTube Clips

```bash
# Install yt-dlp
pip install yt-dlp

# Download audio from clip
yt-dlp -x --audio-format mp3 "https://youtube.com/watch?v=XXXXX" -o aizen_clip.mp3
```

**Search for**: "Aizen Japanese voice" "Aizen Bleach Japanese" "Aizen Soul Society Japanese dub"

---

## 🎤 Step 2: Get Perfect Sample

### What Makes a Good Sample:

✅ **Perfect**:
- Aizen speaking clearly
- No background music
- No other characters talking
- Calm, measured dialogue (not shouting)
- 15-30 seconds long
- Japanese audio track

❌ **Avoid**:
- Battle scenes (too loud)
- Heavy music in background
- Multiple people talking
- English dub (we want Shō Hayami!)

### Recommended Scenes:

**Episode 60 (~5:30-6:00)**:
> "Itsu kara sakasama da to..." (When were you under the impression...)
> Perfect calm, dramatic Aizen

**Episode 309**:
> Philosophical conversation with Ichigo
> Clear, measured speech

---

## 🔧 Step 3: Prepare Audio Sample

```bash
cd c:\projects\JARVIS

# Process the audio
python scripts/prepare_voice_samples.py -i your_aizen_audio.mp3 -o voice_samples/aizen_voice.wav
```

This will:
- Convert to correct format
- Remove background noise
- Normalize volume
- Trim to optimal length

---

## 🎯 Step 4: Install Voice Cloning

### Option A: RVC (Recommended for Exact Voice)

```bash
# Download RVC: https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI

# Train on Aizen sample
# Output: Exact Shō Hayami voice model
```

### Option B: Coqui TTS (What we're using)

```bash
pip install coqui-tts torch torchaudio

# Test
python -c "from TTS.api import TTS; print('Ready!')"
```

---

## ⚙️ Step 5: Configure for Exact Voice

Edit `config.yaml`:

```yaml
voice:
  enabled: true
  engine: "coqui_tts"
  voice_model: "tts_models/multilingual/multi-dataset/your_tts"
  reference_audio: "voice_samples/aizen_voice.wav"
  language: "ja"  # Japanese for authentic pronunciation
  speed: 1.0
```

---

## 🗣️ Step 6: Use Authentic Dialogue

Create `voice_samples/authentic_dialogue.txt`:

```
よこそ私の世界へ (Yokoso watashino sekai e)
計画通り (Keikaku doori - All according to plan)
面白い (Omoshiroi - Interesting)  
完璧だ (Kanpeki da - Perfect)
いつから錯覚していた (Itsu kara sakasama da to - When were you under the impression...)
```

---

## 🧪 Step 7: Test Exact Voice

```bash
cd c:\projects\JARVIS

# Test with Japanese phrase
python -c "from voice_synthesis.aizen_voice import AizenVoice; v = AizenVoice(); v.speak('Yokoso watashino sekai e')"
```

**Expected**: Shō Hayami's voice saying "Welcome to my world" in Japanese!

---

## 🎬 The Result

After setup, when you run J.A.R.V.I.S.:

```
YOU: "Hello"
AIZEN: (In Shō Hayami's exact voice) "よこそ (Yokoso)..."
```

- **Same voice** as anime
- **Same pronunciation** 
- **Same modulation**
- **Authentic Japanese** when using Japanese words
- **Natural English** when using English

---

## 💡 Quick Start (RIGHT NOW)

**If you have a Bleach episode file**:

```bash
# 1. Extract 20 seconds of Aizen dialogue
ffmpeg -i your_bleach_episode.mkv -ss 00:05:30 -t 00:00:20 -vn aizen.wav

# 2. Prepare it
python scripts/prepare_voice_samples.py -i aizen.wav

# 3. Update config.yaml (change engine to "coqui_tts")

# 4. Run
python run_gui.py
```

**Don't have episodes?**
1. Find "Aizen Japanese voice" clip on YouTube
2. Note the URL
3. Run: `yt-dlp -x --audio-format wav "URL" -o aizen.wav`
4. Continue from step 2 above

---

## 📝 What Episode/Scene Do You Have Access To?

Tell me:
- Do you have Bleach episodes downloaded?
- Can you access Crunchyroll/Netflix?
- Or should I help you find YouTube clips?

I'll help you extract the perfect Aizen sample! 🌙

---

**Note**: Voice actor is **Shō Hayami (速水奨)**, not Kenjiro Suda. Make sure to use Japanese audio track!
