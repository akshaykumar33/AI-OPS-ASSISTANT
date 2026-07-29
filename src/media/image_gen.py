"""Cinematic image generation using latest Imagen 3 (Google GenAI) & FLUX.2 models with multi-model fallback."""

import os
import random
import urllib.parse
from typing import Any

import requests
from PIL import Image, ImageDraw

CINEMATIC_BOOSTERS = (
    "photorealistic 8k resolution, cinematic documentary still, 35mm lens, "
    "volumetric lighting, dramatic shadows, dark moody color grade, highly detailed texture, Octane Render"
)

# Latest generation models supported
POLLINATIONS_MODELS = ["flux", "flux-realism", "turbo"]


def generate_scene_image(
    prompt: str,
    output_image_path: str,
    aspect_ratio: str = "16:9",
    style: str = "cinematic"
) -> dict[str, Any]:
    """
    Generate ultra-high-quality cinematic visual keyframe with multi-model fallback.

    Tries:
    1. Google GenAI / Imagen 3 model (if GEMINI_API_KEY configured)
    2. Pollinations FLUX.2 & FLUX-Realism models
    3. Styled local fallback keyframe

    Args:
        prompt: Scene visual prompt description.
        output_image_path: Target path for output image file.
        aspect_ratio: "16:9" for documentary or "9:16" for shorts.
        style: Preset visual style name.

    Returns:
        Dict with status, image_path, dimensions, and source model.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_image_path)), exist_ok=True)
    width, height = (1920, 1080) if aspect_ratio == "16:9" else (1080, 1920)
    full_prompt = f"{prompt}, {style}, {CINEMATIC_BOOSTERS}"

    # 1. Attempt Google GenAI / Imagen 3 API if key present
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            result = client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=full_prompt,
                config={
                    "number_of_images": 1,
                    "aspect_ratio": "16:9" if aspect_ratio == "16:9" else "9:16",
                    "output_mime_type": "image/jpeg",
                },
            )
            if result and result.generated_images:
                image_bytes = result.generated_images[0].image.image_bytes
                with open(output_image_path, "wb") as f:
                    f.write(image_bytes)
                return {
                    "status": "success",
                    "image_path": output_image_path,
                    "width": width,
                    "height": height,
                    "source": "imagen-3.0-generate-002",
                }
        except (ImportError, Exception) as e:  # noqa: BLE001
            print(f"[Info] Imagen 3 API unavailable ({e}). Falling back to FLUX.2 models...")

    # 2. Multi-Model Fallback: Try Pollinations FLUX models
    encoded_prompt = urllib.parse.quote(full_prompt)
    seed = random.randint(1000, 999999)

    for model_name in POLLINATIONS_MODELS:
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={seed}&model={model_name}"
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200 and len(response.content) > 1000:
                with open(output_image_path, "wb") as f:
                    f.write(response.content)
                return {
                    "status": "success",
                    "image_path": output_image_path,
                    "width": width,
                    "height": height,
                    "source": f"pollinations_{model_name}",
                }
        except (requests.RequestException, OSError, ValueError) as e:
            print(f"[Warning] Pollinations model '{model_name}' timed out ({e}). Trying next model...")

    # 3. Fallback: Create dramatic high-contrast dark keyframe graphic
    bg_color = (10, 15, 26)
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    margin = 50
    draw.rectangle([margin, margin, width - margin, height - margin], outline=(0, 212, 255), width=6)
    draw.rectangle([margin + 12, margin + 12, width - margin - 12, height - margin - 12], outline=(255, 215, 0), width=2)

    text_to_draw = f"DOC SCENE: {prompt[:90]}..."
    draw.text((width // 2, height // 2), text_to_draw, fill=(255, 255, 255), anchor="mm")

    img.save(output_image_path)
    return {
        "status": "fallback_created",
        "image_path": output_image_path,
        "width": width,
        "height": height,
        "source": "cinematic_canvas",
    }
