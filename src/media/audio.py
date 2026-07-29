"""Audio processing module: Background Music (BGM) management & audio ducking."""

import os

import numpy as np

try:
    from moviepy import AudioFileClip, CompositeAudioClip
    IS_MOVIEPY_V2 = True
except ImportError:
    from moviepy.editor import AudioFileClip, CompositeAudioClip
    IS_MOVIEPY_V2 = False


def create_ambient_bgm_track(duration: float, output_bgm_path: str) -> str:
    """
    Generate a simple ambient drone/music track if no external BGM file is provided.

    Args:
        duration: Required duration in seconds.
        output_bgm_path: Destination path for .wav / .mp3 ambient track.

    Returns:
        Path to generated ambient track file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_bgm_path)), exist_ok=True)
    
    sample_rate = 44100
    total_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, total_samples, False)

    # Ambient drone synthesis (harmonic chord in A minor: 110Hz A2, 130.81Hz C3, 164.81Hz E3)
    tone = (
        0.3 * np.sin(2 * np.pi * 110.0 * t) +
        0.2 * np.sin(2 * np.pi * 130.81 * t) +
        0.2 * np.sin(2 * np.pi * 164.81 * t)
    )
    
    # Smooth fade in / fade out envelope
    fade_len = int(sample_rate * 1.5)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    
    tone[:fade_len] *= fade_in
    tone[-fade_len:] *= fade_out

    # Normalize to 16-bit audio PCM
    audio_data = (tone * 32767).astype(np.int16)

    try:
        import scipy.io.wavfile as wav
        wav.write(output_bgm_path, sample_rate, audio_data)
    except ImportError:
        # Fallback: simple byte write if scipy is not present
        with open(output_bgm_path, "wb") as f:
            f.write(audio_data.tobytes())

    return output_bgm_path


def apply_audio_ducking(
    narration_clip: AudioFileClip,
    bgm_clip: AudioFileClip,
    ducked_volume: float = 0.15
) -> CompositeAudioClip:
    """
    Combine voiceover narration with background music (BGM), ducking BGM volume under speech.

    Args:
        narration_clip: Main voiceover AudioFileClip.
        bgm_clip: Background music AudioFileClip.
        ducked_volume: Volume multiplier for BGM (0.15 = 15% volume).

    Returns:
        CompositeAudioClip containing mixed narration + ducked BGM.
    """
    min_duration = min(bgm_clip.duration, narration_clip.duration)

    if IS_MOVIEPY_V2:
        bgm_ducked = bgm_clip.subclipped(0, min_duration)
        bgm_ducked = bgm_ducked.with_volume_scaled(ducked_volume)
    else:
        bgm_ducked = bgm_clip.subclip(0, min_duration)
        bgm_ducked = bgm_ducked.volumex(ducked_volume)

    mixed_audio = CompositeAudioClip([narration_clip, bgm_ducked])
    return mixed_audio
