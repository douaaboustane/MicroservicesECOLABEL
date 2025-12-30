"""
Tests pour l'API FastAPI du service Scoring
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture pour le client de test"""
    return TestClient(app)


def test_root_endpoint(client):
    """Test l'endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data or "message" in data


def test_health_endpoint(client):
    """Test l'endpoint de santé"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_docs_endpoint(client):
    """Test que la documentation est accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

