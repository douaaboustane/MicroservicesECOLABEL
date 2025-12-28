"""
Service d'extraction de la provenance/origine des produits
"""
import re
from typing import List, Dict, Any, Optional


class OriginExtractor:
    """Détecte la provenance/origine géographique des produits"""
    
    def __init__(self):
        # Patterns pour détecter la provenance
        self.origin_patterns = {
            # France
            "france": {
                "patterns": [
                    r'\bfrance\b',
                    r'\bfrançais\b',
                    r'\bfrançaise\b',
                    r'\bproduit en france\b',
                    r'\bfabriqué en france\b',
                    r'\borigine france\b',
                    r'\bmade in france\b'
                ],
                "confidence": 0.95
            },
            # Europe
            "europe": {
                "patterns": [
                    r'\beurope\b',
                    r'\beuropéen\b',
                    r'\beuropéenne\b',
                    r'\bue\b',
                    r'\bunion européenne\b',
                    r'\bproduit de l\'?ue\b'
                ],
                "confidence": 0.9
            },
            # Local/Régional
            "local": {
                "patterns": [
                    r'\blocal\b',
                    r'\brégional\b',
                    r'\bde la région\b',
                    r'\bproduit local\b',
                    r'\bcircuit court\b'
                ],
                "confidence": 0.85
            },
            # Pays spécifiques (exemples)
            "espagne": {
                "patterns": [
                    r'\bespagne\b',
                    r'\bespagnol\b',
                    r'\bespañol\b'
                ],
                "confidence": 0.9
            },
            "italie": {
                "patterns": [
                    r'\bitalie\b',
                    r'\bitalien\b',
                    r'\bitaliano\b'
                ],
                "confidence": 0.9
            },
            "allemagne": {
                "patterns": [
                    r'\ballemagne\b',
                    r'\ballemand\b',
                    r'\bdeutschland\b'
                ],
                "confidence": 0.9
            },
            "belgique": {
                "patterns": [
                    r'\bbelgique\b',
                    r'\bbelge\b'
                ],
                "confidence": 0.9
            },
            # Hors Europe
            "hors_europe": {
                "patterns": [
                    r'\bimport\b',
                    r'\bimporté\b',
                    r'\bimported\b',
                    r'\bhors europe\b',
                    r'\bnon européen\b'
                ],
                "confidence": 0.8
            }
        }
        
        # Patterns pour détecter les labels géographiques
        self.geographic_labels = {
            "aoc": {
                "patterns": [r'\baoc\b', r'\bappellation d\'origine contrôlée\b'],
                "confidence": 0.95
            },
            "aop": {
                "patterns": [r'\baop\b', r'\bappellation d\'origine protégée\b'],
                "confidence": 0.95
            },
            "igp": {
                "patterns": [r'\bigp\b', r'\bindication géographique protégée\b'],
                "confidence": 0.95
            },
            "stg": {
                "patterns": [r'\bstg\b', r'\bspécialité traditionnelle garantie\b'],
                "confidence": 0.95
            }
        }
    
    def extract(self, text: str) -> List[Dict[str, Any]]:
        """
        Extrait les informations de provenance.
        
        Args:
            text: Texte à analyser
        
        Returns:
            Liste d'informations de provenance détectées
        """
        if not text:
            return []
        
        text_lower = text.lower()
        origins_detected = []
        
        # Détecter les provenances
        for origin_type, config in self.origin_patterns.items():
            for pattern in config["patterns"]:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    origins_detected.append({
                        "origin": origin_type,
                        "text": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                        "confidence": config["confidence"]
                    })
                    break  # Une seule détection par type
        
        # Détecter les labels géographiques
        geographic_labels = []
        for label_type, config in self.geographic_labels.items():
            for pattern in config["patterns"]:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    geographic_labels.append({
                        "label": label_type,
                        "confidence": config["confidence"]
                    })
                    break
        
        # Retourner les résultats
        result = []
        
        if origins_detected:
            # Prendre la provenance principale (la plus confiante)
            main_origin = max(origins_detected, key=lambda x: x["confidence"])
            result.append({
                "origin": main_origin["origin"],
                "text": main_origin["text"],
                "confidence": main_origin["confidence"],
                "all_origins_detected": [o["origin"] for o in origins_detected]
            })
        
        if geographic_labels:
            result.append({
                "geographic_labels": geographic_labels
            })
        
        return result
    
    def is_local(self, origin: str) -> bool:
        """
        Détermine si une provenance est considérée comme "locale".
        
        Args:
            origin: Type de provenance
        
        Returns:
            True si local, False sinon
        """
        local_origins = ["france", "local"]
        return origin.lower() in local_origins
    
    def get_transport_impact_factor(self, origin: str) -> Dict[str, float]:
        """
        Retourne les facteurs d'impact du transport selon la provenance.
        
        Source: ADEME
        
        Args:
            origin: Type de provenance
        
        Returns:
            Dictionnaire avec facteurs d'impact transport
        """
        factors = {
            "france": {
                "co2_kg_per_km_kg": 0.0005,  # kg CO2 / km / kg de produit
                "distance_km_avg": 200,       # Distance moyenne estimée
                "transport_type": "routier_france"
            },
            "local": {
                "co2_kg_per_km_kg": 0.0003,
                "distance_km_avg": 50,
                "transport_type": "routier_local"
            },
            "europe": {
                "co2_kg_per_km_kg": 0.0006,
                "distance_km_avg": 800,
                "transport_type": "routier_europe"
            },
            "espagne": {
                "co2_kg_per_km_kg": 0.0006,
                "distance_km_avg": 1000,
                "transport_type": "routier_europe"
            },
            "italie": {
                "co2_kg_per_km_kg": 0.0006,
                "distance_km_avg": 1200,
                "transport_type": "routier_europe"
            },
            "hors_europe": {
                "co2_kg_per_km_kg": 0.0015,
                "distance_km_avg": 5000,
                "transport_type": "aerien"
            }
        }
        
        return factors.get(origin, {
            "co2_kg_per_km_kg": 0.0006,
            "distance_km_avg": 500,
            "transport_type": "routier_europe"
        })

