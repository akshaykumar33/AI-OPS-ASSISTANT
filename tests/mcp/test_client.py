"""Tests for src/mcp/client.py.

Mocks the MCP session/stdio machinery so the wiring logic (unknown
server handling, tool listing, result concatenation) is verified
without spawning a real subprocess or needing the mcp package's
network-facing bits.
"""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.mcp.client import SERVER_CONFIGS, call_tool, list_available_tools


@pytest.mark.asyncio
async def test_unknown_server_raises_value_error():
    with pytest.raises(ValueError, match="Unknown MCP server"):
        async with __import__("src.mcp.client", fromlist=["connect"]).connect("not_a_real_server"):
            pass


@pytest.mark.asyncio
@patch("src.mcp.client.ClientSession")
@patch("src.mcp.client.stdio_client")
async def test_list_available_tools_returns_name_and_description(mock_stdio_client, mock_session_cls):
    mock_tool = MagicMock(name="search_documents", description="Search docs")
    mock_tool.name = "search_documents"
    mock_tool.description = "Search docs"

    mock_result = MagicMock()
    mock_result.tools = [mock_tool]

    mock_session = AsyncMock()
    mock_session.list_tools.return_value = mock_result
    mock_session_cls.return_value.__aenter__.return_value = mock_session

    mock_stdio_client.return_value.__aenter__.return_value = (MagicMock(), MagicMock())

    tools = await list_available_tools("rag")

    assert tools == [{"name": "search_documents", "description": "Search docs"}]


@pytest.mark.asyncio
@patch("src.mcp.client.ClientSession")
@patch("src.mcp.client.stdio_client")
async def test_call_tool_concatenates_text_blocks(mock_stdio_client, mock_session_cls):
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "search result text"

    mock_call_result = MagicMock()
    mock_call_result.content = [text_block]

    mock_session = AsyncMock()
    mock_session.call_tool.return_value = mock_call_result
    mock_session_cls.return_value.__aenter__.return_value = mock_session

    mock_stdio_client.return_value.__aenter__.return_value = (MagicMock(), MagicMock())

    result = await call_tool("rag", "search_documents", {"query": "test"})

    assert result == "search result text"
    mock_session.call_tool.assert_called_once_with("search_documents", {"query": "test"})


def test_server_configs_has_rag_entry():
    assert "rag" in SERVER_CONFIGS
