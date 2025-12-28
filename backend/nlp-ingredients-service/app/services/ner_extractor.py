"""
Service d'extraction NER avec spaCy
"""
import spacy
from typing import List, Dict, Any, Tuple
from pathlib import Path
import time

from app.config import settings


class NERExtractor:
    """Extracteur d'entités nommées avec spaCy"""
    
    def __init__(self):
        self.nlp = None
        self.loaded = False
        self.model_version = "v3.0"
        self.load_model()
    
    def load_model(self):
        """Charge le modèle NER"""
        try:
            model_path = Path(settings.NER_MODEL_PATH)
            if model_path.exists():
                self.nlp = spacy.load(model_path)
                self.loaded = True
                print(f"✅ Modèle NER chargé: {model_path}")
            else:
                print(f"❌ Modèle NER introuvable: {model_path}")
                print("   Chargement du modèle français de base...")
                self.nlp = spacy.load(settings.SPACY_MODEL)
                self.loaded = True
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
            self.loaded = False
    
    def extract(self, text: str) -> Tuple[List[Dict[str, Any]], float]:
        """
        Extrait les entités d'un texte.
        
        Args:
            text: Texte à analyser
        
        Returns:
            Tuple (entités, temps_traitement_ms)
        """
        if not self.loaded or not self.nlp:
            raise RuntimeError("Modèle NER non chargé")
        
        start_time = time.time()
        
        # Traiter le texte avec spaCy
        doc = self.nlp(text)
        
        # Extraire les entités
        entities = []
        for ent in doc.ents:
            # Calculer un score de confiance (simplifié)
            # Note: spaCy v3 ne fournit pas de score direct pour NER
            confidence = 0.9 if ent.label_ in ["INGREDIENT", "ALLERGEN", "QUANTITY"] else 0.7
            
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
                "confidence": confidence
            })
        
        processing_time = (time.time() - start_time) * 1000
        
        return entities, processing_time
    
    def get_model_info(self) -> Dict[str, Any]:
        """Retourne les informations du modèle"""
        if self.loaded and self.nlp:
            return {
                "loaded": True,
                "model_path": settings.NER_MODEL_PATH,
                "labels": list(self.nlp.get_pipe("ner").labels),
                "language": self.nlp.lang,
                "pipeline": self.nlp.pipe_names,
                "version": self.model_version
            }
        else:
            return {
                "loaded": False,
                "message": "Modèle NER non chargé"
            }
    
    def get_statistics(self, entities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calcule des statistiques sur les entités extraites"""
        stats = {
            "total": len(entities),
            "ingredients": 0,
            "allergens": 0,
            "quantities": 0,
            "others": 0
        }
        
        for entity in entities:
            label = entity["label"]
            if label == "INGREDIENT":
                stats["ingredients"] += 1
            elif label == "ALLERGEN":
                stats["allergens"] += 1
            elif label == "QUANTITY":
                stats["quantities"] += 1
            else:
                stats["others"] += 1
        
        return stats
    
    def calculate_confidence(self, entities: List[Dict[str, Any]]) -> float:
        """Calcule un score de confiance global"""
        if not entities:
            return 0.0
        
        total_confidence = sum(e.get("confidence", 0.0) for e in entities)
        return total_confidence / len(entities)

