import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker

# Créer une base de données de test en mémoire
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Créer une session de test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Créer un client de test"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health_check(client):
    """Test du health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "parser-service"


def test_root_endpoint(client):
    """Test de l'endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Parser Service"
    assert "version" in data


def test_parse_single_product_no_file(client):
    """Test parsing sans fichier"""
    response = client.post("/product/parse/single")
    assert response.status_code == 422  # Validation error


def test_get_product_not_found(client):
    """Test récupération produit inexistant"""
    response = client.get("/product/99999")
    assert response.status_code == 404

