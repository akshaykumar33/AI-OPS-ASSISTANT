"""Unit & integration tests for Phase 3: Trend Hunter & Grounded RAG Research Engine."""

import pytest

from src.agents.trend_hunter import fetch_trending_topics, get_top_trending_topic
from src.rag.researcher import generate_research_brief


def test_fetch_trending_topics():
    """Test DuckDuckGo trend scraper."""
    topics = fetch_trending_topics(category="AI tech news", max_results=2)
    assert isinstance(topics, list)
    assert len(topics) > 0
    assert "title" in topics[0]

def test_get_top_trending_topic():
    """Test retrieving top trending topic title."""
    title = get_top_trending_topic("quantum computing")
    assert isinstance(title, str)
    assert len(title) > 0

@pytest.mark.asyncio
async def test_generate_research_brief():
    """Test NotebookLM-style grounded research brief synthesis."""
    topic = "The History of Artificial Intelligence"
    res = generate_research_brief(topic)

    assert res["status"] == "success"
    assert res["topic"] == topic
    assert "research_summary" in res
    assert len(res["research_summary"]) > 0
