"""
Phase 4: MCP server that exposes the RAG knowledge base as a tool
any MCP client (agent) can call.

Run standalone to test with the MCP Inspector:
    mcp dev src/mcp/servers/rag_server.py

Or as a subprocess launched by our own client (src/mcp/client.py).
"""
from mcp.server.fastmcp import FastMCP

from src.rag.retrieve import retrieve_chunks

mcp = FastMCP("rag-knowledge-base")


@mcp.tool()
def search_documents(query: str, k: int = 4) -> str:
    """Search the user's ingested documents and return the most relevant excerpts.

    Args:
        query: The question or topic to search for.
        k: How many chunks to retrieve (default 4).

    Returns:
        Relevant excerpts joined together, or a message if nothing is found.
    """
    chunks = retrieve_chunks(query, k=k)
    if not chunks:
        return "No relevant documents found for this query."
    return "\n---\n".join(chunks)


if __name__ == "__main__":
    mcp.run()
