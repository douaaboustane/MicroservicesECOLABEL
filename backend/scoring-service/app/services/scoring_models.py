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
            # Fallback: calculer un score basé sur les règles
            result = self._calculate_rule_based_score(features, method="classification")
            return result
        
        # Scaling
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Prédiction
        letter = self.classifier.predict(features_scaled)[0]
        probabilities = self.classifier.predict_proba(features_scaled)[0]
        
        # Mapping des classes (assumant ordre A, B, C, D, E)
        class_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
        letter_str = class_mapping.get(letter, 'C')
        
        # Convertir lettre en score numérique approximatif
        letter_to_score = {'A': 90.0, 'B': 70.0, 'C': 50.0, 'D': 30.0, 'E': 10.0}
        score_numeric = letter_to_score.get(letter_str, 50.0)
        
        return {
            'score_letter': letter_str,
            'score_numeric': score_numeric,
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
            # Fallback: calculer un score basé sur les règles
            return self._calculate_rule_based_score(features, method="regression")
        
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
    
    def _calculate_rule_based_score(
        self,
        features: np.ndarray,
        method: str = "regression"
    ) -> Dict[str, Any]:
        """
        Calcule un score basé sur des règles logiques quand les modèles ML ne sont pas disponibles.
        
        Logique du score:
        - Base: 50 points (score neutre)
        - CO2: -10 à +20 points selon impact (0-6kg)
        - Eau: -10 à +20 points selon impact (0-2000L)
        - Énergie: -5 à +10 points selon impact (0-20 MJ)
        - Labels positifs: +5 points chacun (bio, équitable)
        - Packaging recyclable: +5 points
        - Origine locale: +3 points
        - Ingrédients problématiques: -5 points chacun (palme, sucre, additifs)
        - Packaging plastique: -5 points
        - Packaging verre/papier: +3 points
        
        Args:
            features: Array de 24 features
            method: "classification" ou "regression"
        
        Returns:
            Dict avec score_letter, score_numeric, probabilities (si classification), confidence
        """
        # Extraire les features (ordre défini dans FeatureExtractor)
        co2_kg = float(features[0])
        water_liters = float(features[1])
        energy_mj = float(features[2])
        acidification = float(features[3])
        eutrophisation = float(features[4])
        
        has_bio = bool(features[5])
        has_fair_trade = bool(features[6])
        has_recyclable = bool(features[7])
        has_local = bool(features[8])
        
        has_palm_oil = bool(features[9])
        has_high_sugar = bool(features[10])
        has_additives = bool(features[11])
        
        ingredient_count = float(features[12])
        allergen_count = float(features[13])
        label_count = float(features[14])
        
        packaging_plastique = bool(features[15])
        packaging_verre = bool(features[16])
        packaging_papier = bool(features[17])
        packaging_metal = bool(features[18])
        
        # Score de base
        base_score = 50.0
        
        # 1. Impact CO2 (0-6kg) - Plus bas = meilleur
        if co2_kg < 0.5:
            co2_score = +20  # Excellent
        elif co2_kg < 1.0:
            co2_score = +15  # Très bon
        elif co2_kg < 2.0:
            co2_score = +10  # Bon
        elif co2_kg < 3.0:
            co2_score = +5   # Moyen
        elif co2_kg < 4.0:
            co2_score = 0    # Neutre
        elif co2_kg < 5.0:
            co2_score = -5   # Faible
        elif co2_kg < 6.0:
            co2_score = -8   # Très faible
        else:
            co2_score = -10  # Très mauvais
        
        # 2. Impact Eau (0-2000L) - Plus bas = meilleur
        if water_liters < 50:
            water_score = +20  # Excellent
        elif water_liters < 100:
            water_score = +15  # Très bon
        elif water_liters < 300:
            water_score = +10  # Bon
        elif water_liters < 500:
            water_score = +5   # Moyen
        elif water_liters < 1000:
            water_score = 0   # Neutre
        elif water_liters < 1500:
            water_score = -5  # Faible
        elif water_liters < 2000:
            water_score = -8  # Très faible
        else:
            water_score = -10  # Très mauvais
        
        # 3. Impact Énergie (0-20 MJ) - Plus bas = meilleur
        if energy_mj < 2:
            energy_score = +10  # Excellent
        elif energy_mj < 4:
            energy_score = +7   # Très bon
        elif energy_mj < 6:
            energy_score = +5   # Bon
        elif energy_mj < 8:
            energy_score = +2   # Moyen
        elif energy_mj < 12:
            energy_score = 0    # Neutre
        elif energy_mj < 16:
            energy_score = -3   # Faible
        else:
            energy_score = -5   # Très faible
        
        # 4. Bonus pour labels positifs
        bonus_labels = 0
        if has_bio:
            bonus_labels += 5
        if has_fair_trade:
            bonus_labels += 5
        if has_recyclable:
            bonus_labels += 5
        if has_local:
            bonus_labels += 3
        
        # 5. Pénalités pour ingrédients problématiques
        penalty_ingredients = 0
        if has_palm_oil:
            penalty_ingredients -= 5
        if has_high_sugar:
            penalty_ingredients -= 3
        if has_additives:
            penalty_ingredients -= 3
        
        # 6. Impact du packaging
        packaging_score = 0
        if packaging_plastique:
            packaging_score -= 5  # Plastique = pénalité
        elif packaging_verre:
            packaging_score += 2  # Verre = léger bonus (recyclable)
        elif packaging_papier:
            packaging_score += 3  # Papier = bonus (recyclable et renouvelable)
        elif packaging_metal:
            packaging_score += 1  # Métal = neutre (recyclable mais énergivore)
        
        # 7. Bonus pour simplicité (moins d'ingrédients = mieux)
        if ingredient_count <= 3:
            simplicity_bonus = +3
        elif ingredient_count <= 5:
            simplicity_bonus = +1
        elif ingredient_count > 15:
            simplicity_bonus = -2  # Trop d'ingrédients = pénalité
        else:
            simplicity_bonus = 0
        
        # Calcul du score final
        final_score = (
            base_score +
            co2_score +
            water_score +
            energy_score +
            bonus_labels +
            penalty_ingredients +
            packaging_score +
            simplicity_bonus
        )
        
        # Clamp entre 0 et 100
        final_score = max(0.0, min(100.0, final_score))
        
        # Conversion en lettre
        if final_score >= 80:
            letter = "A"
        elif final_score >= 60:
            letter = "B"
        elif final_score >= 40:
            letter = "C"
        elif final_score >= 20:
            letter = "D"
        else:
            letter = "E"
        
        # Générer des probabilités pour la classification (basées sur la distance au score)
        if method == "classification":
            # Calculer probabilités basées sur la distance au score
            distances = {
                'A': abs(final_score - 90),
                'B': abs(final_score - 70),
                'C': abs(final_score - 50),
                'D': abs(final_score - 30),
                'E': abs(final_score - 10)
            }
            
            # Convertir distances en probabilités (plus proche = plus probable)
            max_dist = max(distances.values())
            probabilities = {
                letter: max(0.01, 1.0 - (distances[letter] / max_dist) * 0.8)
                for letter in ['A', 'B', 'C', 'D', 'E']
            }
            
            # Normaliser pour que la somme = 1.0
            total = sum(probabilities.values())
            probabilities = {k: v / total for k, v in probabilities.items()}
            
            confidence = probabilities[letter]
            
            return {
                'score_letter': letter,
                'score_numeric': round(final_score, 1),
                'probabilities': probabilities,
                'confidence': round(confidence, 3)
            }
        else:
            # Régression: retourner juste le score numérique
            return {
                'score_numeric': round(final_score, 1),
                'score_letter': letter
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

