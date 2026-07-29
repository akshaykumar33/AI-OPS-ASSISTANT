"""Voiceover synthesis using 100% free Microsoft Edge Neural TTS voices via edge-tts."""

import asyncio
import os
from typing import Any

import edge_tts

# Popular high-quality free neural voices
DEFAULT_VOICES = {
    "deep_bass_male": "en-US-ChristopherNeural",   # Very deep bass documentary narrator
    "en_male_doc": "en-US-ChristopherNeural",       # Deep documentary narrator
    "en_male_news": "en-US-GuyNeural",               # Energetic news/explainer
    "en_female_doc": "en-US-AvaNeural",              # Clear female narrator
    "hi_male_doc": "hi-IN-MadhurNeural",             # Hindi male narrator
    "hi_female_doc": "hi-IN-SwaraNeural",            # Hindi female narrator
}


def _write_bytes_file(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def _write_text_file(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


async def synthesize_voiceover(
    text: str,
    output_audio_path: str,
    output_srt_path: str | None = None,
    voice_key: str = "deep_bass_male",
    rate: str = "+5%",
    pitch: str = "-8Hz",
    max_retries: int = 3
) -> dict[str, Any]:
    """
    Synthesize high-quality neural voiceover audio with deep bass pitch and subtitle generation.

    Args:
        text: Script narration text to speak.
        output_audio_path: Target path for .mp3 output audio.
        output_srt_path: Optional path to save timestamped .srt file.
        voice_key: Key from DEFAULT_VOICES or raw edge-tts voice string.
        rate: TTS speed rate modification string.
        pitch: Deep bass pitch adjustment (e.g. '-8Hz').
        max_retries: Retry attempts on network DNS blips.

    Returns:
        Dict with status, audio_path, srt_path, and voice used.
    """
    voice_name = DEFAULT_VOICES.get(voice_key, voice_key)
    os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)

    for attempt in range(max_retries):
        try:
            submaker = edge_tts.SubMaker()
            communicate = edge_tts.Communicate(text, voice_name, rate=rate, pitch=pitch)

            audio_chunks = []
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_chunks.append(chunk["data"])
                else:
                    submaker.feed(chunk)

            full_audio_data = b"".join(audio_chunks)
            await asyncio.to_thread(_write_bytes_file, output_audio_path, full_audio_data)

            result_info = {
                "status": "success",
                "audio_path": output_audio_path,
                "voice": voice_name,
                "srt_path": None
            }

            if output_srt_path:
                os.makedirs(os.path.dirname(os.path.abspath(output_srt_path)), exist_ok=True)
                srt_content = submaker.get_srt()
                await asyncio.to_thread(_write_text_file, output_srt_path, srt_content)
                result_info["srt_path"] = output_srt_path

            return result_info
        except (OSError, RuntimeError, TimeoutError, ValueError) as e:
            if attempt < max_retries - 1:
                print(f"[Warning] Voiceover TTS network retry ({attempt + 1}/{max_retries}): {e}")
                await asyncio.sleep(2)
            else:
                print(f"[Warning] Edge-TTS failed after {max_retries} retries ({e}).")

    return {
        "status": "failed",
        "audio_path": output_audio_path,
        "voice": voice_name,
        "srt_path": None
    }


def generate_voiceover_sync(
    text: str,
    output_audio_path: str,
    output_srt_path: str | None = None,
    voice_key: str = "deep_bass_male"
) -> dict[str, Any]:
    """Synchronous wrapper for synthesize_voiceover."""
    return asyncio.run(synthesize_voiceover(text, output_audio_path, output_srt_path, voice_key))
