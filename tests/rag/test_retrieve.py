"""Tests for src/rag/retrieve.py.

Mocks the embedding model, Chroma client, and LLM call so retrieval
logic (empty collection handling, prompt construction) can be verified
without a real vector DB or API key.
"""
from unittest.mock import MagicMock, patch

from src.rag.retrieve import answer_question, retrieve_chunks


@patch("src.rag.retrieve.get_chroma_client")
@patch("src.rag.retrieve.get_embedding_model")
def test_retrieve_chunks_returns_empty_when_collection_empty(mock_get_model, mock_get_client):
    mock_collection = MagicMock()
    mock_collection.count.return_value = 0
    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_get_client.return_value = mock_client

    result = retrieve_chunks("any question")

    assert result == []
    mock_collection.query.assert_not_called()


@patch("src.rag.retrieve.get_chroma_client")
@patch("src.rag.retrieve.get_embedding_model")
def test_retrieve_chunks_queries_and_returns_documents(mock_get_model, mock_get_client):
    mock_model = MagicMock()
    mock_model.encode.return_value = MagicMock(tolist=lambda: [[0.1, 0.2]])
    mock_get_model.return_value = mock_model

    mock_collection = MagicMock()
    mock_collection.count.return_value = 3
    mock_collection.query.return_value = {"documents": [["chunk a", "chunk b"]]}
    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_get_client.return_value = mock_client

    result = retrieve_chunks("a question", k=2)

    assert result == ["chunk a", "chunk b"]
    mock_collection.query.assert_called_once_with(
        query_embeddings=[[0.1, 0.2]],
        n_results=2,
    )


@patch("src.rag.retrieve.get_chroma_client")
@patch("src.rag.retrieve.get_embedding_model")
def test_retrieve_chunks_caps_n_results_at_collection_count(mock_get_model, mock_get_client):
    """If k > available chunks, n_results should be capped to what's actually in the collection."""
    mock_model = MagicMock()
    mock_model.encode.return_value = MagicMock(tolist=lambda: [[0.1, 0.2]])
    mock_get_model.return_value = mock_model

    mock_collection = MagicMock()
    mock_collection.count.return_value = 2  # only 2 chunks exist
    mock_collection.query.return_value = {"documents": [["chunk a", "chunk b"]]}
    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_get_client.return_value = mock_client

    retrieve_chunks("a question", k=10)

    mock_collection.query.assert_called_once_with(
        query_embeddings=[[0.1, 0.2]],
        n_results=2,
    )


@patch("src.rag.retrieve.ask")
@patch("src.rag.retrieve.retrieve_chunks")
def test_answer_question_builds_prompt_with_context(mock_retrieve, mock_ask):
    mock_retrieve.return_value = ["fact one", "fact two"]
    mock_ask.return_value = "The answer based on context."

    result = answer_question("What are the facts?")

    assert result == "The answer based on context."
    mock_ask.assert_called_once()
    call_args = mock_ask.call_args
    prompt = call_args.args[0] if call_args.args else call_args.kwargs["prompt"]
    assert "fact one" in prompt
    assert "fact two" in prompt
    assert "What are the facts?" in prompt


@patch("src.rag.retrieve.ask")
@patch("src.rag.retrieve.retrieve_chunks")
def test_answer_question_handles_no_documents_ingested(mock_retrieve, mock_ask):
    mock_retrieve.return_value = []
    mock_ask.return_value = "No documents to search."

    result = answer_question("Anything in there?")

    assert result == "No documents to search."
    call_args = mock_ask.call_args
    prompt = call_args.args[0] if call_args.args else call_args.kwargs["prompt"]
    assert "no documents have been ingested yet" in prompt
