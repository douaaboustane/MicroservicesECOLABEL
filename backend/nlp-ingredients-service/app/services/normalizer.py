"""
Service de normalisation des entités
"""
import re
from typing import List, Dict, Any, Optional
from fuzzywuzzy import fuzz, process

from app.config import settings


class EntityNormalizer:
    """Normalise les entités extraites"""
    
    def __init__(self, taxonomy_data: Optional[Dict] = None):
        self.taxonomy = taxonomy_data or {}
        self.fuzzy_threshold = settings.FUZZY_THRESHOLD
    
    def normalize_text(self, text: str) -> str:
        """
        Normalise un texte (minuscules, accents, etc.)
        
        Args:
            text: Texte à normaliser
        
        Returns:
            Texte normalisé
        """
        # Minuscules
        text = text.lower()
        
        # Supprimer les accents
        text = self._remove_accents(text)
        
        # Supprimer caractères spéciaux (sauf espaces et tirets)
        text = re.sub(r'[^a-z0-9\s\-]', '', text)
        
        # Supprimer espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _remove_accents(self, text: str) -> str:
        """Supprime les accents"""
        accent_map = {
            'à': 'a', 'â': 'a', 'ä': 'a',
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'î': 'i', 'ï': 'i',
            'ô': 'o', 'ö': 'o',
            'ù': 'u', 'û': 'u', 'ü': 'u',
            'ç': 'c',
            'ñ': 'n'
        }
        for accent, replacement in accent_map.items():
            text = text.replace(accent, replacement)
        return text
    
    def normalize_entity(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalise une entité individuelle.
        
        Args:
            entity: Entité brute
        
        Returns:
            Entité normalisée
        """
        text = entity["text"]
        label = entity["label"]
        
        # Normaliser le texte
        normalized_name = self.normalize_text(text)
        
        # Créer l'entité normalisée
        normalized = {
            "text": text,
            "normalized_name": normalized_name,
            "label": label,
            "category": None,
            "agribalyse_code": None,
            "ecoinvent_code": None,
            "is_allergen": label == "ALLERGEN",
            "allergen_category": None,
            "quantity": None,
            "match_score": None,
            "match_method": None
        }
        
        # Si c'est une QUANTITY, la stocker
        if label == "QUANTITY":
            normalized["quantity"] = text
        
        # Matcher avec la taxonomie si disponible
        if label in ["INGREDIENT", "ALLERGEN"] and self.taxonomy:
            match_result = self.match_with_taxonomy(normalized_name)
            if match_result:
                normalized.update(match_result)
        
        return normalized
    
    def match_with_taxonomy(self, normalized_name: str) -> Optional[Dict[str, Any]]:
        """
        Matche un nom normalisé avec la taxonomie.
        
        Args:
            normalized_name: Nom normalisé
        
        Returns:
            Informations de matching ou None
        """
        if not self.taxonomy:
            return None
        
        # Recherche exacte
        if normalized_name in self.taxonomy:
            item = self.taxonomy[normalized_name]
            return {
                "category": item.get("category"),
                "agribalyse_code": item.get("agribalyse_code"),
                "ecoinvent_code": item.get("ecoinvent_code"),
                "allergen_category": item.get("allergen_category"),
                "match_score": 100.0,
                "match_method": "exact"
            }
        
        # Recherche floue
        taxonomy_keys = list(self.taxonomy.keys())
        match = process.extractOne(
            normalized_name,
            taxonomy_keys,
            scorer=fuzz.token_sort_ratio
        )
        
        if match and match[1] >= self.fuzzy_threshold:
            matched_key = match[0]
            item = self.taxonomy[matched_key]
            return {
                "category": item.get("category"),
                "agribalyse_code": item.get("agribalyse_code"),
                "ecoinvent_code": item.get("ecoinvent_code"),
                "allergen_category": item.get("allergen_category"),
                "match_score": float(match[1]),
                "match_method": "fuzzy"
            }
        
        return None
    
    def normalize_batch(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalise un batch d'entités.
        
        Args:
            entities: Liste d'entités brutes
        
        Returns:
            Liste d'entités normalisées
        """
        return [self.normalize_entity(entity) for entity in entities]
    
    def extract_quantities(self, entities: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Extrait les quantités et les associe aux ingrédients.
        
        Args:
            entities: Liste d'entités normalisées
        
        Returns:
            Dictionnaire {ingrédient: quantité}
        """
        quantities = {}
        
        # Trouver les quantités
        quantity_entities = [e for e in entities if e["label"] == "QUANTITY"]
        ingredient_entities = [e for e in entities if e["label"] == "INGREDIENT"]
        
        # Associer les quantités aux ingrédients (simple heuristique)
        for i, ingredient in enumerate(ingredient_entities):
            # Chercher la quantité la plus proche après l'ingrédient
            for quantity in quantity_entities:
                # Si la quantité est proche (heuristique simple)
                # On pourrait améliorer avec des positions dans le texte
                quantities[ingredient["normalized_name"]] = quantity["text"]
                break
        
        return quantities

