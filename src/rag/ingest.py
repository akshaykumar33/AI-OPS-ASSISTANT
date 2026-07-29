"""
Phase 1 - Step 1: Document ingestion.

Responsible for loading raw documents (PDF/txt) from data/docs/
and splitting them into chunks ready for embedding.
"""
from pathlib import Path

from pypdf import PdfReader


def load_documents(docs_dir: str = "data/docs", filenames: list[str] | None = None) -> list[str]:
    """Load raw text from documents in the given directory.

    If filenames is given, only those files are loaded (used by automation
    to ingest just the new files instead of re-processing everything).
    Otherwise all .pdf/.txt files in the directory are loaded.

    Returns a list of raw text strings, one per document. Skips any file
    that fails to load (e.g. corrupt PDF) rather than crashing the whole run.
    """
    directory = Path(docs_dir)
    if not directory.exists():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    documents: list[str] = []

    for file_path in sorted(directory.iterdir()):
        if filenames is not None and file_path.name not in filenames:
            continue

        if file_path.suffix.lower() == ".pdf":
            try:
                reader = PdfReader(str(file_path))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                if text.strip():
                    documents.append(text)
                else:
                    print(f"Warning: no extractable text in {file_path.name}")
            except (OSError, ValueError, RuntimeError) as e:
                print(f"Warning: skipped {file_path.name} ({e})")
        elif file_path.suffix.lower() == ".txt":
            try:
                text = file_path.read_text(encoding="utf-8")
                if text.strip():
                    documents.append(text)
            except (OSError, UnicodeDecodeError) as e:
                print(f"Warning: skipped {file_path.name} ({e})")
        # any other file extension is silently ignored

    return documents


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split a single document's text into overlapping word-based chunks.

    chunk_size and overlap are measured in words (a simple, dependency-free
    stand-in for token counts - close enough for this stage of the project).
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunk_words = words[start : start + chunk_size]
        chunks.append(" ".join(chunk_words))
        if start + chunk_size >= len(words):
            break

    return chunks


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")
    for i, doc in enumerate(docs):
        chunks = chunk_text(doc)
        print(f"  Document {i}: {len(doc.split())} words -> {len(chunks)} chunks")
