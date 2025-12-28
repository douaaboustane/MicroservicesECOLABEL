"""
Script d'entraînement des modèles de scoring
Génère des données synthétiques basées sur des règles logiques
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import joblib
from typing import Tuple, List

from app.config import settings
from app.services.feature_extractor import FeatureExtractor


def generate_synthetic_data(n_samples: int = 1000, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Génère des données synthétiques pour l'entraînement
    
    Args:
        n_samples: Nombre d'échantillons à générer
        random_state: Seed pour reproductibilité
    
    Returns:
        Tuple (X, y_numeric, y_letters)
    """
    np.random.seed(random_state)
    feature_extractor = FeatureExtractor()
    n_features = len(feature_extractor.get_feature_names())
    
    X = []
    y_numeric = []
    y_letters = []
    
    for i in range(n_samples):
        # Générer des features aléatoires mais réalistes
        features = []
        
        # 1. Impacts LCA (normalisés) - varier pour avoir toutes les classes
        # Pour avoir plus de A, générer des valeurs plus basses
        if i < n_samples * 0.2:  # 20% pour A
            co2 = np.random.uniform(0.5, 1.5)
            water = np.random.uniform(100, 500)
            energy = np.random.uniform(2, 5)
        elif i < n_samples * 0.4:  # 20% pour B
            co2 = np.random.uniform(1.5, 2.5)
            water = np.random.uniform(500, 1000)
            energy = np.random.uniform(5, 8)
        elif i < n_samples * 0.7:  # 30% pour C
            co2 = np.random.uniform(2.5, 3.5)
            water = np.random.uniform(1000, 1500)
            energy = np.random.uniform(8, 12)
        elif i < n_samples * 0.9:  # 20% pour D
            co2 = np.random.uniform(3.5, 4.5)
            water = np.random.uniform(1500, 2000)
            energy = np.random.uniform(12, 15)
        else:  # 10% pour E
            co2 = np.random.uniform(4.5, 5.0)
            water = np.random.uniform(1800, 2000)
            energy = np.random.uniform(13, 15)
        
        acidification = np.random.uniform(0.001, 0.01)
        eutrophisation = np.random.uniform(0.001, 0.01)
        
        features.extend([co2, water, energy, acidification, eutrophisation])
        
        # 2. Labels (booléens)
        has_bio = np.random.choice([0, 1], p=[0.7, 0.3])
        has_fair_trade = np.random.choice([0, 1], p=[0.8, 0.2])
        has_recyclable = np.random.choice([0, 1], p=[0.5, 0.5])
        has_local = np.random.choice([0, 1], p=[0.6, 0.4])
        
        features.extend([has_bio, has_fair_trade, has_recyclable, has_local])
        
        # 3. Ingrédients problématiques
        has_palm_oil = np.random.choice([0, 1], p=[0.7, 0.3])
        has_high_sugar = np.random.choice([0, 1], p=[0.6, 0.4])
        has_additives = np.random.choice([0, 1], p=[0.4, 0.6])
        
        features.extend([has_palm_oil, has_high_sugar, has_additives])
        
        # 4. Compteurs
        ingredient_count = np.random.randint(3, 20)
        allergen_count = np.random.randint(0, 5)
        label_count = np.random.randint(0, 3)
        
        features.extend([ingredient_count, allergen_count, label_count])
        
        # 5. Packaging (one-hot)
        packaging_types = ['plastique', 'verre', 'papier', 'metal']
        packaging_type = np.random.choice(packaging_types)
        features.extend([
            1.0 if packaging_type == 'plastique' else 0.0,
            1.0 if packaging_type == 'verre' else 0.0,
            1.0 if packaging_type == 'papier' else 0.0,
            1.0 if packaging_type == 'metal' else 0.0,
        ])
        
        # Calculer le score basé sur des règles logiques
        score = calculate_score_from_features(
            co2, water, energy,
            has_bio, has_fair_trade, has_recyclable, has_local,
            has_palm_oil, has_high_sugar, has_additives
        )
        
        # Convertir en lettre
        if score >= 80:
            letter = 'A'
        elif score >= 60:
            letter = 'B'
        elif score >= 40:
            letter = 'C'
        elif score >= 20:
            letter = 'D'
        else:
            letter = 'E'
        
        X.append(features)
        y_numeric.append(score)
        y_letters.append(letter)
    
    return np.array(X), np.array(y_numeric), np.array(y_letters)


def calculate_score_from_features(
    co2: float, water: float, energy: float,
    has_bio: int, has_fair_trade: int, has_recyclable: int, has_local: int,
    has_palm_oil: int, has_high_sugar: int, has_additives: int
) -> float:
    """
    Calcule un score basé sur des règles logiques (pour génération de données)
    """
    # Score de base basé sur impacts (0-70 points)
    # Normaliser les impacts (plus bas = mieux)
    co2_score = max(0, 30 - (co2 * 4))  # 0-30 points (ajusté pour avoir plus de A)
    water_score = max(0, 20 - (water / 60))  # 0-20 points
    energy_score = max(0, 20 - (energy * 1.2))  # 0-20 points
    
    base_score = co2_score + water_score + energy_score
    
    # Bonus (0-30 points) - augmenté pour avoir plus de A
    bonus = 0
    if has_bio:
        bonus += 10
    if has_fair_trade:
        bonus += 6
    if has_recyclable:
        bonus += 5
    if has_local:
        bonus += 4
    
    # Malus (-20 à 0 points)
    malus = 0
    if has_palm_oil:
        malus -= 12
    if has_high_sugar:
        malus -= 6
    if has_additives:
        malus -= 4
    
    final_score = base_score + bonus + malus
    return max(0, min(100, final_score))


def train_classification_model(X: np.ndarray, y_letters: np.ndarray) -> Tuple[RandomForestClassifier, StandardScaler]:
    """Entraîne le modèle de classification"""
    print("\n" + "=" * 80)
    print(" " * 20 + "🎯 ENTRAÎNEMENT CLASSIFICATION")
    print("=" * 80)
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_letters, test_size=0.2, random_state=42, stratify=y_letters
    )
    
    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entraînement
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    
    print(f"📊 Données d'entraînement: {len(X_train)} échantillons")
    print(f"📊 Données de test: {len(X_test)} échantillons")
    print(f"🏷️  Classes: {sorted(set(y_letters))}")
    print("\n⏳ Entraînement en cours...")
    
    model.fit(X_train_scaled, y_train)
    
    # Évaluation
    y_pred = model.predict(X_test_scaled)
    print("\n📈 Résultats:")
    # Obtenir les classes uniques présentes
    unique_classes = sorted(set(y_test) | set(y_pred))
    target_names = [c for c in ['A', 'B', 'C', 'D', 'E'] if c in unique_classes]
    print(classification_report(y_test, y_pred, labels=unique_classes, target_names=target_names))
    
    # Feature importance
    importances = model.feature_importances_
    feature_names = FeatureExtractor().get_feature_names()
    print("\n🔝 Top 10 Features les plus importantes:")
    indices = np.argsort(importances)[::-1][:10]
    for idx in indices:
        print(f"  {feature_names[idx]:30s}: {importances[idx]:.4f}")
    
    return model, scaler


def train_regression_model(X: np.ndarray, y_numeric: np.ndarray) -> Tuple[RandomForestRegressor, StandardScaler]:
    """Entraîne le modèle de régression"""
    print("\n" + "=" * 80)
    print(" " * 20 + "📊 ENTRAÎNEMENT RÉGRESSION")
    print("=" * 80)
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_numeric, test_size=0.2, random_state=42
    )
    
    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entraînement
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    
    print(f"📊 Données d'entraînement: {len(X_train)} échantillons")
    print(f"📊 Données de test: {len(X_test)} échantillons")
    print(f"📊 Score moyen: {y_numeric.mean():.2f} (min: {y_numeric.min():.2f}, max: {y_numeric.max():.2f})")
    print("\n⏳ Entraînement en cours...")
    
    model.fit(X_train_scaled, y_train)
    
    # Évaluation
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("\n📈 Résultats:")
    print(f"  MSE: {mse:.2f}")
    print(f"  RMSE: {np.sqrt(mse):.2f}")
    print(f"  R² Score: {r2:.4f}")
    
    # Feature importance
    importances = model.feature_importances_
    feature_names = FeatureExtractor().get_feature_names()
    print("\n🔝 Top 10 Features les plus importantes:")
    indices = np.argsort(importances)[::-1][:10]
    for idx in indices:
        print(f"  {feature_names[idx]:30s}: {importances[idx]:.4f}")
    
    return model, scaler


def save_models(classifier: RandomForestClassifier, regressor: RandomForestRegressor, 
                scaler_class: StandardScaler, scaler_reg: StandardScaler):
    """Sauvegarde les modèles entraînés"""
    print("\n" + "=" * 80)
    print(" " * 20 + "💾 SAUVEGARDE DES MODÈLES")
    print("=" * 80)
    
    # Créer les dossiers
    models_dir = Path(settings.CLASSIFICATION_MODEL_PATH).parent
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder classification
    classifier_path = Path(settings.CLASSIFICATION_MODEL_PATH)
    joblib.dump({
        'model': classifier,
        'scaler': scaler_class
    }, classifier_path)
    print(f"✅ Modèle de classification sauvegardé: {classifier_path}")
    
    # Sauvegarder régression
    regressor_path = Path(settings.REGRESSION_MODEL_PATH)
    joblib.dump({
        'model': regressor,
        'scaler': scaler_reg
    }, regressor_path)
    print(f"✅ Modèle de régression sauvegardé: {regressor_path}")
    
    print("\n" + "=" * 80)
    print(" " * 20 + "✅ ENTRAÎNEMENT TERMINÉ")
    print("=" * 80)
    print("\n💡 Les modèles seront automatiquement chargés au prochain démarrage du service.")


def main():
    """Fonction principale d'entraînement"""
    print("\n" + "=" * 80)
    print(" " * 15 + "🚀 ENTRAÎNEMENT DES MODÈLES DE SCORING")
    print("=" * 80)
    print("\n📝 Génération de données synthétiques...")
    
    # Générer les données
    X, y_numeric, y_letters = generate_synthetic_data(n_samples=2000, random_state=42)
    
    print(f"✅ {len(X)} échantillons générés")
    print(f"   • Features: {X.shape[1]}")
    print(f"   • Distribution des scores:")
    for letter in ['A', 'B', 'C', 'D', 'E']:
        count = np.sum(y_letters == letter)
        print(f"     - {letter}: {count} ({count/len(y_letters)*100:.1f}%)")
    
    # Entraîner classification
    classifier, scaler_class = train_classification_model(X, y_letters)
    
    # Entraîner régression
    regressor, scaler_reg = train_regression_model(X, y_numeric)
    
    # Sauvegarder
    save_models(classifier, regressor, scaler_class, scaler_reg)


if __name__ == "__main__":
    main()

