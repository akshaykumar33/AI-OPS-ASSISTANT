"""Tests for src/rag/embed.py.

Uses mocks for the embedding model and Chroma client so the logic
(ID offsetting, empty-input handling, upsert wiring) can be verified
without needing the real model downloaded or a live Chroma instance.
"""
from unittest.mock import MagicMock, patch

from src.rag.embed import embed_and_store


def test_embed_and_store_empty_chunks_returns_zero():
    assert embed_and_store([]) == 0


@patch("src.rag.embed.get_chroma_client")
@patch("src.rag.embed.get_embedding_model")
def test_embed_and_store_calls_upsert_with_correct_args(mock_get_model, mock_get_client):
    mock_model = MagicMock()
    mock_model.encode.return_value = MagicMock(tolist=lambda: [[0.1, 0.2], [0.3, 0.4]])
    mock_get_model.return_value = mock_model

    mock_collection = MagicMock()
    mock_collection.count.return_value = 0
    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_get_client.return_value = mock_client

    chunks = ["chunk one", "chunk two"]
    stored = embed_and_store(chunks, collection_name="test_collection")

    assert stored == 2
    mock_client.get_or_create_collection.assert_called_once_with(name="test_collection")
    mock_model.encode.assert_called_once_with(chunks, show_progress_bar=False)
    mock_collection.upsert.assert_called_once_with(
        ids=["chunk-0", "chunk-1"],
        embeddings=[[0.1, 0.2], [0.3, 0.4]],
        documents=chunks,
    )


@patch("src.rag.embed.get_chroma_client")
@patch("src.rag.embed.get_embedding_model")
def test_embed_and_store_offsets_ids_past_existing_count(mock_get_model, mock_get_client):
    """New chunks should get IDs starting after whatever's already in the collection,
    so repeated ingestion runs don't overwrite earlier documents."""
    mock_model = MagicMock()
    mock_model.encode.return_value = MagicMock(tolist=lambda: [[0.5, 0.6]])
    mock_get_model.return_value = mock_model

    mock_collection = MagicMock()
    mock_collection.count.return_value = 5  # pretend 5 chunks already stored
    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_get_client.return_value = mock_client

    embed_and_store(["new chunk"], collection_name="test_collection")

    mock_collection.upsert.assert_called_once_with(
        ids=["chunk-5"],
        embeddings=[[0.5, 0.6]],
        documents=["new chunk"],
    )
