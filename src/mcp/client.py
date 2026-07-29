"""
Phase 4: MCP client - connects the agent to available MCP servers
(rag_server, and later an action-tool server) so the agent discovers
and calls tools without hardcoded integrations.

Each server runs as a subprocess (stdio transport) launched by this
client. Add new servers to SERVER_CONFIGS below - no other code needs
to change when a new server is added.
"""
import sys
from contextlib import asynccontextmanager

from mcp.client.stdio import stdio_client

from mcp import ClientSession, StdioServerParameters

# Maps a friendly server name -> how to launch it.
# Add new entries here as new MCP servers are built (Phase 4+).
SERVER_CONFIGS = {
    "rag": StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.mcp.servers.rag_server"],
    ),
}


@asynccontextmanager
async def connect(server_name: str):
    """Open a session with the named server. Use as: `async with connect("rag") as session:`"""
    if server_name not in SERVER_CONFIGS:
        raise ValueError(f"Unknown MCP server '{server_name}'. Known servers: {list(SERVER_CONFIGS)}")

    params = SERVER_CONFIGS[server_name]
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        yield session



async def list_available_tools(server_name: str) -> list[dict]:
    """Return all tools exposed by the named MCP server, as {name, description} dicts."""
    async with connect(server_name) as session:
        result = await session.list_tools()
        return [{"name": t.name, "description": t.description} for t in result.tools]


async def call_tool(server_name: str, tool_name: str, args: dict) -> str:
    """Call a tool on the named server and return its text result."""
    async with connect(server_name) as session:
        result = await session.call_tool(tool_name, args)
        # Tool results come back as a list of content blocks; concatenate any text ones.
        return "".join(block.text for block in result.content if block.type == "text")


if __name__ == "__main__":
    import asyncio

    async def _demo():
        tools = await list_available_tools("rag")
        print(f"Tools available on 'rag' server: {tools}")
        answer = await call_tool("rag", "search_documents", {"query": "test query"})
        print(f"Result: {answer}")

    asyncio.run(_demo())
