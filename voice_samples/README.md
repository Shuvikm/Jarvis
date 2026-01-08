# Voice Samples Directory

This directory is for storing voice reference audio files for voice cloning.

## Getting Aizen's Voice Sample

To use voice cloning with Aizen's voice, you need a clean audio sample (10-30 seconds).

### Method 1: Extract from Anime

1. **Find Clear Dialogue**
   - Find a Bleach episode with Aizen speaking clearly
   - Look for scenes with minimal background music
   - Avoid battle scenes with sound effects

2. **Extract Audio**
   - Use a video player to note the timestamp
   - Use FFmpeg or audio extraction tool:
     ```bash
     ffmpeg -i bleach_episode.mp4 -ss 00:01:30 -t 00:00:15 -vn aizen_raw.wav
     ```

3. **Clean Audio** (using Audacity or similar)
   - Remove background noise
   - Normalize volume
   - Trim silence at start/end
   - Export as WAV (22050Hz or higher)

4. **Save Here**
   - Save as `aizen_reference.wav`
   - Update path in `config.yaml`

### Method 2: Use the Preparation Script

```bash
python scripts/prepare_voice_samples.py --input your_audio.mp3
```

This will:
- Convert to proper format
- Attempt noise reduction
- Normalize audio levels
- Save to `voice_samples/aizen_reference.wav`

## Audio Requirements

- **Format**: WAV recommended (MP3 also works)
- **Sample Rate**: 22050Hz or higher
- **Duration**: 10-30 seconds ideal
- **Quality**: Clear speech, minimal background noise
- **Mono/Stereo**: Either works (will be converted if needed)

## Voice Actors

**English Dub**: Kyle Hebert  
**Japanese Original**: Shō Hayami

You can use samples from either version depending on your preference.

## Legal Notice

Voice samples should only be used for personal, non-commercial purposes. Do not distribute the cloned voice models or use them to impersonate the voice actors.

## Tips for Best Results

1. **Clarity is Key**: Choose clips with very clear dialogue
2. **Consistent Tone**: Pick a clip with Aizen's typical calm, confident tone
3. **No Shouting**: Avoid battle scenes where he's yelling
4. **Length**: 15-20 seconds is the sweet spot
5. **Multiple Samples**: You can provide multiple reference files for better cloning

## Example Sources

Good scenes to extract from Bleach:
- Aizen's reveal in Soul Society arc
- His conversations with the Espada
- His monologues about his plans
- Any calm, calculated dialogue scenes

---

Once you have your `aizen_reference.wav` file here, update `config.yaml`:

```yaml
voice:
  engine: "coqui_tts"
  reference_audio: "voice_samples/aizen_reference.wav"
```
