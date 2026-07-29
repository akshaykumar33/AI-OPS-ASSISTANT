"""Tests for src/automation/scheduler.py.

find_new_files/_load_state/_save_state have no external dependencies
and are tested for real. daily_briefing/ingest_new_files/on_new_file
call into embed/ask (Chroma/Gemini) and are tested with mocks.
"""
from unittest.mock import patch

import pytest

from src.automation import scheduler


@pytest.fixture(autouse=True)
def isolated_paths(tmp_path, monkeypatch):
    """Point STATE_FILE and DOCS_DIR at a temp directory so tests never
    touch the real project's data/ folder."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    state_file = tmp_path / "automation_state.json"
    monkeypatch.setattr(scheduler, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(scheduler, "STATE_FILE", state_file)
    return docs_dir, state_file


def test_find_new_files_returns_all_files_when_no_state(isolated_paths):
    docs_dir, _ = isolated_paths
    (docs_dir / "a.txt").write_text("content a")
    (docs_dir / "b.pdf").touch()

    result = scheduler.find_new_files()

    assert result == ["a.txt", "b.pdf"]


def test_find_new_files_excludes_already_ingested(isolated_paths):
    docs_dir, _state_file = isolated_paths
    (docs_dir / "a.txt").write_text("content a")
    (docs_dir / "b.txt").write_text("content b")
    scheduler._save_state({"a.txt"})

    result = scheduler.find_new_files()

    assert result == ["b.txt"]


def test_find_new_files_ignores_unsupported_extensions(isolated_paths):
    docs_dir, _ = isolated_paths
    (docs_dir / "a.txt").write_text("content")
    (docs_dir / "notes.csv").write_text("a,b,c")

    result = scheduler.find_new_files()

    assert result == ["a.txt"]


def test_find_new_files_returns_empty_when_docs_dir_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(scheduler, "DOCS_DIR", tmp_path / "does_not_exist")
    assert scheduler.find_new_files() == []


def test_state_roundtrip(isolated_paths):
    scheduler._save_state({"x.txt", "y.pdf"})
    assert scheduler._load_state() == {"x.txt", "y.pdf"}


@patch("src.automation.scheduler.embed_and_store")
@patch("src.automation.scheduler.load_documents")
def test_ingest_new_files_updates_state(mock_load_documents, mock_embed_and_store, isolated_paths):
    mock_load_documents.return_value = ["doc text"]
    mock_embed_and_store.return_value = 3

    stored = scheduler.ingest_new_files(["report.pdf"])

    assert stored == 3
    assert scheduler._load_state() == {"report.pdf"}


def test_ingest_new_files_empty_list_does_nothing(isolated_paths):
    assert scheduler.ingest_new_files([]) == 0
    assert scheduler._load_state() == set()


@patch("src.automation.scheduler.ask")
@patch("src.automation.scheduler.ingest_new_files")
@patch("src.automation.scheduler.find_new_files")
def test_daily_briefing_no_new_files(mock_find_new, mock_ingest, mock_ask):
    mock_find_new.return_value = []

    result = scheduler.daily_briefing()

    assert result == "Daily briefing: no new documents since last run."
    mock_ingest.assert_not_called()
    mock_ask.assert_not_called()


@patch("src.automation.scheduler.ask")
@patch("src.automation.scheduler.ingest_new_files")
@patch("src.automation.scheduler.find_new_files")
def test_daily_briefing_summarizes_new_files(mock_find_new, mock_ingest, mock_ask):
    mock_find_new.return_value = ["report.pdf"]
    mock_ingest.return_value = 5
    mock_ask.return_value = "One new document was added and is ready to search."

    result = scheduler.daily_briefing()

    assert result == "One new document was added and is ready to search."
    mock_ingest.assert_called_once_with(["report.pdf"])


@patch("src.automation.scheduler.ingest_new_files")
def test_on_new_file_reports_success(mock_ingest):
    mock_ingest.return_value = 2

    result = scheduler.on_new_file("notes.txt")

    assert "Ingested 'notes.txt'" in result
    assert "2 chunks" in result


@patch("src.automation.scheduler.ingest_new_files")
def test_on_new_file_reports_nothing_to_do(mock_ingest):
    mock_ingest.return_value = 0

    result = scheduler.on_new_file("already_seen.txt")

    assert "already ingested" in result
