"""
Script d'entraînement avec de vraies données labellisées
Utilise les données Open Food Facts avec ecoscore_grade
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from typing import List, Dict, Any, Optional, Tuple
try:
    from tqdm import tqdm
except ImportError:
    # Fallback si tqdm n'est pas disponible
    def tqdm(iterable, *args, **kwargs):
        return iterable

# Ajouter le chemin parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.services.train_models import (
    train_classification_model,
    train_regression_model,
    save_models
)
from app.services.feature_extractor import FeatureExtractor
from app.config import settings


class RealDataTrainer:
    """Entraîne les modèles avec de vraies données"""
    
    def __init__(
        self,
        parser_service_url: str = "http://parser-service:8001",
        nlp_service_url: str = "http://nlp-service:8003",
        lca_service_url: str = "http://lca-service:8004"
    ):
        self.parser_url = parser_service_url
        self.nlp_url = nlp_service_url
        self.lca_url = lca_service_url
        self.feature_extractor = FeatureExtractor()
    
    def load_openfoodfacts_data(self, csv_path: str) -> pd.DataFrame:
        """Charge les données Open Food Facts"""
        from app.services.data_preparer import load_and_prepare_data
        return load_and_prepare_data(csv_path, max_samples=5000, min_samples_per_class=50)
    
    def extract_features_from_product(
        self,
        product: Dict[str, Any],
        ingredients_text: Optional[str] = None
    ) -> Optional[Tuple[np.ndarray, str, float]]:
        """
        Extrait les features depuis un produit réel
        
        Returns:
            Tuple (features, ecoscore_letter, ecoscore_numeric) ou None
        """
        try:
            # 1. Extraire les ingrédients avec NLP Service
            ingredients_text = ingredients_text or product.get('ingredients_text', '')
            if not ingredients_text or len(ingredients_text) < 5:
                return None
            
            # Appel NLP Service (simulé pour l'instant - on peut utiliser les données existantes)
            nlp_data = self._extract_nlp_features_from_product(product)
            
            # 2. Calculer LCA (simulé - on peut utiliser Agribalyse)
            lca_data = self._estimate_lca_from_product(product, nlp_data)
            
            # 3. Extraire features
            from app import schemas
            lca_input = schemas.LCAInput(
                co2_kg=lca_data['co2_kg'],
                water_liters=lca_data['water_liters'],
                energy_mj=lca_data['energy_mj'],
                acidification=lca_data.get('acidification', 0.0),
                eutrophisation=lca_data.get('eutrophisation', 0.0)
            )
            
            nlp_input = schemas.NLPInput(
                ingredients=nlp_data.get('ingredients', []),
                allergens=nlp_data.get('allergens', []),
                labels=nlp_data.get('labels', []),
                packaging_type=nlp_data.get('packaging_type'),
                packaging_recyclable=nlp_data.get('packaging_recyclable'),
                origin=nlp_data.get('origin'),
                has_bio_label=nlp_data.get('has_bio_label'),
                has_fair_trade=nlp_data.get('has_fair_trade'),
                has_palm_oil=nlp_data.get('has_palm_oil'),
                has_high_sugar=nlp_data.get('has_high_sugar'),
                has_additives=nlp_data.get('has_additives')
            )
            
            features = self.feature_extractor.extract(lca_input, nlp_input)
            
            # 4. Récupérer le score réel
            ecoscore_grade = product.get('ecoscore_grade', '').lower()
            if ecoscore_grade not in ['a', 'b', 'c', 'd', 'e']:
                return None
            
            # Convertir en score numérique approximatif
            score_mapping = {'a': 90, 'b': 70, 'c': 50, 'd': 30, 'e': 10}
            score_numeric = score_mapping.get(ecoscore_grade, 50)
            
            return np.array(features), ecoscore_grade.upper(), float(score_numeric)
        
        except Exception as e:
            print(f"⚠️  Erreur pour produit {product.get('code', 'unknown')}: {e}")
            return None
    
    def _extract_nlp_features_from_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Extrait les features NLP depuis les données du produit"""
        from app.services.data_preparer import extract_nlp_features
        return extract_nlp_features(product)
    
    def _estimate_lca_from_product(
        self,
        product: Dict[str, Any],
        nlp_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Estime les impacts LCA depuis les données du produit
        (Simplifié - en production, utiliser le LCA Service)
        """
        from app.services.data_preparer import estimate_lca_impacts
        return estimate_lca_impacts(product, nlp_data)
    
    def prepare_training_data(
        self,
        df: pd.DataFrame,
        max_samples: int = 2000,
        min_samples_per_class: int = 50
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Prépare les données d'entraînement depuis le DataFrame
        
        Args:
            df: DataFrame avec produits Open Food Facts
            max_samples: Nombre maximum d'échantillons
            min_samples_per_class: Minimum par classe
        
        Returns:
            Tuple (X, y_numeric, y_letters)
        """
        print(f"\n🔄 Préparation des données d'entraînement...")
        print(f"   Max samples: {max_samples}")
        print(f"   Min par classe: {min_samples_per_class}")
        
        X_list = []
        y_numeric_list = []
        y_letters_list = []
        
        # Échantillonner équitablement par classe
        classes = ['a', 'b', 'c', 'd', 'e']
        samples_per_class = max_samples // len(classes)
        
        for grade in classes:
            df_class = df[df['ecoscore_grade'] == grade].copy()
            if len(df_class) < min_samples_per_class:
                print(f"⚠️  Classe {grade.upper()}: seulement {len(df_class)} échantillons (min: {min_samples_per_class})")
                continue
            
            # Échantillonner
            n_samples = min(samples_per_class, len(df_class))
            df_sampled = df_class.sample(n=n_samples, random_state=42)
            
            print(f"\n📊 Classe {grade.upper()}: {n_samples} échantillons")
            
            # Extraire les features
            for idx, row in tqdm(df_sampled.iterrows(), total=len(df_sampled), desc=f"  {grade.upper()}"):
                result = self.extract_features_from_product(row.to_dict())
                if result:
                    features, letter, score = result
                    X_list.append(features)
                    y_numeric_list.append(score)
                    y_letters_list.append(letter)
        
        if len(X_list) == 0:
            raise ValueError("Aucune donnée valide extraite")
        
        print(f"\n✅ {len(X_list)} échantillons préparés")
        print(f"   Distribution:")
        for letter in ['A', 'B', 'C', 'D', 'E']:
            count = y_letters_list.count(letter)
            if count > 0:
                print(f"     - {letter}: {count} ({count/len(y_letters_list)*100:.1f}%)")
        
        return np.array(X_list), np.array(y_numeric_list), np.array(y_letters_list)
    
    def train_with_real_data(
        self,
        csv_path: str,
        max_samples: int = 2000
    ):
        """Entraîne les modèles avec de vraies données"""
        print("\n" + "=" * 80)
        print(" " * 15 + "🚀 ENTRAÎNEMENT AVEC DONNÉES RÉELLES")
        print("=" * 80)
        
        # 1. Charger les données
        df = self.load_openfoodfacts_data(csv_path)
        if df.empty:
            print("❌ Aucune donnée valide trouvée")
            return
        
        # 2. Préparer les données d'entraînement
        X, y_numeric, y_letters = self.prepare_training_data(df, max_samples=max_samples)
        
        # 3. Entraîner classification
        classifier, scaler_class = train_classification_model(X, y_letters)
        
        # 4. Entraîner régression
        regressor, scaler_reg = train_regression_model(X, y_numeric)
        
        # 5. Sauvegarder
        save_models(classifier, regressor, scaler_class, scaler_reg)
        
        print("\n" + "=" * 80)
        print(" " * 20 + "✅ ENTRAÎNEMENT TERMINÉ")
        print("=" * 80)
        print("\n💡 Les modèles améliorés seront chargés au prochain démarrage du service.")


def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Entraîner les modèles avec de vraies données")
    parser.add_argument(
        '--data',
        type=str,
        default='../../data-pipeline/datasets/cleaned/products_cleaned.csv',
        help='Chemin vers le fichier CSV avec données Open Food Facts'
    )
    parser.add_argument(
        '--max-samples',
        type=int,
        default=2000,
        help='Nombre maximum d\'échantillons à utiliser'
    )
    
    args = parser.parse_args()
    
    # Résoudre le chemin
    data_path = Path(args.data)
    if not data_path.is_absolute():
        # Chemin relatif depuis le service
        data_path = Path(__file__).parent.parent.parent.parent.parent / args.data
    
    if not data_path.exists():
        print(f"❌ Fichier non trouvé: {data_path}")
        print(f"💡 Utilisez le scraper Open Food Facts pour générer les données")
        return
    
    trainer = RealDataTrainer()
    trainer.train_with_real_data(str(data_path), max_samples=args.max_samples)


if __name__ == "__main__":
    main()

