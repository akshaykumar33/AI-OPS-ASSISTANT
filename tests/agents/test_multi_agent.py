"""Tests for src/agents/multi_agent.py.

Mocks run_agent() and ask() so the pipeline logic (revision loop,
approval parsing) is verified without real API calls.
"""
from unittest.mock import patch

from src.agents.multi_agent import researcher, reviewer, run_pipeline, writer


@patch("src.agents.multi_agent.run_agent")
def test_researcher_calls_run_agent_with_task(mock_run_agent):
    mock_run_agent.return_value = "- fact one\n- fact two"

    result = researcher("population of France")

    assert result == "- fact one\n- fact two"
    mock_run_agent.assert_called_once()
    prompt_sent = mock_run_agent.call_args.args[0]
    assert "population of France" in prompt_sent


@patch("src.agents.multi_agent.ask")
def test_writer_builds_prompt_with_findings(mock_ask):
    mock_ask.return_value = "Here is the draft."

    result = writer("What is X?", "- finding one\n- finding two")

    assert result == "Here is the draft."
    call_args = mock_ask.call_args
    prompt = call_args.args[0]
    assert "What is X?" in prompt
    assert "finding one" in prompt
    assert "feedback" not in prompt.lower()


@patch("src.agents.multi_agent.ask")
def test_writer_includes_feedback_when_revising(mock_ask):
    mock_ask.return_value = "Revised draft."

    writer("What is X?", "- finding one", feedback="Add more detail on Y")

    prompt = mock_ask.call_args.args[0]
    assert "Add more detail on Y" in prompt


@patch("src.agents.multi_agent.ask")
def test_reviewer_parses_approved(mock_ask):
    mock_ask.return_value = "APPROVED"

    approved, feedback = reviewer("task", "findings", "draft")

    assert approved is True
    assert feedback == ""


@patch("src.agents.multi_agent.ask")
def test_reviewer_parses_revise_feedback(mock_ask):
    mock_ask.return_value = "REVISE: The draft misses the second finding."

    approved, feedback = reviewer("task", "findings", "draft")

    assert approved is False
    assert feedback == "The draft misses the second finding."


@patch("src.agents.multi_agent.writer")
@patch("src.agents.multi_agent.reviewer")
@patch("src.agents.multi_agent.researcher")
def test_pipeline_returns_draft_when_approved_first_try(mock_researcher, mock_reviewer, mock_writer):
    mock_researcher.return_value = "findings"
    mock_writer.return_value = "first draft"
    mock_reviewer.return_value = (True, "")

    result = run_pipeline("some task")

    assert result == "first draft"
    assert mock_writer.call_count == 1  # never had to revise
    assert mock_reviewer.call_count == 1


@patch("src.agents.multi_agent.writer")
@patch("src.agents.multi_agent.reviewer")
@patch("src.agents.multi_agent.researcher")
def test_pipeline_revises_then_returns_approved_draft(mock_researcher, mock_reviewer, mock_writer):
    mock_researcher.return_value = "findings"
    mock_writer.side_effect = ["first draft", "revised draft"]
    mock_reviewer.side_effect = [(False, "needs work"), (True, "")]

    result = run_pipeline("some task")

    assert result == "revised draft"
    assert mock_writer.call_count == 2
    assert mock_reviewer.call_count == 2


@patch("src.agents.multi_agent.writer")
@patch("src.agents.multi_agent.reviewer")
@patch("src.agents.multi_agent.researcher")
def test_pipeline_stops_at_max_revisions_and_returns_last_draft(mock_researcher, mock_reviewer, mock_writer):
    """If the reviewer never approves, the pipeline must still return
    something rather than looping forever or raising."""
    mock_researcher.return_value = "findings"
    mock_writer.side_effect = ["draft 1", "draft 2", "draft 3"]
    mock_reviewer.return_value = (False, "still not good enough")

    result = run_pipeline("some task", max_revisions=2)

    assert result == "draft 3"
    assert mock_writer.call_count == 3  # initial + 2 revisions
    assert mock_reviewer.call_count == 2
