"""FastAPI router for Autonomous AI Media Studio video generation, trend discovery, and research endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.agents.trend_hunter import fetch_trending_topics
from src.rag.researcher import generate_research_brief
from src.studio import create_video_from_topic

router = APIRouter(prefix="/studio", tags=["AI Media Studio"])


class StudioVideoRequest(BaseModel):
    topic: str
    format_type: str = "short"  # "short" or "documentary"
    language: str = "en"
    enable_research: bool = True


class ResearchRequest(BaseModel):
    topic: str


@router.get("/trends")
def get_trends_endpoint(category: str = "AI technology news", max_results: int = 5) -> dict[str, Any]:
    """Fetch live trending video topic ideas using DuckDuckGo search."""
    try:
        topics = fetch_trending_topics(category=category, max_results=max_results)
        return {"status": "success", "category": category, "topics": topics}
    except (OSError, ValueError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trends: {e}") from e


@router.post("/research")
def research_endpoint(request: ResearchRequest) -> dict[str, Any]:
    """Generate NotebookLM-style grounded research brief for a topic."""
    if not request.topic.strip():
        raise HTTPException(status_code=422, detail="topic must not be empty")

    try:
        brief = generate_research_brief(request.topic)
        return brief
    except (OSError, ValueError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Research brief generation failed: {e}") from e


@router.post("/generate")
async def generate_video_endpoint(request: StudioVideoRequest) -> dict[str, Any]:
    """Trigger autonomous video generation flow (Topic -> Research -> Voice + Visuals -> MP4)."""
    if not request.topic.strip():
        raise HTTPException(status_code=422, detail="topic must not be empty")

    try:
        result = await create_video_from_topic(
            topic=request.topic,
            format_type=request.format_type,
            language=request.language,
            enable_research=request.enable_research
        )
        return result
    except (OSError, ValueError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Studio video generation failed: {e}") from e
