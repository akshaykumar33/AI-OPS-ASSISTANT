"""Unit & integration tests for Phase 4: Audio Ducking, BGM & Subtitle Styling."""

import os

from src.media.audio import create_ambient_bgm_track
from src.media.subtitles import create_caption_overlay, parse_srt_file


def test_ambient_bgm_generation(tmp_path):
    """Test creating an ambient audio BGM track."""
    bgm_path = str(tmp_path / "test_bgm.wav")
    result_path = create_ambient_bgm_track(duration=3.0, output_bgm_path=bgm_path)

    assert os.path.exists(result_path)
    assert os.path.getsize(result_path) > 0

def test_srt_parsing(tmp_path):
    """Test parsing .srt subtitle timestamps."""
    srt_path = str(tmp_path / "sample.srt")
    content = (
        "1\n"
        "00:00:00,100 --> 00:00:02,500\n"
        "Welcome to the AI revolution.\n\n"
        "2\n"
        "00:00:02,600 --> 00:00:05,000\n"
        "This is autonomous video production."
    )
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(content)

    cues = parse_srt_file(srt_path)
    assert len(cues) == 2
    assert cues[0]["start"] == 0.1
    assert cues[0]["text"] == "Welcome to the AI revolution."

def test_caption_overlay_creation():
    """Test creating styled caption PIL image overlay."""
    img = create_caption_overlay("Test Caption Line", target_size=(1920, 1080), style="short")
    assert img.size == (1920, 1080)
