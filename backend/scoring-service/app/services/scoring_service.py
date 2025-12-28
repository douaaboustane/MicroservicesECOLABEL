"""
Service principal de calcul de score écologique
"""
from typing import Dict, Any, Optional
import numpy as np

from app import schemas
from app.services.scoring_models import ScoringModels
from app.services.feature_extractor import FeatureExtractor


class ScoringService:
    """Service de calcul de score écologique"""
    
    def __init__(self):
        self.models = ScoringModels()
        self.feature_extractor = FeatureExtractor()
    
    def calculate_score(
        self,
        request: schemas.ScoreRequest,
        method: Optional[str] = None
    ) -> schemas.ScoreResponse:
        """
        Calcule le score écologique
        
        Args:
            request: Requête avec données LCA et NLP
            method: Méthode à utiliser ('classification', 'regression', 'hybrid')
        
        Returns:
            ScoreResponse avec le score calculé
        """
        method = method or request.method or "hybrid"
        
        # Extraire les features
        features = self.feature_extractor.extract(
            request.lca_data,
            request.nlp_data
        )
        features_array = np.array(features)
        
        # Calculer selon la méthode
        if method == "classification":
            result = self.models.predict_classification(features_array)
            return schemas.ScoreResponse(
                score_letter=result['score_letter'],
                score_numeric=self._letter_to_numeric(result['score_letter']),
                confidence=result['confidence'],
                method="classification",
                probabilities=schemas.ScoreProbabilities(**result['probabilities']),
                details={"probabilities": result['probabilities']}
            )
        
        elif method == "regression":
            result = self.models.predict_regression(features_array)
            return schemas.ScoreResponse(
                score_letter=result['score_letter'],
                score_numeric=result['score_numeric'],
                confidence=0.8,  # Confiance par défaut pour régression
                method="regression",
                details={"score_numeric": result['score_numeric']}
            )
        
        else:  # hybrid
            result = self.models.predict_hybrid(features_array)
            return schemas.ScoreResponse(
                score_letter=result['score_letter'],
                score_numeric=result['score_numeric'],
                confidence=result['confidence'],
                method=result['method'],
                probabilities=schemas.ScoreProbabilities(**result.get('probabilities', {})),
                details={
                    "method_used": result['method'],
                    "probabilities": result.get('probabilities', {})
                }
            )
    
    def _letter_to_numeric(self, letter: str) -> float:
        """Convertit une lettre en score numérique approximatif"""
        mapping = {
            'A': 90.0,
            'B': 70.0,
            'C': 50.0,
            'D': 30.0,
            'E': 10.0
        }
        return mapping.get(letter.upper(), 50.0)

