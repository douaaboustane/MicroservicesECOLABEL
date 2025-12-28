"""
Service de détection de labels (bio, équitable, recyclé, etc.)
"""
import re
from typing import List, Dict, Any


class LabelDetector:
    """Détecte les labels dans le texte"""
    
    def __init__(self):
        # Patterns pour chaque type de label
        self.label_patterns = {
            "bio": {
                "patterns": [
                    r'\bbio\b',
                    r'\biologique\b',
                    r'\borganic\b',
                    r'\bab\b',  # Agriculture Biologique
                    r'\becocert\b'
                ],
                "confidence": 0.9
            },
            "fair_trade": {
                "patterns": [
                    r'\b(?:commerce )?équitable\b',
                    r'\bfair\s*trade\b',
                    r'\bmax havelaar\b',
                    r'\bfairtrade\b'
                ],
                "confidence": 0.9
            },
            "recyclable": {
                "patterns": [
                    r'\brecyclable\b',
                    r'\brecyclé\b',
                    r'\brecycled\b',
                    r'\bpoint vert\b'
                ],
                "confidence": 0.85
            },
            "local": {
                "patterns": [
                    r'\blocal\b',
                    r'\brégional\b',
                    r'\bfrançais\b',
                    r'\bfrance\b',
                    r'\bproduit en france\b'
                ],
                "confidence": 0.8
            },
            "aoc_aop": {
                "patterns": [
                    r'\baoc\b',
                    r'\baop\b',
                    r'\bappellation d\'origine\b'
                ],
                "confidence": 0.95
            },
            "igp": {
                "patterns": [
                    r'\bigp\b',
                    r'\bindication géographique\b'
                ],
                "confidence": 0.95
            },
            "label_rouge": {
                "patterns": [
                    r'\blabel rouge\b'
                ],
                "confidence": 0.95
            },
            "msc": {
                "patterns": [
                    r'\bmsc\b',
                    r'\bmarine stewardship\b',
                    r'\bpêche durable\b'
                ],
                "confidence": 0.9
            },
            "rainforest": {
                "patterns": [
                    r'\brainforest\b',
                    r'\brainforest alliance\b'
                ],
                "confidence": 0.9
            },
            "vegan": {
                "patterns": [
                    r'\bvegan\b',
                    r'\bvégétalien\b',
                    r'\bplant[-\s]?based\b'
                ],
                "confidence": 0.85
            }
        }
    
    def detect(self, text: str) -> List[Dict[str, Any]]:
        """
        Détecte les labels dans un texte.
        
        Args:
            text: Texte à analyser
        
        Returns:
            Liste de labels détectés
        """
        labels = []
        text_lower = text.lower()
        
        for label_type, config in self.label_patterns.items():
            for pattern in config["patterns"]:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    labels.append({
                        "label_type": label_type,
                        "label_name": match.group(0),
                        "confidence": config["confidence"]
                    })
                    break  # Une seule détection par type
        
        # Supprimer les doublons
        unique_labels = []
        seen_types = set()
        for label in labels:
            if label["label_type"] not in seen_types:
                unique_labels.append(label)
                seen_types.add(label["label_type"])
        
        return unique_labels
    
    def get_bonus_points(self, labels: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calcule les points bonus pour l'Eco-Score basés sur les labels.
        
        Args:
            labels: Liste de labels détectés
        
        Returns:
            Dictionnaire {type_label: points_bonus}
        """
        bonus_map = {
            "bio": 10.0,
            "fair_trade": 5.0,
            "recyclable": 5.0,
            "local": 5.0,
            "aoc_aop": 3.0,
            "igp": 3.0,
            "label_rouge": 5.0,
            "msc": 5.0,
            "rainforest": 5.0,
            "vegan": 3.0
        }
        
        bonus_points = {}
        for label in labels:
            label_type = label["label_type"]
            if label_type in bonus_map:
                bonus_points[label_type] = bonus_map[label_type] * label["confidence"]
        
        return bonus_points

