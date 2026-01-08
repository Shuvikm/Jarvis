"""Script to prepare voice samples for TTS voice cloning."""

import argparse
import logging
from pathlib import Path
import sys

try:
    import soundfile as sf
    import librosa
    import numpy as np
    from scipy.io import wavfile
except ImportError:
    print("Error: Required audio libraries not installed.")
    print("Install with: pip install soundfile librosa scipy")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_audio(input_path: str) -> tuple:
    """Load audio file.
    
    Args:
        input_path: Path to input audio
        
    Returns:
        Tuple of (audio_data, sample_rate)
    """
    logger.info(f"Loading audio from: {input_path}")
    
    try:
        # Load with librosa (handles multiple formats)
        audio, sr = librosa.load(input_path, sr=None, mono=False)
        logger.info(f"Loaded audio: {audio.shape}, Sample rate: {sr}Hz")
        return audio, sr
    except Exception as e:
        logger.error(f"Failed to load audio: {e}")
        raise


def convert_to_mono(audio: np.ndarray) -> np.ndarray:
    """Convert stereo to mono if needed.
    
    Args:
        audio: Audio data
        
    Returns:
        Mono audio
    """
    if len(audio.shape) > 1:
        logger.info("Converting stereo to mono")
        audio = librosa.to_mono(audio)
    return audio


def normalize_audio(audio: np.ndarray) -> np.ndarray:
    """Normalize audio levels.
    
    Args:
        audio: Audio data
        
    Returns:
        Normalized audio
    """
    logger.info("Normalizing audio levels")
    
    # Normalize to -3dB to avoid clipping
    max_val = np.abs(audio).max()
    if max_val > 0:
        target_peak = 0.7  # -3dB
        audio = audio * (target_peak / max_val)
    
    return audio


def reduce_noise(audio: np.ndarray, sr: int) -> np.ndarray:
    """Simple noise reduction.
    
    Args:
        audio: Audio data
        sample_rate: Sample rate
        
    Returns:
        Noise-reduced audio
    """
    logger.info("Applying basic noise reduction")
    
    # Simple noise gate - reduce very quiet parts
    threshold = 0.01  # Adjust as needed
    audio = np.where(np.abs(audio) < threshold, audio * 0.1, audio)
    
    return audio


def trim_silence(audio: np.ndarray, sr: int, threshold: int = 20) -> np.ndarray:
    """Trim silence from start and end.
    
    Args:
        audio: Audio data
        sr: Sample rate
        threshold: Silence threshold in dB
        
    Returns:
        Trimmed audio
    """
    logger.info("Trimming silence")
    
    audio_trimmed, _ = librosa.effects.trim(audio, top_db=threshold)
    return audio_trimmed


def resample_audio(audio: np.ndarray, orig_sr: int, target_sr: int = 22050) -> tuple:
    """Resample audio to target sample rate.
    
    Args:
        audio: Audio data
        orig_sr: Original sample rate
        target_sr: Target sample rate
        
    Returns:
        Tuple of (resampled_audio, target_sr)
    """
    if orig_sr != target_sr:
        logger.info(f"Resampling from {orig_sr}Hz to {target_sr}Hz")
        audio = librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)
    
    return audio, target_sr


def save_audio(audio: np.ndarray, sr: int, output_path: str):
    """Save audio to file.
    
    Args:
        audio: Audio data
        sr: Sample rate
        output_path: Output file path
    """
    logger.info(f"Saving to: {output_path}")
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save as WAV
    sf.write(output_path, audio, sr)
    logger.info("Audio saved successfully")


def prepare_voice_sample(
    input_path: str,
    output_path: str = "voice_samples/aizen_reference.wav",
    target_sr: int = 22050,
    apply_noise_reduction: bool = True
):
    """Prepare voice sample for TTS voice cloning.
    
    Args:
        input_path: Path to input audio file
        output_path: Path to save processed audio
        target_sr: Target sample rate
        apply_noise_reduction: Whether to apply noise reduction
    """
    try:
        # Load audio
        audio, sr = load_audio(input_path)
        
        # Convert to mono
        audio = convert_to_mono(audio)
        
        # Trim silence
        audio = trim_silence(audio, sr)
        
        # Noise reduction (optional)
        if apply_noise_reduction:
            audio = reduce_noise(audio, sr)
        
        # Normalize
        audio = normalize_audio(audio)
        
        # Resample
        audio, sr = resample_audio(audio, sr, target_sr)
        
        # Save
        save_audio(audio, sr, output_path)
        
        # Print info
        duration = len(audio) / sr
        logger.info(f"\n{'='*50}")
        logger.info(f"Processing complete!")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Sample rate: {sr}Hz")
        logger.info(f"Output: {output_path}")
        logger.info(f"{'='*50}\n")
        
        if duration < 5:
            logger.warning("Warning: Audio is very short (<5s). Consider using a longer sample.")
        elif duration > 60:
            logger.warning("Warning: Audio is very long (>60s). Consider trimming to 15-30 seconds.")
        else:
            logger.info("Duration is good for voice cloning!")
        
    except Exception as e:
        logger.error(f"Failed to prepare voice sample: {e}")
        raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Prepare voice samples for TTS voice cloning'
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input audio file (WAV, MP3, etc.)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='voice_samples/aizen_reference.wav',
        help='Output file path (default: voice_samples/aizen_reference.wav)'
    )
    
    parser.add_argument(
        '--sample-rate', '-sr',
        type=int,
        default=22050,
        help='Target sample rate (default: 22050)'
    )
    
    parser.add_argument(
        '--no-noise-reduction',
        action='store_true',
        help='Skip noise reduction step'
    )
    
    args = parser.parse_args()
    
    # Check input file exists
    if not Path(args.input).exists():
        logger.error(f"Input file not found: {args.input}")
        return 1
    
    # Prepare sample
    prepare_voice_sample(
        input_path=args.input,
        output_path=args.output,
        target_sr=args.sample_rate,
        apply_noise_reduction=not args.no_noise_reduction
    )
    
    logger.info("\nNow update config.yaml:")
    logger.info(f"  voice.reference_audio: \"{args.output}\"")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
