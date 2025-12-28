"""
Modèles SQLAlchemy pour le service LCALite
"""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class LCAResult(Base):
    """Résultats d'une analyse ACV"""
    __tablename__ = "lca_results"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    
    # Impacts totaux
    co2_kg = Column(Float, nullable=False)
    water_m3 = Column(Float, nullable=False)
    energy_mj = Column(Float, nullable=False)
    acidification = Column(Float)
    eutrophisation = Column(Float)
    
    # Détail
    breakdown = Column(JSON)  # Détail par catégorie (ingrédients, emballage, transport)
    
    # Métadonnées
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ImpactFactor(Base):
    """Facteurs d'impact pour référence"""
    __tablename__ = "impact_factors"
    
    id = Column(Integer, primary_key=True, index=True)
    ingredient_code = Column(String(50), unique=True, index=True)
    ingredient_name = Column(String(255))
    
    # Facteurs d'impact (par kg)
    co2_kg_per_kg = Column(Float)
    water_m3_per_kg = Column(Float)
    energy_mj_per_kg = Column(Float)
    acidification_per_kg = Column(Float)
    eutrophisation_per_kg = Column(Float)
    
    # Source
    source = Column(String(100))  # agribalyse, ecoinvent, etc.
    source_id = Column(String(100))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TransportData(Base):
    """Données de transport"""
    __tablename__ = "transport_data"
    
    id = Column(Integer, primary_key=True, index=True)
    transport_type = Column(String(50), index=True)  # routier_france, routier_europe, aerien
    origin_country = Column(String(10))
    destination_country = Column(String(10))
    
    # Facteurs d'émission (kg CO2 / tonne.km)
    co2_per_tonne_km = Column(Float, nullable=False)
    
    # Métadonnées
    created_at = Column(DateTime(timezone=True), server_default=func.now())

