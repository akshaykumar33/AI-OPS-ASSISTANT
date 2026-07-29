"""Autonomous AI Media Studio Pipeline: From trend/topic prompt to grounded rendered video."""

import asyncio
import json
import os
from typing import Any

from src.agents.storyboarder import generate_storyboard
from src.llm_client import generate_youtube_metadata
from src.media.image_gen import generate_scene_image
from src.media.renderer import assemble_video
from src.media.voice import synthesize_voiceover
from src.rag.researcher import generate_research_brief


def _write_json_file(path: str, data: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


async def create_video_from_topic(
    topic: str,
    output_dir: str = "data/outputs",
    format_type: str = "short",
    language: str = "en",
    enable_research: bool = True
) -> dict[str, Any]:
    """
    End-to-end autonomous video creation flow:
    Topic -> Grounded Research Brief -> Script & Storyboard -> Voiceover & Subtitles -> Image Keyframes -> Rendered Video MP4 -> YouTube SEO Metadata.

    Args:
        topic: Video topic or trend title.
        output_dir: Workspace directory for generated assets and final video.
        format_type: "short" (9:16) or "documentary" (16:9).
        language: "en" or "hi".
        enable_research: If True, performs grounded research (web search + RAG retrieval).

    Returns:
        Dict containing output video path, duration, title, and storyboard details.
    """
    research_summary = None
    if enable_research:
        print(f"[Studio] Step 1: Performing grounded research on '{topic}'...")
        research_res = generate_research_brief(topic)
        research_summary = research_res.get("research_summary")

    print(f"[Studio] Step 2: Generating storyboard for '{topic}'...")
    storyboard = generate_storyboard(
        topic,
        format_type=format_type,
        language=language,
        research_summary=research_summary
    )

    sanitized_title = "".join(c for c in topic if c.isalnum() or c in (" ", "_")).rstrip().replace(" ", "_").lower()
    project_dir = os.path.join(output_dir, sanitized_title)
    os.makedirs(project_dir, exist_ok=True)

    scenes_data = []
    aspect_ratio = "9:16" if format_type == "short" else "16:9"
    voice_key = storyboard.get("voice_key", "en_male_doc")

    for scene in storyboard.get("scenes", []):
        scene_num = scene["scene_num"]
        narration = scene["narration"]
        visual_prompt = scene["visual_prompt"]

        print(f"[Studio] Step 3.{scene_num}: Synthesizing voiceover...")
        audio_path = os.path.join(project_dir, f"scene_{scene_num}.mp3")
        srt_path = os.path.join(project_dir, f"scene_{scene_num}.srt")

        await synthesize_voiceover(
            text=narration,
            output_audio_path=audio_path,
            output_srt_path=srt_path,
            voice_key=voice_key
        )

        print(f"[Studio] Step 4.{scene_num}: Generating keyframe image...")
        img_path = os.path.join(project_dir, f"scene_{scene_num}.png")
        generate_scene_image(
            prompt=visual_prompt,
            output_image_path=img_path,
            aspect_ratio=aspect_ratio
        )

        scenes_data.append({
            "scene_num": scene_num,
            "narration": narration,
            "image_path": img_path,
            "audio_path": audio_path
        })

    print("[Studio] Step 5: Stitching scenes and rendering final video...")
    output_video_path = os.path.join(project_dir, f"{sanitized_title}_{format_type}.mp4")
    render_result = assemble_video(
        scenes=scenes_data,
        output_video_path=output_video_path,
        aspect_ratio=aspect_ratio
    )

    print("[Studio] Step 6: Generating YouTube SEO Growth Metadata...")
    script_summary_text = " ".join([s.get("narration", "") for s in scenes_data])
    youtube_metadata = generate_youtube_metadata(topic, script_summary=script_summary_text)

    metadata_path = os.path.join(project_dir, "youtube_metadata.json")
    await asyncio.to_thread(_write_json_file, metadata_path, youtube_metadata)

    return {
        "status": "completed",
        "title": storyboard.get("title", topic),
        "video_path": output_video_path,
        "format": format_type,
        "scenes_count": len(scenes_data),
        "research_used": research_summary is not None,
        "youtube_metadata": youtube_metadata,
        "render_details": render_result
    }


def run_studio_pipeline(
    topic: str,
    format_type: str = "short",
    language: str = "en",
    enable_research: bool = True
) -> dict[str, Any]:
    """Synchronous entrypoint for studio pipeline."""
    return asyncio.run(create_video_from_topic(
        topic,
        format_type=format_type,
        language=language,
        enable_research=enable_research
    ))
