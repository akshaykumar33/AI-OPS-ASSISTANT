"""LangFlow / LangGraph Node Export Definitions for Visual Workflow Editing."""

from typing import Any

from src.agents.storyboarder import generate_storyboard
from src.rag.researcher import generate_research_brief


def research_node(inputs: dict[str, Any]) -> dict[str, Any]:
    """LangFlow / LangGraph Node: Grounded Research Brief Synthesis."""
    topic = inputs.get("topic", "AI Technology")
    res = generate_research_brief(topic)
    return {"research_summary": res.get("research_summary", "")}

def scriptwriter_node(inputs: dict[str, Any]) -> dict[str, Any]:
    """LangFlow / LangGraph Node: Scriptwriter & Director Storyboarder."""
    topic = inputs.get("topic", "AI Technology")
    research_summary = inputs.get("research_summary")
    format_type = inputs.get("format_type", "short")
    language = inputs.get("language", "en")

    storyboard = generate_storyboard(
        topic,
        format_type=format_type,
        language=language,
        research_summary=research_summary
    )
    return {"storyboard": storyboard}
