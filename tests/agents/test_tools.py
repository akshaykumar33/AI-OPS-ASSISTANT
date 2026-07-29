"""Tests for src/agents/tools.py."""
from unittest.mock import patch

from src.agents.tools import calculate, execute_tool, search_documents


def test_calculate_basic_multiplication():
    assert calculate("47 * 89") == "4183"


def test_calculate_handles_parentheses_and_division():
    assert calculate("(12 + 3) / 5") == "3.0"


def test_calculate_rejects_unsafe_expression():
    """Anything that isn't plain arithmetic (e.g. attempted code execution) should
    return an error message, never actually execute."""
    result = calculate("__import__('os').system('echo hi')")
    assert result.startswith("Error evaluating")


def test_calculate_handles_invalid_syntax():
    result = calculate("2 + ")
    assert result.startswith("Error evaluating")


@patch("src.rag.retrieve.retrieve_chunks")
def test_search_documents_returns_joined_chunks(mock_retrieve):
    mock_retrieve.return_value = ["chunk one", "chunk two"]
    result = search_documents("some query")
    assert result == "chunk one\n---\nchunk two"


@patch("src.rag.retrieve.retrieve_chunks")
def test_search_documents_handles_no_results(mock_retrieve):
    mock_retrieve.return_value = []
    result = search_documents("some query")
    assert result == "No relevant documents found for this query."


def test_execute_tool_dispatches_to_calculate():
    result = execute_tool("calculate", {"expression": "2 + 2"})
    assert result == "4"


def test_execute_tool_unknown_tool_returns_error():
    result = execute_tool("not_a_real_tool", {})
    assert result == "Error: unknown tool 'not_a_real_tool'"


def test_execute_tool_catches_exceptions_from_tool():
    """Missing/wrong args should be caught and reported, not raised."""
    result = execute_tool("calculate", {"wrong_arg_name": "2+2"})
    assert result.startswith("Error running tool 'calculate'")
