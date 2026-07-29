"""Storyboarder Agent: Generates viral, cinematic documentary storyboards using Master AI Producer directives."""

import json
import re
from typing import Any

from src.llm_client import ask
from src.prompts import MASTER_PRODUCER_SYSTEM_PROMPT


def generate_storyboard(
    topic: str,
    format_type: str = "short",
    language: str = "en",
    research_summary: str | None = None
) -> dict[str, Any]:
    """
    Generate viral documentary storyboard JSON for a video topic using Master AI Producer system instructions.

    Args:
        topic: The video subject/trend topic.
        format_type: "short" (9:16) or "documentary" (16:9).
        language: Language preference ("en" or "hi").
        research_summary: Optional grounded research brief.

    Returns:
        Dict containing title, scenes, and narration metadata.
    """
    context_str = f"\nFACTUAL RESEARCH GROUNDING:\n{research_summary}\n" if research_summary else ""
    prompt = (
        f"Topic: '{topic}'\n"
        f"Target Format: '{format_type}'\n"
        f"Language: '{language}'\n"
        f"{context_str}\n"
        "Execute the Master Producer Directives and generate a high-retention viral documentary JSON storyboard."
    )

    response_text = ask(
        prompt,
        system=MASTER_PRODUCER_SYSTEM_PROMPT,
        task_type="research_and_script"
    )

    # Clean markdown formatting wrappers if present
    cleaned_json = re.sub(r"^```json\s*", "", response_text.strip(), flags=re.MULTILINE)
    cleaned_json = re.sub(r"^```\s*", "", cleaned_json, flags=re.MULTILINE)
    cleaned_json = re.sub(r"\s*```$", "", cleaned_json, flags=re.MULTILINE).strip()

    try:
        storyboard_data = json.loads(cleaned_json)
        return storyboard_data
    except json.JSONDecodeError as e:
        print(f"[Warning] JSON decode failed ({e}). Raw response: {response_text}")
        return {
            "title": topic,
            "format": format_type,
            "voice_key": "en_male_doc" if language == "en" else "hi_male_doc",
            "scenes": [
                {
                    "scene_num": 1,
                    "narration": f"What they never told you about {topic} will change how you see the world.",
                    "visual_prompt": f"Dramatic cinematic close up of {topic}, dark moody lighting, volumetric fog, photorealistic 8k resolution, 35mm lens",
                    "camera_motion": "zoom_in"
                },
                {
                    "scene_num": 2,
                    "narration": "Behind closed doors, a dangerous decision was made that couldn't be undone.",
                    "visual_prompt": "Low angle shot of shadowy silhouette in a dimly lit high tech control room, neon rim light, 8k render",
                    "camera_motion": "pan_right"
                }
            ]
        }
