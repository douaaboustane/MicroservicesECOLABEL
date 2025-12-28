"""
Schémas Pydantic pour validation des données
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class LCAInput(BaseModel):
    """Données LCA pour le calcul de score"""
    co2_kg: float = Field(..., description="Émissions CO2 en kg")
    water_liters: float = Field(..., description="Consommation d'eau en litres")
    energy_mj: float = Field(..., description="Énergie en MJ")
    acidification: Optional[float] = Field(None, description="Acidification")
    eutrophisation: Optional[float] = Field(None, description="Eutrophisation")


class NLPInput(BaseModel):
    """Données NLP pour le calcul de score"""
    ingredients: List[str] = Field(default_factory=list, description="Liste des ingrédients")
    allergens: List[str] = Field(default_factory=list, description="Liste des allergènes")
    labels: List[str] = Field(default_factory=list, description="Labels détectés")
    packaging_type: Optional[str] = Field(None, description="Type d'emballage")
    packaging_recyclable: Optional[bool] = Field(None, description="Emballage recyclable")
    origin: Optional[str] = Field(None, description="Origine géographique")
    has_bio_label: Optional[bool] = Field(None, description="Label bio")
    has_fair_trade: Optional[bool] = Field(None, description="Commerce équitable")
    has_palm_oil: Optional[bool] = Field(None, description="Contient de l'huile de palme")
    has_high_sugar: Optional[bool] = Field(None, description="Teneur élevée en sucre")
    has_additives: Optional[bool] = Field(None, description="Contient des additifs")


class ScoreRequest(BaseModel):
    """Requête de calcul de score"""
    lca_data: LCAInput
    nlp_data: NLPInput
    method: Optional[str] = Field("hybrid", description="Méthode: 'classification', 'regression', ou 'hybrid'")


class ScoreProbabilities(BaseModel):
    """Probabilités pour chaque classe"""
    A: float
    B: float
    C: float
    D: float
    E: float


class ScoreResponse(BaseModel):
    """Réponse avec le score calculé"""
    score_letter: str = Field(..., description="Score lettre (A-E)")
    score_numeric: float = Field(..., description="Score numérique (0-100)")
    confidence: Optional[float] = Field(None, description="Niveau de confiance")
    method: str = Field(..., description="Méthode utilisée")
    probabilities: Optional[ScoreProbabilities] = Field(None, description="Probabilités (si classification)")
    details: Optional[Dict[str, Any]] = Field(None, description="Détails du calcul")


class HealthResponse(BaseModel):
    """Réponse de health check"""
    status: str
    service: str
    version: str
    classification_model_loaded: bool
    regression_model_loaded: bool
    timestamp: datetime

