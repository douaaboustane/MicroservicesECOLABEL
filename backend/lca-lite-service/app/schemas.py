"""
Schémas Pydantic pour la validation des données
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ============================================================================
# Schémas pour les requêtes
# ============================================================================

class IngredientInput(BaseModel):
    """Ingrédient en entrée"""
    name: str = Field(..., description="Nom de l'ingrédient")
    normalized_name: Optional[str] = Field(None, description="Nom normalisé")
    agribalyse_code: Optional[str] = Field(None, description="Code Agribalyse")
    quantity_kg: Optional[float] = Field(None, description="Quantité en kg")
    quantity_percentage: Optional[float] = Field(None, description="Quantité en pourcentage")
    origin: Optional[str] = Field(None, description="Origine géographique")


class PackagingInput(BaseModel):
    """Emballage en entrée"""
    type: str = Field(..., description="Type d'emballage (plastique, verre, papier, etc.)")
    weight_kg: Optional[float] = Field(None, description="Poids en kg")
    weight_g: Optional[float] = Field(None, description="Poids en grammes")
    recyclable: Optional[bool] = Field(False, description="Est recyclable")


class TransportInput(BaseModel):
    """Transport en entrée"""
    origin_country: Optional[str] = Field(None, description="Pays d'origine (code ISO)")
    destination_country: Optional[str] = Field(None, description="Pays de destination")
    distance_km: Optional[float] = Field(None, description="Distance en km")
    transport_type: Optional[str] = Field(None, description="Type (routier_france, routier_europe, aerien)")


class LCACalcRequest(BaseModel):
    """Requête de calcul ACV"""
    product_id: Optional[int] = Field(None, description="ID du produit (optionnel)")
    ingredients: List[IngredientInput] = Field(..., description="Liste des ingrédients")
    packaging: Optional[PackagingInput] = Field(None, description="Informations emballage")
    transport: Optional[TransportInput] = Field(None, description="Informations transport")
    product_weight_kg: Optional[float] = Field(None, description="Poids total du produit en kg")


# ============================================================================
# Schémas pour les réponses
# ============================================================================

class ImpactBreakdown(BaseModel):
    """Détail des impacts par catégorie"""
    co2_kg: float = Field(..., description="CO2 en kg")
    water_m3: float = Field(..., description="Eau en m³")
    energy_mj: float = Field(..., description="Énergie en MJ")
    acidification: Optional[float] = None
    eutrophisation: Optional[float] = None
    contribution_percentage: Optional[float] = Field(None, description="Pourcentage de contribution")


class IngredientImpact(BaseModel):
    """Impact d'un ingrédient"""
    ingredient_name: str
    quantity_kg: float
    impacts: ImpactBreakdown
    agribalyse_code: Optional[str] = None


class TotalImpacts(BaseModel):
    """Impacts totaux"""
    co2_kg: float = Field(..., description="CO2 total en kg")
    water_m3: float = Field(..., description="Eau totale en m³")
    energy_mj: float = Field(..., description="Énergie totale en MJ")
    acidification: Optional[float] = None
    eutrophisation: Optional[float] = None


class LCACalcResponse(BaseModel):
    """Réponse de calcul ACV"""
    # Impacts totaux
    total_impacts: TotalImpacts = Field(..., description="Impacts totaux")
    
    # Détail par catégorie
    breakdown: Dict[str, ImpactBreakdown] = Field(..., description="Détail par catégorie")
    
    # Détail par ingrédient
    ingredients_impacts: List[IngredientImpact] = Field(..., description="Impacts par ingrédient")
    
    # Métadonnées
    product_weight_kg: Optional[float] = Field(None, description="Poids total du produit")
    unit: str = Field("per product", description="Unité des impacts")
    processing_time_ms: Optional[float] = Field(None, description="Temps de traitement")


class Uncertainty(BaseModel):
    """Incertitude du calcul"""
    co2_range: List[float] = Field(..., description="Plage CO2 [min, max]")
    confidence_level: float = Field(..., description="Niveau de confiance (0-1)")


class HealthResponse(BaseModel):
    """État de santé du service"""
    status: str = Field(..., description="État (healthy, unhealthy)")
    service: str = Field(..., description="Nom du service")
    version: str = Field(..., description="Version")
    agribalyse_loaded: bool = Field(..., description="Base Agribalyse chargée")
    timestamp: datetime = Field(..., description="Timestamp")

