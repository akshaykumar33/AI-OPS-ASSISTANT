"""Unit & integration tests for Phase 5: FastAPI Studio Endpoints & API Router."""

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

def test_studio_trends_endpoint():
    """Test GET /studio/trends endpoint."""
    response = client.get("/studio/trends?category=AI news&max_results=2")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "topics" in data
    assert len(data["topics"]) > 0

def test_studio_research_endpoint():
    """Test POST /studio/research endpoint."""
    response = client.post("/studio/research", json={"topic": "Quantum Computing"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "research_summary" in data

def test_studio_research_empty_topic():
    """Test POST /studio/research error on empty topic."""
    response = client.post("/studio/research", json={"topic": "   "})
    assert response.status_code == 422
