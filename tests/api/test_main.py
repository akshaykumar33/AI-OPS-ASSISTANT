"""Tests for src/api/main.py.

Uses FastAPI's TestClient with the underlying phase functions mocked,
so these check routing/validation/error-handling, not the real
RAG/agent/pipeline logic (which is already tested in their own modules).
"""
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("src.api.main.answer_question")
def test_ask_returns_answer(mock_answer_question):
    mock_answer_question.return_value = "Paris is the capital of France."

    response = client.post("/ask", json={"question": "What is the capital of France?"})

    assert response.status_code == 200
    assert response.json() == {"answer": "Paris is the capital of France."}
    mock_answer_question.assert_called_once_with("What is the capital of France?", k=4)


def test_ask_rejects_empty_question():
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 422


@patch("src.api.main.answer_question")
def test_ask_returns_500_on_internal_error(mock_answer_question):
    mock_answer_question.side_effect = RuntimeError("Chroma connection failed")

    response = client.post("/ask", json={"question": "anything"})

    assert response.status_code == 500
    assert "Chroma connection failed" in response.json()["detail"]


@patch("src.api.main.run_agent")
def test_agent_endpoint_returns_result(mock_run_agent):
    mock_run_agent.return_value = "47 * 89 = 4183"

    response = client.post("/agent", json={"task": "What is 47 * 89?"})

    assert response.status_code == 200
    assert response.json() == {"answer": "47 * 89 = 4183"}


def test_agent_rejects_empty_task():
    response = client.post("/agent", json={"task": ""})
    assert response.status_code == 422


@patch("src.api.main.run_pipeline")
def test_pipeline_endpoint_returns_result(mock_run_pipeline):
    mock_run_pipeline.return_value = "Final reviewed answer."

    response = client.post("/pipeline", json={"task": "Summarize my docs"})

    assert response.status_code == 200
    assert response.json() == {"answer": "Final reviewed answer."}


@patch("src.api.main.ingest_new_files")
@patch("src.api.main.find_new_files")
def test_ingest_endpoint_returns_counts(mock_find_new_files, mock_ingest_new_files):
    mock_find_new_files.return_value = ["report.pdf"]
    mock_ingest_new_files.return_value = 5

    response = client.post("/ingest")

    assert response.status_code == 200
    assert response.json() == {"files_ingested": ["report.pdf"], "chunks_stored": 5}


@patch("src.api.main.ingest_new_files")
@patch("src.api.main.find_new_files")
def test_ingest_endpoint_handles_no_new_files(mock_find_new_files, mock_ingest_new_files):
    mock_find_new_files.return_value = []
    mock_ingest_new_files.return_value = 0

    response = client.post("/ingest")

    assert response.status_code == 200
    assert response.json() == {"files_ingested": [], "chunks_stored": 0}
