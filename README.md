# J.A.R.V.I.S. with Aizen Voice

A personal AI assistant inspired by J.A.R.V.I.S. from Iron Man, speaking with the voice and personality of Aizen from Bleach anime.

## Features

- 🎤 **Text-to-Speech** with voice cloning capabilities
- 🧠 **Aizen Personality** - Intelligent, calculated responses
- ⏰ **Time & Date** queries
- 🔌 **Extensible Commands** - Easy to add new capabilities
- 🎯 **Multiple TTS Backends** - Coqui TTS, pyttsx3, gTTS

## Quick Start

### 1. Installation

```bash
# Clone or navigate to the project
cd c:\projects\JARVIS

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

**Note**: Some dependencies may take time to install, especially `torch` and `TTS`.

### 2. Basic Usage (Without Voice Cloning)

```bash
# Run in text mode
python main.py

# Test mode (automated demo)
python main.py --test
```

### 3. Adding Aizen's Voice (Optional)

To use voice cloning with Aizen's actual voice:

1. **Get Voice Samples**
   - Extract clean audio clips from Bleach anime (10-30 seconds)
   - Remove background music and sound effects
   - Save as WAV file: `voice_samples/aizen_reference.wav`

2. **Configure Voice Model**
   - Edit `config.yaml`
   - Set `voice.engine` to `"coqui_tts"`
   - Ensure `voice.reference_audio` points to your sample

3. **Run with Voice Cloning**
   ```bash
   python main.py
   ```

## Configuration

Edit `config.yaml` to customize:

```yaml
voice:
  engine: "pyttsx3"  # Change to coqui_tts for voice cloning
  reference_audio: "voice_samples/aizen_reference.wav"
  speed: 1.0
```

## Available Commands

- **Time**: "What time is it?"
- **Date**: "What's the date?"
- **Greeting**: "Hello" / "Hi"
- **Help**: "Help" / "What can you do?"
- **Exit**: "Goodbye" / "Exit" / "Quit"

## Voice Sample Preparation

### Option 1: Extract from Anime

1. Find a Bleach episode with clear Aizen dialogue
2. Use audio editing software (Audacity, Adobe Audition)
3. Extract 10-30 seconds of clean speech
4. Remove background music/effects
5. Save as `voice_samples/aizen_reference.wav`

### Option 2: Use Available Tools

We've included a voice preparation script:

```bash
python scripts/prepare_voice_samples.py --input your_audio.mp3 --output voice_samples/aizen_reference.wav
```

## Project Structure

```
JARVIS/
├── main.py                      # Main entry point
├── config.yaml                  # Configuration
├── requirements.txt             # Python dependencies
├── jarvis_core/
│   ├── assistant.py            # Main assistant logic
│   └── commands.py             # Command handlers
├── voice_synthesis/
│   ├── tts_engine.py           # TTS engine
│   └── aizen_voice.py          # Aizen personality
├── voice_samples/              # Voice reference audio
├── models/                     # Downloaded TTS models
├── cache/                      # Temporary audio files
└── logs/                       # Application logs
```

## Troubleshooting

### No Audio Output

**Windows**: Install pygame for audio playback
```bash
pip install pygame
```

### TTS Model Download Issues

If Coqui TTS fails to download models:
```bash
# Use offline mode with pyttsx3
# Edit config.yaml: voice.engine = "pyttsx3"
```

### Import Errors

Make sure you're in the project directory and virtual environment is activated:
```bash
cd c:\projects\JARVIS
venv\Scripts\activate
python main.py
```

## Advanced Usage

### Adding Custom Commands

Edit `jarvis_core/commands.py`:

```python
def my_custom_command(self, text: str) -> Dict[str, str]:
    """Your custom command."""
    return {
        'text': "Your response here",
        'context': 'custom'
    }

# Register in __init__
self.register_command("custom", self.my_custom_command, ["trigger phrase"])
```

### Voice Mode (Coming Soon)

Voice input with wake word detection:
```bash
python main.py --mode voice
```

## Privacy & Security

- ✅ All processing happens locally by default
- ✅ No data sent to cloud (unless using gTTS)
- ✅ Voice samples stored locally only
- ✅ No telemetry or analytics

## Legal Disclaimer

This project is for **personal use only**. Aizen's voice is portrayed by professional voice actors (Kyle Hebert in English, Shō Hayami in Japanese) and is copyrighted by Studio Pierrot/TV Tokyo. This implementation uses voice cloning for educational and personal entertainment purposes under fair use principles.

**Do Not**:
- Distribute cloned voice models
- Use commercially
- Impersonate voice actors
- Violate copyright laws

## Dependencies

Main dependencies:
- `TTS` - Coqui TTS for voice cloning
- `pyttsx3` - Offline text-to-speech
- `PyYAML` - Configuration management
- `torch` - Neural network backend

Full list in `requirements.txt`

## Contributing

This is a personal project but feel free to fork and customize for your own use!

## Credits

- Inspired by J.A.R.V.I.S. from Marvel's Iron Man
- Personality based on Aizen Sōsuke from Bleach
- Built with Coqui TTS and Python

## License

MIT License - See LICENSE file for details

---

**"All according to plan."** - Aizen
