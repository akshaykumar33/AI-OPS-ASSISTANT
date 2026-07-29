"""Tests for src/rag/ingest.py."""
import pytest

from src.rag.ingest import chunk_text, load_documents


def test_chunk_text_basic():
    """A short text under chunk_size should come back as a single chunk."""
    text = "one two three four five"
    chunks = chunk_text(text, chunk_size=10, overlap=2)
    assert chunks == ["one two three four five"]


def test_chunk_text_splits_and_overlaps():
    """Text longer than chunk_size should split into multiple overlapping chunks."""
    words = [str(i) for i in range(1, 21)]  # "1" .. "20"
    text = " ".join(words)
    chunks = chunk_text(text, chunk_size=10, overlap=2)

    assert len(chunks) == 3
    # first chunk: words 1-10
    assert chunks[0] == "1 2 3 4 5 6 7 8 9 10"
    # second chunk starts 2 words back from where first ended (overlap=2): words 9-18
    assert chunks[1] == "9 10 11 12 13 14 15 16 17 18"
    # last chunk covers the tail: words 17-20
    assert chunks[2] == "17 18 19 20"


def test_chunk_text_empty_string_returns_empty_list():
    assert chunk_text("", chunk_size=10, overlap=2) == []


def test_chunk_text_rejects_bad_overlap():
    with pytest.raises(ValueError):
        chunk_text("some words here", chunk_size=5, overlap=5)


def test_load_documents_missing_dir_raises(tmp_path):
    missing_dir = tmp_path / "does_not_exist"
    with pytest.raises(FileNotFoundError):
        load_documents(str(missing_dir))


def test_load_documents_reads_txt_files(tmp_path):
    (tmp_path / "note.txt").write_text("hello from a text file", encoding="utf-8")
    (tmp_path / "ignored.csv").write_text("a,b,c", encoding="utf-8")

    docs = load_documents(str(tmp_path))

    assert docs == ["hello from a text file"]


def test_load_documents_skips_empty_txt(tmp_path):
    (tmp_path / "empty.txt").write_text("   ", encoding="utf-8")
    (tmp_path / "real.txt").write_text("actual content", encoding="utf-8")

    docs = load_documents(str(tmp_path))

    assert docs == ["actual content"]
