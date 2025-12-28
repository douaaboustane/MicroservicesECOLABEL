"""
Service d'extraction des matériaux d'emballage
"""
import re
from typing import List, Dict, Any, Optional


class PackagingExtractor:
    """Détecte les matériaux d'emballage dans le texte"""
    
    def __init__(self):
        # Patterns pour détecter les types d'emballage
        self.packaging_patterns = {
            "plastique": {
                "patterns": [
                    r'\bplastique\b',
                    r'\bpolyéthylène\b',
                    r'\bpet\b',
                    r'\bpehd\b',
                    r'\bpebd\b',
                    r'\bpp\b',
                    r'\bps\b',
                    r'\bpvc\b',
                    r'\bplastic\b',
                    r'\bpolyethylene\b',
                    r'\bemballage plastique\b'
                ],
                "confidence": 0.9
            },
            "verre": {
                "patterns": [
                    r'\bverre\b',
                    r'\bglass\b',
                    r'\bbouteille en verre\b',
                    r'\bpot en verre\b',
                    r'\bverre recyclé\b'
                ],
                "confidence": 0.95
            },
            "papier": {
                "patterns": [
                    r'\bpapier\b',
                    r'\bpaper\b',
                    r'\bemballage papier\b',
                    r'\bsachet papier\b',
                    r'\bpapier recyclé\b'
                ],
                "confidence": 0.9
            },
            "carton": {
                "patterns": [
                    r'\bcarton\b',
                    r'\bcardboard\b',
                    r'\bboîte en carton\b',
                    r'\bemballage carton\b',
                    r'\bcarton recyclé\b'
                ],
                "confidence": 0.9
            },
            "metal": {
                "patterns": [
                    r'\bmétal\b',
                    r'\bmetal\b',
                    r'\baluminium\b',
                    r'\balu\b',
                    r'\bacier\b',
                    r'\bsteel\b',
                    r'\bboîte métallique\b',
                    r'\bcanette\b'
                ],
                "confidence": 0.9
            },
            "bois": {
                "patterns": [
                    r'\bbois\b',
                    r'\bwood\b',
                    r'\bemballage bois\b',
                    r'\bcarton bois\b'
                ],
                "confidence": 0.85
            },
            "bioplastique": {
                "patterns": [
                    r'\bbioplastique\b',
                    r'\bbiodegradable\b',
                    r'\bcompostable\b',
                    r'\bpla\b'
                ],
                "confidence": 0.9
            }
        }
        
        # Patterns pour détecter si recyclable
        self.recyclable_patterns = [
            r'\brecyclable\b',
            r'\brecyclé\b',
            r'\brecycled\b',
            r'\bpoint vert\b',
            r'\btriman\b'
        ]
        
        # Patterns pour détecter le poids de l'emballage
        self.weight_patterns = [
            r'(\d+(?:[.,]\d+)?)\s*(?:g|kg|grammes?|kilogrammes?)\s*(?:d\'?emballage|d\'?emb)',
            r'emballage\s*:?\s*(\d+(?:[.,]\d+)?)\s*(?:g|kg)',
            r'poids\s*(?:emballage|emb)\s*:?\s*(\d+(?:[.,]\d+)?)\s*(?:g|kg)'
        ]
    
    def extract(self, text: str) -> List[Dict[str, Any]]:
        """
        Extrait les informations sur l'emballage.
        
        Args:
            text: Texte à analyser
        
        Returns:
            Liste d'informations d'emballage détectées
        """
        if not text:
            return []
        
        text_lower = text.lower()
        packaging_detected = []
        
        # Détecter les types d'emballage
        for packaging_type, config in self.packaging_patterns.items():
            for pattern in config["patterns"]:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    packaging_detected.append({
                        "type": packaging_type,
                        "text": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                        "confidence": config["confidence"]
                    })
                    break  # Une seule détection par type
        
        # Détecter si recyclable
        is_recyclable = False
        for pattern in self.recyclable_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                is_recyclable = True
                break
        
        # Détecter le poids
        weight = None
        weight_unit = None
        for pattern in self.weight_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                weight_str = match.group(1).replace(',', '.')
                try:
                    weight = float(weight_str)
                    # Déterminer l'unité
                    if 'kg' in match.group(0) or 'kilogramme' in match.group(0):
                        weight_unit = "kg"
                    else:
                        weight_unit = "g"
                    break
                except ValueError:
                    continue
        
        # Si on a détecté au moins un type d'emballage
        if packaging_detected:
            # Prendre le premier (ou le plus confiant)
            main_packaging = packaging_detected[0]
            
            return [{
                "type": main_packaging["type"],
                "text": main_packaging["text"],
                "recyclable": is_recyclable,
                "weight": weight,
                "weight_unit": weight_unit,
                "confidence": main_packaging["confidence"],
                "all_types_detected": [p["type"] for p in packaging_detected]
            }]
        
        return []
    
    def get_packaging_impact_factor(self, packaging_type: str) -> Dict[str, float]:
        """
        Retourne les facteurs d'impact environnemental par type d'emballage.
        
        Source: ADEME
        
        Args:
            packaging_type: Type d'emballage
        
        Returns:
            Dictionnaire avec facteurs d'impact (CO2, eau, énergie)
        """
        factors = {
            "plastique": {
                "co2_kg_per_kg": 1.5,      # kg CO2 / kg d'emballage
                "eau_m3_per_kg": 0.01,     # m³ / kg
                "energie_mj_per_kg": 45.0   # MJ / kg
            },
            "verre": {
                "co2_kg_per_kg": 0.8,
                "eau_m3_per_kg": 0.005,
                "energie_mj_per_kg": 12.0
            },
            "papier": {
                "co2_kg_per_kg": 0.3,
                "eau_m3_per_kg": 0.002,
                "energie_mj_per_kg": 8.0
            },
            "carton": {
                "co2_kg_per_kg": 0.4,
                "eau_m3_per_kg": 0.003,
                "energie_mj_per_kg": 10.0
            },
            "metal": {
                "co2_kg_per_kg": 2.0,
                "eau_m3_per_kg": 0.015,
                "energie_mj_per_kg": 50.0
            },
            "bois": {
                "co2_kg_per_kg": 0.2,
                "eau_m3_per_kg": 0.001,
                "energie_mj_per_kg": 5.0
            },
            "bioplastique": {
                "co2_kg_per_kg": 0.5,
                "eau_m3_per_kg": 0.008,
                "energie_mj_per_kg": 15.0
            }
        }
        
        return factors.get(packaging_type, {
            "co2_kg_per_kg": 1.0,
            "eau_m3_per_kg": 0.01,
            "energie_mj_per_kg": 30.0
        })

