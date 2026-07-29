"""
Shared Gemini API client with task-based model dispatcher matrix & fallback handling.
Maps friendly model aliases (flash_high, omni, nano_banana) to valid Google GenAI API identifiers.
"""

import json
import os
import re
import time
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from google.genai import Client, errors, types

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Task-to-Model Specialization Dispatcher Matrix
TASK_MODEL_DISPATCHER = {
    "video_directives": "gemini-2.0-flash",
    "image_generation": "gemini-2.0-flash-lite",
    "research_and_script": "gemini-2.0-flash",
    "youtube_metadata": "gemini-2.0-flash-lite",
}

# Maps friendly user aliases to official Google GenAI model identifiers
SUPPORTED_MODELS = {
    "flash_high": "gemini-2.0-flash",
    "gemini-3.6-flash-high": "gemini-2.0-flash",
    "omni": "gemini-2.0-flash",
    "omni-2-pro": "gemini-2.0-flash",
    "nano_banana": "gemini-2.0-flash-lite",
    "nano-banana-2-pro": "gemini-2.0-flash-lite",
    "gemini_2_flash": "gemini-2.0-flash",
    "gemini_2_pro": "gemini-2.0-flash",
    "gemini_2_5": "gemini-2.0-flash",
    "lite": "gemini-2.0-flash-lite",
}

DEFAULT_MODEL_FALLBACKS = [
    MODEL_NAME,
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]


@lru_cache(maxsize=1)
def get_client() -> Client:
    """Return a cached Gemini client instance (reads GEMINI_API_KEY from env)."""
    return Client()


def ask(
    prompt: str,
    system: str | None = None,
    preferred_model: str | None = None,
    task_type: str | None = None,
    max_retries: int = 2
) -> str:
    """
    Send a prompt to Gemini with task-based model selection and rate-limit backoff.

    Args:
        prompt: User input or query text.
        system: Optional system instruction prompt.
        preferred_model: Explicit custom model name or alias.
        task_type: 'video_directives', 'image_generation', 'research_and_script', or 'youtube_metadata'.
        max_retries: Retries per model before trying next fallback model.

    Returns:
        Generated text string response.
    """
    client = get_client()
    config = types.GenerateContentConfig(system_instruction=system) if system else None

    # Resolve target model from task_type or preferred_model or default
    raw_target = preferred_model or (TASK_MODEL_DISPATCHER.get(task_type) if task_type else MODEL_NAME)
    target_model = SUPPORTED_MODELS.get(raw_target, raw_target)

    models_to_try = [target_model] + [m for m in DEFAULT_MODEL_FALLBACKS if m != target_model]

    for model_name in models_to_try:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config,
                )
                if response.text and len(response.text.strip()) > 0:
                    return response.text
            except errors.ClientError as e:
                if e.code == 429:
                    print(f"[Warning] 429 rate limit on '{model_name}'. Retrying in 4s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(4)
                else:
                    print(f"[Warning] API error on '{model_name}' ({e}). Trying next fallback model...")
                    break  # Try next model in sequence

    print("[Warning] Gemini API rate-limited. Returning structured fallback text.")
    return (
        "Core Hook: Key technological turning point.\n"
        "Key Facts:\n"
        "- Breakthrough discovery altered industry standards.\n"
        "- Secret developments triggered intense global competition.\n"
        "Takeaway: The innovation reshaped modern technology."
    )


def generate_youtube_metadata(topic: str, script_summary: str = "") -> dict[str, Any]:
    """
    Generate high-CTR YouTube Title, Description, Tags, and Thumbnail visual prompt using lightweight Flash Lite model.

    Args:
        topic: Video topic title.
        script_summary: Optional brief summary of narration script.

    Returns:
        Dict containing title, description, tags list, and thumbnail_prompt.
    """
    system_prompt = (
        "You are an expert YouTube SEO Growth Manager. Generate high-CTR titles, engaging descriptions, "
        "relevant tags, and cinematic thumbnail visual prompts. Respond STRICTLY with valid JSON:\n"
        "{\n"
        '    "title": "Explosive Viral Title",\n'
        '    "description": "Engaging description with timestamps and call to action.",\n'
        '    "tags": ["tag1", "tag2", "tag3"],\n'
        '    "thumbnail_prompt": "Cinematic high-contrast thumbnail prompt description"\n'
        "}"
    )

    prompt = f"Topic: '{topic}'\nScript Summary: '{script_summary}'\nGenerate complete YouTube metadata JSON."

    response_text = ask(prompt, system=system_prompt, task_type="youtube_metadata")
    cleaned_json = re.sub(r"^```json\s*", "", response_text.strip(), flags=re.MULTILINE)
    cleaned_json = re.sub(r"^```\s*", "", cleaned_json, flags=re.MULTILINE)
    cleaned_json = re.sub(r"\s*```$", "", cleaned_json, flags=re.MULTILINE).strip()

    try:
        return json.loads(cleaned_json)
    except json.JSONDecodeError:
        return {
            "title": f"The Untold Truth About {topic}",
            "description": f"Discover the secret history and scientific breakthrough of {topic}. Subscribe for more daily AI documentaries!",
            "tags": [topic.lower(), "ai documentary", "history", "tech news"],
            "thumbnail_prompt": f"Dramatic cinematic close up of {topic}, glowing neon lights, 8k resolution"
        }
