"""
YouTube Video Auto-Uploader using official Google API Client.
Automatically uploads rendered studio MP4 videos with SEO metadata (Title, Description, Tags).
"""

import json
import os
from typing import Any


def upload_video_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list[str] | None = None,
    category_id: str = "28",  # Science & Technology category
    privacy_status: str = "private"  # 'private', 'unlisted', or 'public'
) -> dict[str, Any]:
    """
    Upload a rendered MP4 video to YouTube channel via Google YouTube Data API v3.

    Args:
        video_path: Local path to .mp4 video file.
        title: YouTube video title.
        description: Video description box text with timestamps.
        tags: List of SEO tag keywords.
        category_id: YouTube category ID ("28" = Science & Tech).
        privacy_status: 'private', 'unlisted', or 'public'.

    Returns:
        Dict containing status, video_id, and watch_url.
    """
    if not os.path.exists(video_path):
        return {"status": "error", "message": f"Video file not found at {video_path}"}

    effective_tags = tags or ["ai documentary", "technology", "shorts"]

    # Optional Google API Client import for live uploading
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        token_path = os.getenv("YOUTUBE_TOKEN_PATH", "data/credentials/youtube_token.json")
        if os.path.exists(token_path):
            with open(token_path, encoding="utf-8") as f:
                token_data = json.load(f)
            credentials = Credentials.from_authorized_user_info(token_data)
            youtube = build("youtube", "v3", credentials=credentials)

            body = {
                "snippet": {
                    "title": title[:100],
                    "description": description[:5000],
                    "tags": effective_tags,
                    "categoryId": category_id
                },
                "status": {
                    "privacyStatus": privacy_status
                }
            }

            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
            response = request.execute()

            video_id = response.get("id")
            return {
                "status": "success",
                "video_id": video_id,
                "watch_url": f"https://www.youtube.com/watch?v={video_id}",
                "privacy": privacy_status
            }
    except (ImportError, OSError, ValueError, KeyError, RuntimeError) as e:
        print(f"[Warning] Live YouTube API upload skipped ({e}). Prepared metadata for manual upload.")

    # Return upload manifest if live OAuth token is not configured yet
    return {
        "status": "prepared",
        "video_path": video_path,
        "title": title,
        "description": description,
        "tags": effective_tags,
        "privacy": privacy_status,
        "message": "YouTube upload manifest ready. Add youtube_token.json to enable automatic background publishing."
    }
