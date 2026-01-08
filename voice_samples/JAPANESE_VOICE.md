# Voice Sample Requirements for Aizen

## ⚠️ Important: Correct Voice Actor

**Aizen's Japanese Voice**: **Shō Hayami (速水奨)**

NOT Kenjiro Tsuda - that's a different voice actor!

## Goal

Get the **EXACT** anime voice - Shō Hayami speaking as Aizen.

## What You Need

Extract audio from Japanese Bleach episodes with Aizen's dialogue.

### Method 1: From Video Files

If you have Bleach episodes:

```bash
python scripts/extract_audio.py "Bleach_Episode_60.mkv" --start 00:05:30 --duration 20
```

### Method 2: YouTube Clips

```bash
pip install yt-dlp
yt-dlp -x --audio-format wav "YOUTUBE_URL" -o aizen_clip.wav
```

Search: "Aizen Japanese voice" or "Aizen Soul Society Japanese"

## Best Episodes/Scenes

- **Episode 60** (~5:30): Aizen's reveal - PERFECT!
- **Episode 309** (~12:30): vs Ichigo dialogue
- **Episodes 291-299**: Espada meetings

## Requirements

✅ Japanese audio (Shō Hayami's voice)  
✅ Clear dialogue, minimal background music  
✅ 15-30 seconds  
✅ Calm speaking (not battle screams)

## After Extraction

```bash
# Prepare the sample
python scripts/prepare_voice_samples.py -i aizen_raw.wav

# Update config.yaml
# Change: engine: "coqui_tts"

# Run
python run_gui.py
```

**Result**: Exact Shō Hayami voice speaking your text!
