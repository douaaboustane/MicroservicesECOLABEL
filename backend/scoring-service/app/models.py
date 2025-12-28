"""
Modèles SQLAlchemy pour la base de données
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class ScoreHistory(Base):
    """Historique des scores calculés"""
    __tablename__ = "score_history"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    score_letter = Column(String, index=True)  # A, B, C, D, E
    score_numeric = Column(Float)  # 0-100
    lca_data = Column(JSON)  # Données LCA utilisées
    nlp_data = Column(JSON)  # Données NLP utilisées
    method = Column(String)  # "classification", "regression", "hybrid"
    confidence = Column(Float)  # Niveau de confiance
    created_at = Column(DateTime(timezone=True), server_default=func.now())

