"""Trend Hunter Agent: Searches for viral news, AI topics, and trending documentary ideas."""

from typing import Any

from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException


def fetch_trending_topics(
    category: str = "technology AI documentary news",
    max_results: int = 5
) -> list[dict[str, Any]]:
    """
    Search for recent trending topics using free DuckDuckGo Search API.

    Args:
        category: Search query category.
        max_results: Maximum number of trending items to return.

    Returns:
        List of dicts containing title, snippet, and url.
    """
    trending_items = []
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(category, max_results=int(max_results)))
            for item in results:
                trending_items.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("body", ""),
                    "url": item.get("href", "")
                })
    except (DuckDuckGoSearchException, RuntimeError, OSError) as e:
        print(f"[Warning] DuckDuckGo search encountered an issue ({e}). Returning fallback trends.")
        trending_items = [
            {
                "title": "The Evolution of Quantum Computing",
                "snippet": "How quantum supremacy is transforming cryptography and AI.",
                "url": "https://example.com/quantum"
            },
            {
                "title": "The Forgotten AI Pioneer",
                "snippet": "The story of Alan Turing and the birth of modern computing.",
                "url": "https://example.com/turing"
            }
        ]

    return trending_items if trending_items else [
        {
            "title": "The Evolution of Quantum Computing",
            "snippet": "How quantum supremacy is transforming cryptography and AI.",
            "url": "https://example.com/quantum"
        }
    ]


def get_top_trending_topic(category: str = "latest AI breakthrough") -> str:
    """Convenience helper to return the single best trending topic title."""
    trends = fetch_trending_topics(category=category, max_results=1)
    if trends and "title" in trends[0]:
        return trends[0]["title"]
    return "The Future of Artificial Intelligence"
