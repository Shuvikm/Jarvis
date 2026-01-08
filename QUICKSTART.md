# Quick Start Guide

## Run J.A.R.V.I.S. Now!

### Option 1: Interactive Mode
```bash
python main.py
```

Then type commands like:
- "Hello"
- "What time is it?"
- "What's the date?"
- "Help"
- "Goodbye"

### Option 2: Auto Demo
```bash
python main.py --test
```

Runs through all commands automatically.

### Option 3: Voice Demo
```bash
python demo.py
```

Press Enter to hear each of Aizen's signature phrases.

## Adding Aizen's Actual Voice

1. Get 15-30 seconds of Aizen speaking from Bleach
2. Save to `voice_samples/aizen_reference.wav`
3. Edit `config.yaml`:
   ```yaml
   voice:
     engine: "coqui_tts"
   ```
4. Install: `pip install TTS torch`
5. Run: `python main.py`

## Troubleshooting

**No sound?**
- Install pygame: `pip install pygame`
- Or use system default audio player

**Want better voice quality?**
- Use Coqui TTS with voice cloning (see above)

**Need help?**
- Read `README.md` for full documentation
- Check `walkthrough.md` for implementation details

---

**That's it! Your J.A.R.V.I.S. with Aizen's personality is ready!**
