"""Unit & integration tests for free media production suite (voiceover, image gen, video render)."""

import os

import pytest

from src.media.image_gen import generate_scene_image
from src.media.renderer import assemble_video
from src.media.voice import synthesize_voiceover


@pytest.mark.asyncio
async def test_voiceover_synthesis(tmp_path):
    """Test generating free EdgeTTS voiceover and subtitles."""
    audio_path = str(tmp_path / "test_narration.mp3")
    srt_path = str(tmp_path / "test_narration.srt")
    script_text = "Welcome to the future of AI documentary creation."

    result = await synthesize_voiceover(
        text=script_text,
        output_audio_path=audio_path,
        output_srt_path=srt_path,
        voice_key="en_male_doc"
    )

    assert result["status"] == "success"
    assert os.path.exists(audio_path)
    assert os.path.getsize(audio_path) > 0
    assert os.path.exists(srt_path)
    assert os.path.getsize(srt_path) > 0

def test_image_keyframe_generation(tmp_path):
    """Test image keyframe generation and fallback canvas."""
    img_path = str(tmp_path / "scene_1.png")
    prompt = "A futuristic AI supercomputer in a dark glowing cyber room"

    result = generate_scene_image(
        prompt=prompt,
        output_image_path=img_path,
        aspect_ratio="16:9"
    )

    assert result["status"] in ["success", "fallback_created"]
    assert os.path.exists(img_path)
    assert os.path.getsize(img_path) > 0

@pytest.mark.asyncio
async def test_full_video_scene_assembly(tmp_path):
    """Integration test: synthesize voiceover + generate image -> assemble MP4 video."""
    audio_path = str(tmp_path / "scene_voice.mp3")
    img_path = str(tmp_path / "scene_image.png")
    video_path = str(tmp_path / "output_short.mp4")

    # 1. Synthesize voice
    await synthesize_voiceover(
        text="This short video was produced completely autonomously.",
        output_audio_path=audio_path,
        voice_key="en_male_news"
    )
    assert os.path.exists(audio_path)

    # 2. Generate image
    generate_scene_image(
        prompt="Cyberpunk city skyline with glowing neon lights",
        output_image_path=img_path,
        aspect_ratio="9:16"
    )
    assert os.path.exists(img_path)

    # 3. Assemble video
    scenes = [{
        "narration": "This short video was produced completely autonomously.",
        "image_path": img_path,
        "audio_path": audio_path
    }]

    render_res = assemble_video(
        scenes=scenes,
        output_video_path=video_path,
        aspect_ratio="9:16",
        fps=15
    )

    assert render_res["status"] == "success"
    assert os.path.exists(video_path)
    assert os.path.getsize(video_path) > 0
