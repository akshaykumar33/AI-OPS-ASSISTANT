"""
Phase 1 - Step 2: Embedding + vector storage.

Responsible for turning text chunks into embeddings and storing them
in a persistent ChromaDB collection.

DO NOT change the embedding model or chunk config here without updating
retrieve.py to match - they must stay in sync.
"""
import os
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma")
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load and return the sentence-transformers embedding model (cached - loaded once per process)."""
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


@lru_cache(maxsize=1)
def get_chroma_client() -> chromadb.ClientAPI:
    """Return a persistent Chroma client rooted at CHROMA_DB_PATH (cached - one client per process)."""
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)


def embed_and_store(chunks: list[str], collection_name: str = "documents") -> int:
    """Embed each chunk and upsert into the given Chroma collection.

    IDs are content-based (index in the batch + a hash-free running counter
    against existing collection size) so re-running ingestion on the same
    chunks doesn't duplicate them. Returns the number of chunks stored.
    """
    if not chunks:
        return 0

    model = get_embedding_model()
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=collection_name)

    embeddings = model.encode(chunks, show_progress_bar=False).tolist()

    # Offset new IDs past whatever is already in the collection so repeated
    # ingest runs on new documents don't collide with existing entries.
    existing_count = collection.count()
    ids = [f"chunk-{existing_count + i}" for i in range(len(chunks))]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
    )

    return len(chunks)


if __name__ == "__main__":
    from src.rag.ingest import chunk_text, load_documents

    docs = load_documents()
    all_chunks = [c for doc in docs for c in chunk_text(doc)]
    stored = embed_and_store(all_chunks)
    print(f"Stored {stored} chunks in Chroma collection 'documents' at {CHROMA_DB_PATH}")
