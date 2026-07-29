"""Automated video assembly & rendering pipeline with dynamic motion transforms & animated captions."""

import math
import os
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

from src.media.audio import apply_audio_ducking, create_ambient_bgm_track

try:
    # MoviePy v2 syntax
    from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
    IS_MOVIEPY_V2 = True
except ImportError:
    # MoviePy v1 fallback
    from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
    IS_MOVIEPY_V2 = False


def create_scene_clip(
    image_path: str,
    audio_path: str,
    narration_text: str = "",
    target_size: tuple[int, int] = (1080, 1920),
    camera_motion: str = "zoom_in"
):
    """
    Create an animated video scene clip combining keyframe image with voiceover audio,
    dynamic Ken Burns scale & pan camera motion, and animated neon subtitle cards.

    Args:
        image_path: Path to keyframe image.
        audio_path: Path to voiceover audio clip.
        narration_text: Scene caption text.
        target_size: (width, height) resolution tuple.
        camera_motion: "zoom_in", "zoom_out", or "pan_horizontal".

    Returns:
        MoviePy ImageClip configured with audio, motion, and captions.
    """
    audio_clip = AudioFileClip(audio_path)
    scene_duration = max(audio_clip.duration, 0.5)

    if IS_MOVIEPY_V2:
        img_clip = ImageClip(image_path).with_duration(scene_duration).resized(target_size)

        # Dynamic Camera Motion Transform & Subtitle Burn-In per frame
        def frame_transform(get_frame, t):
            frame = get_frame(t)  # NumPy RGB array
            img = Image.fromarray(frame)
            orig_w, orig_h = target_size
            progress = min(t / scene_duration, 1.0)

            # 1. Dynamic Motion Animation Modes
            if camera_motion == "zoom_in":
                # Smooth scale from 1.0x to 1.25x with upward center drift
                scale = 1.0 + 0.25 * progress
                new_w, new_h = int(orig_w * scale), int(orig_h * scale)
                resized_img = img.resize((new_w, new_h), Image.Resampling.BILINEAR)

                left = (new_w - orig_w) // 2
                top = int((new_h - orig_h) * (0.5 - 0.15 * progress))
                top = max(0, min(top, new_h - orig_h))
                img = resized_img.crop((left, top, left + orig_w, top + orig_h))

            elif camera_motion == "zoom_out":
                # Scale down from 1.25x to 1.02x with downward center drift
                scale = 1.25 - 0.23 * progress
                new_w, new_h = int(orig_w * scale), int(orig_h * scale)
                resized_img = img.resize((new_w, new_h), Image.Resampling.BILINEAR)

                left = (new_w - orig_w) // 2
                top = int((new_h - orig_h) * (0.35 + 0.15 * progress))
                top = max(0, min(top, new_h - orig_h))
                img = resized_img.crop((left, top, left + orig_w, top + orig_h))

            else:  # "pan_horizontal" or default
                # Scale to 1.22x and pan left to right
                scale = 1.22
                new_w, new_h = int(orig_w * scale), int(orig_h * scale)
                resized_img = img.resize((new_w, new_h), Image.Resampling.BILINEAR)

                max_left = new_w - orig_w
                left = int(max_left * progress)
                top = (new_h - orig_h) // 2
                img = resized_img.crop((left, top, left + orig_w, top + orig_h))

            # 2. Burn-In Styled Subtitle Card with Animated Neon Glow
            if narration_text:
                draw = ImageDraw.Draw(img)
                y_pos = int(orig_h * 0.80)
                margin = 40

                # Truncate caption for high-retention short reading
                display_text = narration_text if len(narration_text) < 75 else f"{narration_text[:72]}..."

                # Pulsing yellow neon border intensity
                pulse = math.sin(t * 8.0) * 0.5 + 0.5
                border_color = (int(255 * (0.8 + 0.2 * pulse)), int(215 * (0.8 + 0.2 * pulse)), 0)

                # Dark rounded rectangle box with neon stroke
                box_rect = [margin, y_pos - 30, orig_w - margin, y_pos + 50]
                draw.rectangle(box_rect, fill=(10, 15, 26), outline=border_color, width=5)
                draw.text((orig_w // 2, y_pos + 10), display_text, fill=(255, 255, 255), anchor="mm")

            return np.array(img)

        img_clip = img_clip.transform(frame_transform)
        img_clip = img_clip.with_audio(audio_clip)
    else:
        img_clip = ImageClip(image_path).set_duration(scene_duration).resize(target_size)
        img_clip = img_clip.set_audio(audio_clip)

    return img_clip


def assemble_video(
    scenes: list[dict[str, Any]],
    output_video_path: str,
    aspect_ratio: str = "9:16",
    fps: int = 24,
    enable_bgm: bool = True
) -> dict[str, Any]:
    """
    Stitch video scenes (keyframe images + voiceover audio clips + ducked BGM) into a final MP4 video.

    Args:
        scenes: List of scene dicts containing 'image_path', 'audio_path', 'narration', and 'camera_motion'.
        output_video_path: Path for output .mp4 file.
        aspect_ratio: "16:9" or "9:16".
        fps: Target frames per second.
        enable_bgm: If True, applies ambient background music with audio ducking.

    Returns:
        Dict with execution status and output video details.
    """
    out_dir = os.path.dirname(os.path.abspath(output_video_path))
    os.makedirs(out_dir, exist_ok=True)
    target_size = (1920, 1080) if aspect_ratio == "16:9" else (1080, 1920)

    video_clips = []
    motion_types = ["zoom_in", "pan_horizontal", "zoom_out"]

    for idx, scene in enumerate(scenes):
        image_path = scene["image_path"]
        audio_path = scene["audio_path"]
        narration = scene.get("narration", "")
        motion = scene.get("camera_motion", motion_types[idx % len(motion_types)])

        scene_clip = create_scene_clip(
            image_path=image_path,
            audio_path=audio_path,
            narration_text=narration,
            target_size=target_size,
            camera_motion=motion
        )
        video_clips.append(scene_clip)

    # Concatenate all scene clips smoothly
    final_clip = concatenate_videoclips(video_clips, method="compose")

    # Optionally generate and duck ambient BGM track
    if enable_bgm and final_clip.audio:
        bgm_path = os.path.join(out_dir, "ambient_bgm.wav")
        create_ambient_bgm_track(final_clip.duration, bgm_path)
        bgm_clip = AudioFileClip(bgm_path)
        ducked_audio = apply_audio_ducking(final_clip.audio, bgm_clip, ducked_volume=0.20)
        if IS_MOVIEPY_V2:
            final_clip = final_clip.with_audio(ducked_audio)
        else:
            final_clip = final_clip.set_audio(ducked_audio)

    temp_audio_file = os.path.join(out_dir, "temp_audio.m4a")

    # Render video file with explicit temp audio file path
    final_clip.write_videofile(
        output_video_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=temp_audio_file,
        remove_temp=True,
        preset="fast",
        threads=4,
        logger=None
    )

    total_dur = sum(c.duration for c in video_clips)

    # Close clips to free memory
    final_clip.close()

    # Clean up temp audio file if it remains
    if os.path.exists(temp_audio_file):
        try:
            os.remove(temp_audio_file)
        except OSError:
            pass

    return {
        "status": "success",
        "video_path": output_video_path,
        "duration": total_dur,
        "scenes_count": len(scenes),
        "aspect_ratio": aspect_ratio,
        "bgm_applied": enable_bgm
    }
