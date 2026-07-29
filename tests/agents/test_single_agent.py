"""Tests for src/agents/single_agent.py.

Mocks the Gemini client entirely so the agent LOOP logic (when to stop,
how tool results get fed back, the max_steps safety limit) is verified
without any real API calls.
"""
from unittest.mock import MagicMock, patch

from src.agents.single_agent import run_agent


def _text_response(text):
    """Build a fake response with no function calls - a final answer."""
    response = MagicMock()
    response.function_calls = None
    response.text = text
    response.candidates = [MagicMock(content=MagicMock())]
    return response


def _tool_call_response(tool_name, args):
    """Build a fake response requesting one tool call."""
    call = MagicMock()
    call.name = tool_name
    call.args = args

    response = MagicMock()
    response.function_calls = [call]
    response.candidates = [MagicMock(content=MagicMock())]
    return response


@patch("src.agents.single_agent.execute_tool")
@patch("src.agents.single_agent.get_client")
def test_agent_returns_immediately_when_no_tool_needed(mock_get_client, mock_execute_tool):
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = _text_response("The answer is 42.")
    mock_get_client.return_value = mock_client

    result = run_agent("What is the meaning of life?")

    assert result == "The answer is 42."
    mock_execute_tool.assert_not_called()
    assert mock_client.models.generate_content.call_count == 1


@patch("src.agents.single_agent.execute_tool")
@patch("src.agents.single_agent.get_client")
def test_agent_calls_tool_then_returns_final_answer(mock_get_client, mock_execute_tool):
    mock_execute_tool.return_value = "4183"

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = [
        _tool_call_response("calculate", {"expression": "47 * 89"}),
        _text_response("47 times 89 is 4183."),
    ]
    mock_get_client.return_value = mock_client

    result = run_agent("What is 47 * 89?")

    assert result == "47 times 89 is 4183."
    mock_execute_tool.assert_called_once_with("calculate", {"expression": "47 * 89"})
    assert mock_client.models.generate_content.call_count == 2


@patch("src.agents.single_agent.execute_tool")
@patch("src.agents.single_agent.get_client")
def test_agent_stops_after_max_steps_without_final_answer(mock_get_client, mock_execute_tool):
    """If the model keeps requesting tool calls forever, the loop must stop
    rather than run indefinitely."""
    mock_execute_tool.return_value = "some result"

    mock_client = MagicMock()
    # Always return a tool-call response, never a final answer
    mock_client.models.generate_content.return_value = _tool_call_response(
        "calculate", {"expression": "1 + 1"}
    )
    mock_get_client.return_value = mock_client

    result = run_agent("Loop forever", max_steps=3)

    assert result == "Agent stopped after 3 steps without a final answer."
    assert mock_client.models.generate_content.call_count == 3
