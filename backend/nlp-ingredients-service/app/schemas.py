"""
Schémas Pydantic pour la validation des données
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ============================================================================
# Schémas pour les entités extraites
# ============================================================================

class Entity(BaseModel):
    """Entité extraite par le NER"""
    text: str = Field(..., description="Texte de l'entité")
    label: str = Field(..., description="Type d'entité (INGREDIENT, ALLERGEN, QUANTITY)")
    start: int = Field(..., description="Position de début")
    end: int = Field(..., description="Position de fin")
    confidence: Optional[float] = Field(None, description="Score de confiance (0-1)")


class NormalizedEntity(BaseModel):
    """Entité normalisée avec références"""
    text: str = Field(..., description="Texte original")
    normalized_name: str = Field(..., description="Nom normalisé")
    category: Optional[str] = Field(None, description="Catégorie (fruit, légume, etc.)")
    label: str = Field(..., description="Type d'entité")
    
    # Références externes
    agribalyse_code: Optional[str] = None
    ecoinvent_code: Optional[str] = None
    
    # Métadonnées
    is_allergen: bool = False
    allergen_category: Optional[str] = None
    quantity: Optional[str] = None
    
    # Matching
    match_score: Optional[float] = Field(None, description="Score de matching (0-100)")
    match_method: Optional[str] = Field(None, description="Méthode de matching (exact, fuzzy)")


class Label(BaseModel):
    """Label détecté (bio, équitable, etc.)"""
    label_type: str = Field(..., description="Type de label")
    label_name: str = Field(..., description="Nom du label")
    confidence: float = Field(..., description="Confiance de détection (0-1)")


class Packaging(BaseModel):
    """Emballage détecté"""
    type: str = Field(..., description="Type d'emballage (plastique, verre, papier, etc.)")
    text: str = Field(..., description="Texte détecté")
    recyclable: bool = Field(False, description="Est recyclable")
    weight: Optional[float] = Field(None, description="Poids de l'emballage")
    weight_unit: Optional[str] = Field(None, description="Unité du poids (g, kg)")
    confidence: float = Field(..., description="Confiance de détection (0-1)")
    all_types_detected: List[str] = Field(default_factory=list, description="Tous les types détectés")


class Origin(BaseModel):
    """Provenance détectée"""
    origin: str = Field(..., description="Type de provenance (france, europe, local, etc.)")
    text: str = Field(..., description="Texte détecté")
    confidence: float = Field(..., description="Confiance de détection (0-1)")
    all_origins_detected: List[str] = Field(default_factory=list, description="Toutes les provenances détectées")
    geographic_labels: Optional[List[Dict[str, Any]]] = Field(None, description="Labels géographiques (AOC, AOP, IGP)")


# ============================================================================
# Schémas pour les requêtes/réponses
# ============================================================================

class ExtractRequest(BaseModel):
    """Requête d'extraction NLP"""
    text: str = Field(..., description="Texte à analyser", min_length=1)
    normalize: bool = Field(True, description="Normaliser les entités")
    detect_labels: bool = Field(True, description="Détecter les labels")
    detect_packaging: bool = Field(True, description="Détecter les emballages")
    detect_origin: bool = Field(True, description="Détecter la provenance")
    language: str = Field("fr", description="Langue du texte (fr, en)")


class ExtractResponse(BaseModel):
    """Réponse d'extraction NLP"""
    # Entités extraites
    entities: List[Entity] = Field(..., description="Entités brutes extraites")
    entities_normalized: List[NormalizedEntity] = Field(..., description="Entités normalisées")
    
    # Labels détectés
    labels: List[Label] = Field(default_factory=list, description="Labels détectés")
    
    # Emballage détecté
    packaging: Optional[Packaging] = Field(None, description="Emballage détecté")
    
    # Provenance détectée
    origin: Optional[Origin] = Field(None, description="Provenance détectée")
    
    # Statistiques
    total_entities: int = Field(..., description="Nombre total d'entités")
    total_ingredients: int = Field(..., description="Nombre d'ingrédients")
    total_allergens: int = Field(..., description="Nombre d'allergènes")
    total_quantities: int = Field(..., description="Nombre de quantités")
    
    # Métadonnées
    processing_time_ms: float = Field(..., description="Temps de traitement (ms)")
    model_version: str = Field(..., description="Version du modèle NER")
    confidence_score: float = Field(..., description="Score de confiance global (0-1)")


class BatchExtractRequest(BaseModel):
    """Requête d'extraction en batch"""
    texts: List[str] = Field(..., description="Liste de textes à analyser")
    normalize: bool = Field(True, description="Normaliser les entités")
    detect_labels: bool = Field(True, description="Détecter les labels")
    detect_packaging: bool = Field(True, description="Détecter les emballages")
    detect_origin: bool = Field(True, description="Détecter la provenance")


class BatchExtractResponse(BaseModel):
    """Réponse d'extraction en batch"""
    results: List[ExtractResponse] = Field(..., description="Résultats pour chaque texte")
    total_processed: int = Field(..., description="Nombre de textes traités")
    total_time_ms: float = Field(..., description="Temps total de traitement (ms)")


# ============================================================================
# Schémas pour la taxonomie
# ============================================================================

class IngredientTaxonomyItem(BaseModel):
    """Item de la taxonomie des ingrédients"""
    id: int
    name: str
    name_normalized: str
    category: Optional[str]
    synonyms: List[str]
    is_allergen: bool
    allergen_category: Optional[str]
    agribalyse_code: Optional[str]
    ecoinvent_code: Optional[str]


class SearchTaxonomyRequest(BaseModel):
    """Requête de recherche dans la taxonomie"""
    query: str = Field(..., description="Terme à rechercher")
    fuzzy: bool = Field(True, description="Utiliser la recherche floue")
    limit: int = Field(10, description="Nombre de résultats max")


class SearchTaxonomyResponse(BaseModel):
    """Réponse de recherche dans la taxonomie"""
    results: List[IngredientTaxonomyItem]
    total: int


# ============================================================================
# Schémas pour la santé du service
# ============================================================================

class HealthResponse(BaseModel):
    """État de santé du service"""
    status: str = Field(..., description="État du service (healthy, unhealthy)")
    service: str = Field(..., description="Nom du service")
    version: str = Field(..., description="Version du service")
    model_loaded: bool = Field(..., description="Modèle NER chargé")
    database_connected: bool = Field(..., description="Base de données connectée")
    timestamp: datetime = Field(..., description="Timestamp")

