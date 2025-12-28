"""
Extracteur de features pour les modèles ML
"""
from typing import Dict, Any, List
from app import schemas


class FeatureExtractor:
    """Extrait et prépare les features depuis LCA et NLP data"""
    
    def __init__(self):
        self.feature_names = [
            # Impacts LCA (normalisés)
            'co2_kg',
            'water_liters',
            'energy_mj',
            'acidification',
            'eutrophisation',
            
            # Labels détectés (booléens)
            'has_bio_label',
            'has_fair_trade',
            'has_recyclable_packaging',
            'has_local_origin',
            
            # Ingrédients problématiques
            'has_palm_oil',
            'has_high_sugar',
            'has_additives',
            
            # Compteurs
            'ingredient_count',
            'allergen_count',
            'label_count',
            
            # Packaging
            'packaging_type_plastique',
            'packaging_type_verre',
            'packaging_type_papier',
            'packaging_type_metal',
        ]
    
    def extract(self, lca_data: schemas.LCAInput, nlp_data: schemas.NLPInput) -> List[float]:
        """
        Extrait les features depuis les données LCA et NLP
        
        Returns:
            Liste de features normalisées
        """
        features = []
        
        # 1. Impacts LCA
        features.append(lca_data.co2_kg)
        features.append(lca_data.water_liters)
        features.append(lca_data.energy_mj)
        features.append(lca_data.acidification or 0.0)
        features.append(lca_data.eutrophisation or 0.0)
        
        # 2. Labels (booléens)
        features.append(1.0 if nlp_data.has_bio_label else 0.0)
        features.append(1.0 if nlp_data.has_fair_trade else 0.0)
        features.append(1.0 if nlp_data.packaging_recyclable else 0.0)
        features.append(1.0 if (nlp_data.origin and 'france' in nlp_data.origin.lower()) else 0.0)
        
        # 3. Ingrédients problématiques
        features.append(1.0 if nlp_data.has_palm_oil else 0.0)
        features.append(1.0 if nlp_data.has_high_sugar else 0.0)
        features.append(1.0 if nlp_data.has_additives else 0.0)
        
        # 4. Compteurs
        features.append(float(len(nlp_data.ingredients)))
        features.append(float(len(nlp_data.allergens)))
        features.append(float(len(nlp_data.labels)))
        
        # 5. Type d'emballage (one-hot encoding simplifié)
        packaging_type = (nlp_data.packaging_type or "").lower()
        features.append(1.0 if 'plastique' in packaging_type else 0.0)
        features.append(1.0 if 'verre' in packaging_type else 0.0)
        features.append(1.0 if 'papier' in packaging_type or 'carton' in packaging_type else 0.0)
        features.append(1.0 if 'metal' in packaging_type or 'aluminium' in packaging_type else 0.0)
        
        return features
    
    def get_feature_names(self) -> List[str]:
        """Retourne les noms des features"""
        return self.feature_names

