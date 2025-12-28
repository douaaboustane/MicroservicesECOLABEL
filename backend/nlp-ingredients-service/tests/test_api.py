"""
Tests pour l'API FastAPI
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
    assert data["service"] == "NLP-Ingredients Service"
    assert data["status"] == "running"


def test_health_endpoint(client):
    """Test l'endpoint de santé"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data


def test_extract_endpoint(client):
    """Test l'endpoint d'extraction"""
    payload = {
        "text": "farine de blé, eau, sel, levure",
        "normalize": True,
        "detect_labels": True
    }
    
    response = client.post("/nlp/extract", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "entities" in data
    assert "entities_normalized" in data
    assert "total_entities" in data
    assert data["total_entities"] > 0


def test_extract_with_enumbers(client):
    """Test l'extraction avec E-numbers"""
    payload = {
        "text": "colorant E150d, conservateur E330, émulsifiant E471"
    }
    
    response = client.post("/nlp/extract", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    entities = data["entities"]
    
    # Vérifier qu'on détecte des E-numbers
    e_numbers = [e for e in entities if "E" in e["text"]]
    assert len(e_numbers) >= 3


def test_extract_with_minerals(client):
    """Test l'extraction avec minéraux"""
    payload = {
        "text": "CALCIUM 55 MAGNESIUM 19 SODIUM 24"
    }
    
    response = client.post("/nlp/extract", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_ingredients"] >= 3


def test_extract_with_labels(client):
    """Test la détection de labels"""
    payload = {
        "text": "Farine bio, sucre équitable, emballage recyclable",
        "detect_labels": True
    }
    
    response = client.post("/nlp/extract", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "labels" in data
    # Au moins le label "bio" devrait être détecté
    assert len(data["labels"]) > 0


def test_batch_extract_endpoint(client):
    """Test l'endpoint d'extraction en batch"""
    payload = {
        "texts": [
            "farine de blé, eau, sel",
            "lait, sucre, vanille"
        ],
        "normalize": True
    }
    
    response = client.post("/nlp/extract/batch", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2
    assert data["total_processed"] == 2


def test_model_info_endpoint(client):
    """Test l'endpoint d'infos du modèle"""
    response = client.get("/nlp/model/info")
    assert response.status_code == 200
    
    data = response.json()
    assert "loaded" in data
    assert data["loaded"] is True

