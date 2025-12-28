"""
Modèles ML pour le scoring (Classification + Régression)
"""
import joblib
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd

from app.config import settings
from app.services.feature_extractor import FeatureExtractor


class ScoringModels:
    """Gestionnaire des modèles ML de scoring"""
    
    def __init__(self):
        self.classifier: Optional[RandomForestClassifier] = None
        self.regressor: Optional[RandomForestRegressor] = None
        self.scaler = StandardScaler()
        self.feature_extractor = FeatureExtractor()
        self.classifier_loaded = False
        self.regressor_loaded = False
        
        # Charger les modèles si disponibles
        self.load_models()
    
    def load_models(self):
        """Charge les modèles depuis les fichiers"""
        # Classification
        classifier_path = Path(settings.CLASSIFICATION_MODEL_PATH)
        if classifier_path.exists():
            try:
                model_data = joblib.load(classifier_path)
                if isinstance(model_data, dict):
                    self.classifier = model_data.get('model')
                    self.scaler = model_data.get('scaler', StandardScaler())
                else:
                    self.classifier = model_data
                self.classifier_loaded = True
                print(f"✅ Modèle de classification chargé: {classifier_path}")
            except Exception as e:
                print(f"⚠️  Erreur chargement classification: {e}")
        
        # Régression
        regressor_path = Path(settings.REGRESSION_MODEL_PATH)
        if regressor_path.exists():
            try:
                model_data = joblib.load(regressor_path)
                if isinstance(model_data, dict):
                    self.regressor = model_data.get('model')
                    if 'scaler' in model_data:
                        self.scaler = model_data['scaler']
                else:
                    self.regressor = model_data
                self.regressor_loaded = True
                print(f"✅ Modèle de régression chargé: {regressor_path}")
            except Exception as e:
                print(f"⚠️  Erreur chargement régression: {e}")
        
        # Si aucun modèle chargé, créer des modèles par défaut (non entraînés)
        if not self.classifier_loaded:
            print("⚠️  Modèle de classification non trouvé, création d'un modèle par défaut")
            self.classifier = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                class_weight='balanced',
                random_state=42
            )
        
        if not self.regressor_loaded:
            print("⚠️  Modèle de régression non trouvé, création d'un modèle par défaut")
            self.regressor = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42
            )
    
    def predict_classification(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Prédit directement A-E avec le modèle de classification
        
        Args:
            features: Array de features normalisées
            
        Returns:
            Dict avec score_letter, probabilities, confidence
        """
        if not self.classifier_loaded:
            raise RuntimeError("Modèle de classification non entraîné")
        
        # Scaling
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Prédiction
        letter = self.classifier.predict(features_scaled)[0]
        probabilities = self.classifier.predict_proba(features_scaled)[0]
        
        # Mapping des classes (assumant ordre A, B, C, D, E)
        class_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
        letter_str = class_mapping.get(letter, 'C')
        
        return {
            'score_letter': letter_str,
            'probabilities': {
                'A': float(probabilities[0]),
                'B': float(probabilities[1]),
                'C': float(probabilities[2]),
                'D': float(probabilities[3]),
                'E': float(probabilities[4])
            },
            'confidence': float(max(probabilities))
        }
    
    def predict_regression(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Prédit score 0-100 avec le modèle de régression
        
        Args:
            features: Array de features normalisées
            
        Returns:
            Dict avec score_numeric, score_letter
        """
        if not self.regressor_loaded:
            raise RuntimeError("Modèle de régression non entraîné")
        
        # Scaling
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Prédiction
        score_numeric = self.regressor.predict(features_scaled)[0]
        score_numeric = max(0.0, min(100.0, float(score_numeric)))  # Clamp 0-100
        
        # Conversion en lettre
        if score_numeric >= 80:
            letter = "A"
        elif score_numeric >= 60:
            letter = "B"
        elif score_numeric >= 40:
            letter = "C"
        elif score_numeric >= 20:
            letter = "D"
        else:
            letter = "E"
        
        return {
            'score_numeric': round(score_numeric, 1),
            'score_letter': letter
        }
    
    def predict_hybrid(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Approche hybride : combine classification et régression
        
        Args:
            features: Array de features normalisées
            
        Returns:
            Dict avec score_letter, score_numeric, confidence, method
        """
        # Classification
        class_result = self.predict_classification(features)
        letter_class = class_result['score_letter']
        proba_class = class_result['probabilities']
        confidence_class = class_result['confidence']
        
        # Régression
        reg_result = self.predict_regression(features)
        score_num = reg_result['score_numeric']
        letter_reg = reg_result['score_letter']
        
        # Consensus
        if letter_class == letter_reg:
            # Les deux sont d'accord → confiance élevée
            return {
                'score_letter': letter_class,
                'score_numeric': score_num,
                'confidence': confidence_class,
                'method': 'hybrid_consensus',
                'probabilities': proba_class
            }
        else:
            # Désaccord → utiliser celui avec plus de confiance
            if confidence_class > 0.7:
                return {
                    'score_letter': letter_class,
                    'score_numeric': score_num,
                    'confidence': confidence_class,
                    'method': 'hybrid_classification',
                    'probabilities': proba_class
                }
            else:
                # Utiliser la régression (plus fiable pour valeurs intermédiaires)
                return {
                    'score_letter': letter_reg,
                    'score_numeric': score_num,
                    'confidence': 0.6,  # Confiance moyenne
                    'method': 'hybrid_regression',
                    'probabilities': proba_class
                }
    
    def save_models(self, classifier_path: Optional[str] = None, regressor_path: Optional[str] = None):
        """Sauvegarde les modèles entraînés"""
        classifier_path = classifier_path or settings.CLASSIFICATION_MODEL_PATH
        regressor_path = regressor_path or settings.REGRESSION_MODEL_PATH
        
        # Créer les dossiers si nécessaire
        Path(classifier_path).parent.mkdir(parents=True, exist_ok=True)
        Path(regressor_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder
        if self.classifier:
            joblib.dump({
                'model': self.classifier,
                'scaler': self.scaler
            }, classifier_path)
            print(f"✅ Modèle de classification sauvegardé: {classifier_path}")
        
        if self.regressor:
            joblib.dump({
                'model': self.regressor,
                'scaler': self.scaler
            }, regressor_path)
            print(f"✅ Modèle de régression sauvegardé: {regressor_path}")

