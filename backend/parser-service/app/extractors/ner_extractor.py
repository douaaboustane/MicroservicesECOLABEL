"""
Extracteur d'ingrédients basé sur le modèle NER spaCy entraîné
Utilise le modèle NER du data-pipeline pour extraire les ingrédients de manière structurée
"""
import spacy
from typing import List, Dict, Optional
from pathlib import Path


class NERExtractor:
    """Extracteur d'ingrédients utilisant le modèle NER entraîné"""
    
    def __init__(self, model_path: str = "app/models/ner_ingredients_v1"):
        """
        Initialise l'extracteur NER
        
        Args:
            model_path: Chemin vers le modèle spaCy entraîné
        """
        self.model_path = model_path
        self.nlp = None
        self._load_model()
    
    def _load_model(self):
        """Charge le modèle spaCy"""
        try:
            # Charger le modèle depuis le chemin
            model_full_path = Path(self.model_path)
            if not model_full_path.exists():
                raise FileNotFoundError(f"Modèle NER introuvable: {model_full_path}")
            
            self.nlp = spacy.load(str(model_full_path))
            print(f"✅ Modèle NER chargé: {self.model_path}")
            
        except Exception as e:
            print(f"⚠️  Erreur chargement modèle NER: {e}")
            print(f"   Utilisation du fallback (extraction basique)")
            self.nlp = None
    
    def extract_ingredients(self, text: str) -> List[Dict[str, any]]:
        """
        Extrait les ingrédients d'un texte avec le modèle NER
        
        Args:
            text: Texte contenant les ingrédients
            
        Returns:
            Liste d'ingrédients avec leurs métadonnées
            [
                {
                    "name": "farine de blé",
                    "quantity": "60%",
                    "start": 0,
                    "end": 14,
                    "label": "INGREDIENT"
                },
                ...
            ]
        """
        if not text or not text.strip():
            return []
        
        # Si le modèle n'est pas chargé, retourner vide
        if self.nlp is None:
            return []
        
        try:
            # Traiter le texte avec spaCy
            doc = self.nlp(text)
            
            ingredients = []
            quantities = []
            
            # Extraire les entités
            for ent in doc.ents:
                entity_data = {
                    "text": ent.text,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "label": ent.label_
                }
                
                if ent.label_ == "INGREDIENT":
                    ingredients.append(entity_data)
                elif ent.label_ == "QUANTITY":
                    quantities.append(entity_data)
            
            # Associer les quantités aux ingrédients (si proches)
            result = []
            for ing in ingredients:
                # Chercher une quantité proche
                quantity = None
                for qty in quantities:
                    # Si la quantité est juste avant ou après l'ingrédient
                    if abs(qty["start"] - ing["end"]) < 10 or abs(ing["start"] - qty["end"]) < 10:
                        quantity = qty["text"]
                        break
                
                result.append({
                    "name": ing["text"],
                    "quantity": quantity,
                    "start": ing["start"],
                    "end": ing["end"],
                    "label": ing["label"]
                })
            
            return result
            
        except Exception as e:
            print(f"Erreur extraction NER: {e}")
            return []
    
    def extract_ingredients_as_text(self, text: str) -> str:
        """
        Extrait les ingrédients et les retourne sous forme de texte simple
        
        Args:
            text: Texte contenant les ingrédients
            
        Returns:
            Chaîne de caractères avec les ingrédients séparés par des virgules
        """
        ingredients = self.extract_ingredients(text)
        
        if not ingredients:
            return ""
        
        # Formater en texte
        ingredient_list = []
        for ing in ingredients:
            if ing.get("quantity"):
                ingredient_list.append(f"{ing['name']} ({ing['quantity']})")
            else:
                ingredient_list.append(ing['name'])
        
        return ", ".join(ingredient_list)
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Retourne les informations sur le modèle chargé
        
        Returns:
            Dict avec les métadonnées du modèle
        """
        if self.nlp is None:
            return {
                "loaded": False,
                "error": "Model not loaded"
            }
        
        return {
            "loaded": True,
            "model_path": self.model_path,
            "labels": list(self.nlp.get_pipe("ner").labels),
            "language": self.nlp.lang,
            "pipeline": self.nlp.pipe_names
        }

