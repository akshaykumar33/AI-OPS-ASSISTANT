"""Tests for src/llm_client.py.

Mocks the Gemini client so tests don't need a real API key or network call.
"""
from unittest.mock import MagicMock, patch

from src.llm_client import ask


@patch("src.llm_client.get_client")
def test_ask_returns_response_text(mock_get_client):
    mock_response = MagicMock()
    mock_response.text = "This is the answer."

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client

    result = ask("What is 2+2?")

    assert result == "This is the answer."
    mock_client.models.generate_content.assert_called_once()
    call_kwargs = mock_client.models.generate_content.call_args.kwargs
    assert call_kwargs["contents"] == "What is 2+2?"
    assert call_kwargs["config"] is None


@patch("src.llm_client.get_client")
def test_ask_includes_system_instruction_when_provided(mock_get_client):
    mock_response = MagicMock()
    mock_response.text = "Answer with context."

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client

    result = ask("A question", system="You are helpful.")

    assert result == "Answer with context."
    call_kwargs = mock_client.models.generate_content.call_args.kwargs
    assert call_kwargs["config"] is not None
    assert call_kwargs["config"].system_instruction == "You are helpful."
