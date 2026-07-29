"""NotebookLM-Style Grounded Research Engine for Documentary & Script Writing."""

from typing import Any

from src.agents.trend_hunter import fetch_trending_topics
from src.llm_client import ask
from src.prompts import RESEARCHER_SYSTEM_PROMPT
from src.rag.retrieve import retrieve_chunks


def generate_research_brief(topic: str) -> dict[str, Any]:
    """
    Perform grounded research combining ChromaDB local docs & live web search snippets.

    Args:
        topic: The topic/concept to research.

    Returns:
        Dict containing topic, research_summary, and reference sources.
    """
    # 1. Retrieve local RAG knowledge
    local_chunks = retrieve_chunks(topic, k=3)
    local_context = "\n".join(local_chunks) if local_chunks else "No local document context available."

    # 2. Retrieve web search snippets
    web_results = fetch_trending_topics(category=topic, max_results=3)
    web_context = "\n".join([f"- {r['title']}: {r['snippet']}" for r in web_results])

    combined_context = f"--- LOCAL DOCUMENTS ---\n{local_context}\n\n--- WEB SEARCH RESULTS ---\n{web_context}"

    prompt = f"Topic: '{topic}'\n\nSynthesize the research context below into a structured documentary research brief:\n\n{combined_context}"

    research_summary = ask(
        prompt,
        system=RESEARCHER_SYSTEM_PROMPT,
        task_type="research_and_script"
    )

    return {
        "status": "success",
        "topic": topic,
        "research_summary": research_summary,
        "local_sources_count": len(local_chunks),
        "web_sources_count": len(web_results)
    }
