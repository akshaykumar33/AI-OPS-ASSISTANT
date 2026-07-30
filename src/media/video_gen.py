"""AI video clip generation using Google Veo 3.1 with multi-tier fallback.

Tier 1: Veo 3.1 (veo-3.1-generate-preview) — Full cinematic AI-animated video clip
Tier 2: Veo 3.1 Fast (veo-3.1-fast-generate-preview) — Faster, slightly lower quality
Tier 3: Pollinations FLUX still image (fallback to Ken Burns motion in renderer)
"""

import os
import time
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.media.image_gen import generate_scene_image

load_dotenv()

# Veo models ordered by quality (best first)
VEO_MODELS = [
    "veo-3.1-generate-preview",
    "veo-3.1-fast-generate-preview",
]

# Maximum polling time per video generation (seconds)
VEO_MAX_POLL_SECONDS = 300
VEO_POLL_INTERVAL = 15


def _generate_veo_clip(
    prompt: str,
    output_video_path: str,
    aspect_ratio: str = "9:16",
) -> dict[str, Any] | None:
    """
    Attempt to generate a video clip via Google Veo 3.1.

    Returns dict with status/path on success, or None if all models fail.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[Veo] No GEMINI_API_KEY found. Skipping Veo generation.")
        return None

    client = genai.Client(api_key=api_key)

    for model_name in VEO_MODELS:
        try:
            print(f"[Veo] Generating video with model '{model_name}'...")
            operation = client.models.generate_videos(
                model=model_name,
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    aspect_ratio=aspect_ratio,
                ),
            )

            # Poll for completion with timeout
            elapsed = 0
            while not operation.done:
                if elapsed >= VEO_MAX_POLL_SECONDS:
                    print(f"[Veo] Timeout after {VEO_MAX_POLL_SECONDS}s on model '{model_name}'.")
                    break
                print(f"[Veo] Waiting for video... ({elapsed}s elapsed)")
                time.sleep(VEO_POLL_INTERVAL)
                elapsed += VEO_POLL_INTERVAL
                operation = client.operations.get(operation)

            if not operation.done:
                continue

            # Download and save the generated video
            generated_video = operation.response.generated_videos[0]
            client.files.download(file=generated_video.video)
            generated_video.video.save(output_video_path)

            file_size = os.path.getsize(output_video_path)
            print(f"[Veo] SUCCESS! Video saved ({file_size} bytes) via model '{model_name}'.")

            return {
                "status": "success",
                "media_path": output_video_path,
                "media_type": "video",
                "source": f"veo_{model_name}",
            }

        except Exception as e:  # noqa: BLE001
            error_msg = str(e)

            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"[Veo] Rate limited on '{model_name}': quota exhausted. Trying next...")
            elif "404" in error_msg or "NOT_FOUND" in error_msg:
                print(f"[Veo] Model '{model_name}' not available. Trying next...")
            else:
                print(f"[Veo] Error on '{model_name}': {e}. Trying next...")
            continue

    return None


def generate_scene_media(
    prompt: str,
    output_dir: str,
    scene_num: int,
    aspect_ratio: str = "9:16",
    style: str = "3d_animation",
) -> dict[str, Any]:
    """
    Generate the best available media for a scene — AI video clip (Veo) or still image (FLUX).

    This is the primary entry point for scene media generation. It tries Veo first
    for real animated video, then falls back to FLUX still images.

    Args:
        prompt: Scene visual description prompt.
        output_dir: Directory to save generated media.
        scene_num: Scene number (for filename).
        aspect_ratio: "9:16" for shorts or "16:9" for documentary.
        style: Visual style preset name.

    Returns:
        Dict with media_path, media_type ("video" or "image"), and source model.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Tier 1 & 2: Try Veo 3.1 AI video generation
    video_path = os.path.join(output_dir, f"scene_{scene_num}.mp4")
    cinematic_prompt = (
        f"{prompt}, {style}, cinematic quality, smooth animation, "
        "vibrant colors, 8k render, highly detailed, masterpiece"
    )

    veo_result = _generate_veo_clip(
        prompt=cinematic_prompt,
        output_video_path=video_path,
        aspect_ratio=aspect_ratio,
    )

    if veo_result is not None:
        return veo_result

    # Tier 3: Fallback to FLUX still image (Ken Burns motion applied in renderer)
    print(f"[Studio] Veo unavailable for scene {scene_num}. Falling back to FLUX image...")
    img_path = os.path.join(output_dir, f"scene_{scene_num}.png")
    luxury_prompt = (
        f"{prompt}, ultra detailed 3d pixar animation style, 8k render, "
        "vibrant lighting, highly expressive characters, polished masterpiece artwork"
    )

    img_result = generate_scene_image(
        prompt=luxury_prompt,
        output_image_path=img_path,
        aspect_ratio=aspect_ratio,
        style=style,
    )

    return {
        "status": img_result.get("status", "fallback_created"),
        "media_path": img_path,
        "media_type": "image",
        "source": img_result.get("source", "canvas_graphic"),
    }
