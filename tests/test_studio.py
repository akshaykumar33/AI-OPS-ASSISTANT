"""Integration test for full end-to-end studio pipeline (studio.py)."""

import os

import pytest

from src.studio import create_video_from_topic


@pytest.mark.asyncio
async def test_full_studio_pipeline_short(tmp_path):
    """Test full pipeline execution for a short video."""
    out_dir = str(tmp_path / "studio_outputs")
    topic = "The History of Zero"

    result = await create_video_from_topic(
        topic=topic,
        output_dir=out_dir,
        format_type="short",
        language="en"
    )

    assert result["status"] == "completed"
    assert os.path.exists(result["video_path"])
    assert os.path.getsize(result["video_path"]) > 0
    assert result["scenes_count"] > 0
