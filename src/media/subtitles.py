"""Subtitle parsing & styled caption overlay generator for Shorts and AniDoc Documentaries."""

import os
import re
from typing import Any

from PIL import Image, ImageDraw


def parse_srt_file(srt_path: str) -> list[dict[str, Any]]:
    """
    Parse an .srt subtitle file into a list of timing cues.

    Args:
        srt_path: Path to .srt file.

    Returns:
        List of dicts containing index, start_sec, end_sec, and text.
    """
    if not os.path.exists(srt_path):
        return []

    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    subtitle_blocks = re.split(r"\n\s*\n", content.strip())
    cues = []

    for block in subtitle_blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            time_match = re.match(
                r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})",
                lines[1]
            )
            if time_match:
                h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, time_match.groups())
                start_sec = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000.0
                end_sec = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000.0
                text = " ".join(lines[2:])

                cues.append({
                    "start": start_sec,
                    "end": end_sec,
                    "text": text
                })

    return cues


def create_caption_overlay(
    text: str,
    target_size: tuple = (1920, 1080),
    style: str = "short"
) -> Image.Image:
    """
    Render styled text caption overlay image with semi-transparent background card.

    Args:
        text: Subtitle text string to draw.
        target_size: (width, height) canvas dimensions.
        style: "short" (bold yellow/white centered) or "documentary" (lower-third card).

    Returns:
        PIL Image with RGBA transparency layer containing the caption.
    """
    width, height = target_size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    if style == "short":
        # Centered bold viral shorts caption (e.g. 9:16)
        y_pos = int(height * 0.75)
        # Background box for high contrast readability
        margin = 60
        box_rect = [margin, y_pos - 30, width - margin, y_pos + 60]
        draw.rectangle(box_rect, fill=(0, 0, 0, 180), outline=(255, 215, 0), width=3)
        draw.text((width // 2, y_pos), text, fill=(255, 255, 0), anchor="mm")
    else:
        # Lower-third documentary caption (e.g. 16:9)
        y_pos = int(height * 0.85)
        box_rect = [100, y_pos - 25, width - 100, y_pos + 45]
        draw.rectangle(box_rect, fill=(15, 23, 42, 200), outline=(0, 200, 255), width=2)
        draw.text((width // 2, y_pos + 10), text, fill=(255, 255, 255), anchor="mm")

    return overlay
