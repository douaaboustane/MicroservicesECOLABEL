"""
Modèles SQLAlchemy pour l'API Gateway
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class JobStatus(str, enum.Enum):
    """Statuts possibles d'un job"""
    PENDING = "PENDING"
    OCR = "OCR"
    NLP = "NLP"
    ACV = "ACV"
    SCORE = "SCORE"
    DONE = "DONE"
    ERROR = "ERROR"


class User(Base):
    """Modèle utilisateur"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Hashé avec bcrypt
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    jobs = relationship("Job", back_populates="user")


class Job(Base):
    """Modèle job de traitement"""
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    progress = Column(Integer, default=0, nullable=False)  # 0-100
    current_step = Column(String, nullable=True)
    
    # Données intermédiaires
    parser_result = Column(JSON, nullable=True)
    nlp_result = Column(JSON, nullable=True)
    lca_result = Column(JSON, nullable=True)
    scoring_result = Column(JSON, nullable=True)
    
    # Résultat final
    result = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    user = relationship("User", back_populates="jobs")

