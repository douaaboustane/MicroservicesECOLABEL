"""
Modèles SQLAlchemy pour le service NLP-Ingredients
"""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.database import Base


class IngredientTaxonomy(Base):
    """Taxonomie des ingrédients avec références externes"""
    __tablename__ = "ingredient_taxonomy"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    name_normalized = Column(String(255), nullable=False, index=True)
    category = Column(String(100))  # fruit, légume, céréale, etc.
    
    # Références externes
    agribalyse_code = Column(String(50))
    ecoinvent_code = Column(String(50))
    
    # Synonymes et variations
    synonyms = Column(JSON)  # ["farine", "farine de blé", "wheat flour"]
    
    # Métadonnées
    is_allergen = Column(Boolean, default=False)
    allergen_category = Column(String(100))  # gluten, lait, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ExtractionHistory(Base):
    """Historique des extractions NLP"""
    __tablename__ = "extraction_history"
    
    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    
    # Résultats
    entities_raw = Column(JSON)  # Entités brutes du NER
    entities_normalized = Column(JSON)  # Entités normalisées
    
    # Métadonnées
    model_version = Column(String(50))
    processing_time_ms = Column(Float)
    confidence_score = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LabelDetection(Base):
    """Détection de labels (bio, équitable, recyclé, etc.)"""
    __tablename__ = "label_detection"
    
    id = Column(Integer, primary_key=True, index=True)
    extraction_id = Column(Integer, index=True)
    
    label_type = Column(String(100))  # bio, fair_trade, recyclable, etc.
    label_name = Column(String(255))
    confidence = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

