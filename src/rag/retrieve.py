"""
Phase 1 - Step 3: Retrieval + answer generation.

Responsible for taking a user question, retrieving the most relevant
chunks from Chroma, stuffing them into a prompt, and calling the LLM
to generate a grounded answer.
"""
from src.llm_client import ask
from src.rag.embed import get_chroma_client, get_embedding_model

COLLECTION_NAME = "documents"

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions using ONLY the "
    "context provided below. If the answer isn't in the context, say so "
    "clearly instead of guessing."
)


def retrieve_chunks(query: str, k: int = 4) -> list[str]:
    """Return the top-k most relevant chunks for the given query.

    Returns an empty list if the collection doesn't exist yet or has no
    matches, rather than raising - an empty result is a normal, expected
    case (e.g. before any documents have been ingested).
    """
    model = get_embedding_model()
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    if collection.count() == 0:
        return []

    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(k, collection.count()),
    )

    # results["documents"] is a list of lists (one inner list per query embedding)
    documents = results.get("documents") or [[]]
    return documents[0]


def answer_question(query: str, k: int = 4) -> str:
    """Retrieve context for query, build a grounded prompt, call the LLM, return the answer."""
    chunks = retrieve_chunks(query, k=k)

    if not chunks:
        context = "(no documents have been ingested yet)"
    else:
        context = "\n\n---\n\n".join(chunks)

    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    return ask(prompt, system=SYSTEM_PROMPT)


if __name__ == "__main__":
    question = input("Ask a question about your documents: ")
    print(answer_question(question))
