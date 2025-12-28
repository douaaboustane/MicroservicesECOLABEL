"""
Préparation des données pour l'entraînement avec données réelles
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import re


def load_and_prepare_data(
    csv_path: str,
    max_samples: int = 2000,
    min_samples_per_class: int = 50
) -> pd.DataFrame:
    """
    Charge et prépare les données depuis un CSV Open Food Facts
    
    Args:
        csv_path: Chemin vers le fichier CSV
        max_samples: Nombre maximum d'échantillons
        min_samples_per_class: Minimum par classe
    
    Returns:
        DataFrame préparé
    """
    print(f"\n📂 Chargement des données depuis: {csv_path}")
    
    try:
        # Essayer de lire le CSV (peut être compressé)
        # Détecter si c'est gzip en lisant les premiers bytes
        import gzip
        with open(csv_path, 'rb') as f:
            first_bytes = f.read(2)
            is_gzipped = first_bytes == b'\x1f\x8b'
        
        if is_gzipped or csv_path.endswith('.gz'):
            df = pd.read_csv(csv_path, compression='gzip', low_memory=False)
        else:
            df = pd.read_csv(csv_path, low_memory=False)
        
        print(f"✅ {len(df)} produits chargés")
        
        # Filtrer les produits avec ecoscore valide
        if 'ecoscore_grade' not in df.columns:
            print("⚠️  Colonne 'ecoscore_grade' non trouvée")
            return pd.DataFrame()
        
        df_valid = df[
            (df['ecoscore_grade'].notna()) &
            (df['ecoscore_grade'].isin(['a', 'b', 'c', 'd', 'e', 'A', 'B', 'C', 'D', 'E']))
        ].copy()
        
        # Normaliser les grades en minuscules
        df_valid['ecoscore_grade'] = df_valid['ecoscore_grade'].str.lower()
        
        print(f"📊 Produits avec ecoscore valide: {len(df_valid)}")
        print(f"   Distribution:")
        for grade in ['a', 'b', 'c', 'd', 'e']:
            count = len(df_valid[df_valid['ecoscore_grade'] == grade])
            if count > 0:
                print(f"     - {grade.upper()}: {count} ({count/len(df_valid)*100:.1f}%)")
        
        # Échantillonner équitablement
        if len(df_valid) > max_samples:
            # Stratified sampling
            samples_per_class = max_samples // 5
            df_sampled = pd.DataFrame()
            
            for grade in ['a', 'b', 'c', 'd', 'e']:
                df_class = df_valid[df_valid['ecoscore_grade'] == grade]
                if len(df_class) >= min_samples_per_class:
                    n = min(samples_per_class, len(df_class))
                    df_sampled = pd.concat([df_sampled, df_class.sample(n=n, random_state=42)])
            
            print(f"📊 Échantillonnage: {len(df_sampled)} produits sélectionnés")
            return df_sampled
        
        return df_valid
    
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def extract_nlp_features(product: Dict[str, Any]) -> Dict[str, Any]:
    """Extrait les features NLP depuis un produit"""
    labels_str = str(product.get('labels', '')).lower()
    packaging_str = str(product.get('packaging', '')).lower()
    origins_str = str(product.get('origins', '')).lower()
    ingredients_str = str(product.get('ingredients_text', '')).lower()
    allergens_str = str(product.get('allergens', '')).lower()
    
    # Extraire les ingrédients
    ingredients = []
    if ingredients_str and ingredients_str != 'nan':
        # Split par virgule ou autre séparateur
        parts = re.split(r'[,;]', ingredients_str)
        ingredients = [p.strip() for p in parts if len(p.strip()) > 2][:20]
    
    # Extraire les allergènes
    allergens = []
    if allergens_str and allergens_str != 'nan':
        parts = re.split(r'[,;]', allergens_str)
        allergens = [p.strip() for p in parts if len(p.strip()) > 2][:10]
    
    # Détecter les labels
    has_bio = any(label in labels_str for label in ['bio', 'organic', 'ab', 'ecocert', 'agriculture biologique'])
    has_fair_trade = any(label in labels_str for label in ['fair', 'équitable', 'commerce équitable', 'fairtrade'])
    
    # Détecter le packaging
    packaging_type = None
    if 'plastique' in packaging_str or 'plastic' in packaging_str or 'polyéthylène' in packaging_str:
        packaging_type = 'plastique'
    elif 'verre' in packaging_str or 'glass' in packaging_str:
        packaging_type = 'verre'
    elif 'papier' in packaging_str or 'carton' in packaging_str or 'paper' in packaging_str or 'cardboard' in packaging_str:
        packaging_type = 'papier'
    elif 'metal' in packaging_str or 'aluminium' in packaging_str or 'aluminum' in packaging_str or 'fer' in packaging_str:
        packaging_type = 'metal'
    
    packaging_recyclable = any(word in packaging_str for word in ['recyclable', 'recyclé', 'recyclable', 'recycled'])
    
    # Détecter l'origine
    origin = None
    if 'france' in origins_str or 'french' in origins_str or 'fr' in origins_str:
        origin = 'france'
    elif 'europe' in origins_str or 'european' in origins_str or 'eu' in origins_str:
        origin = 'europe'
    
    # Détecter les ingrédients problématiques
    has_palm_oil = 'huile de palme' in ingredients_str or 'palm oil' in ingredients_str or 'palme' in ingredients_str
    has_high_sugar = any(word in ingredients_str for word in ['sucre', 'sugar', 'sirop', 'syrup', 'glucose', 'fructose'])
    has_additives = bool(re.search(r'\be\d{3,4}\b', ingredients_str, re.IGNORECASE))
    
    # Extraire les labels
    labels = []
    if has_bio:
        labels.append('bio')
    if has_fair_trade:
        labels.append('fair_trade')
    
    return {
        'ingredients': ingredients,
        'allergens': allergens,
        'labels': labels,
        'packaging_type': packaging_type,
        'packaging_recyclable': packaging_recyclable,
        'origin': origin,
        'has_bio_label': has_bio,
        'has_fair_trade': has_fair_trade,
        'has_palm_oil': has_palm_oil,
        'has_high_sugar': has_high_sugar,
        'has_additives': has_additives
    }


def estimate_lca_impacts(product: Dict[str, Any], nlp_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Estime les impacts LCA depuis les données du produit
    Utilise des heuristiques basées sur les caractéristiques du produit
    """
    # Base d'impacts (moyennes par défaut pour produits alimentaires)
    co2_base = 2.5  # kg CO2
    water_base = 800.0  # litres
    energy_base = 10.0  # MJ
    
    # Ajustements selon les labels
    if nlp_data.get('has_bio_label'):
        co2_base *= 0.85  # -15% pour bio
        water_base *= 0.90
    
    if nlp_data.get('has_palm_oil'):
        co2_base *= 1.4  # +40% pour huile de palme
        water_base *= 1.3
    
    if nlp_data.get('has_high_sugar'):
        co2_base *= 1.1  # +10% pour sucre élevé
        water_base *= 1.2
    
    # Ajustements selon le packaging
    packaging_type = nlp_data.get('packaging_type')
    if packaging_type == 'plastique':
        co2_base += 0.6
        energy_base += 2.0
    elif packaging_type == 'verre':
        co2_base += 1.2
        energy_base += 3.0
    elif packaging_type == 'papier':
        co2_base += 0.3
        energy_base += 1.0
    elif packaging_type == 'metal':
        co2_base += 0.8
        energy_base += 2.5
    
    # Ajustements selon l'origine
    if nlp_data.get('origin') == 'france':
        co2_base *= 0.95  # -5% pour local
    elif nlp_data.get('origin') == 'europe':
        co2_base *= 0.98  # -2% pour européen
    
    # Variation réaliste (ajouter un peu de bruit)
    np.random.seed(hash(str(product.get('code', ''))) % 2**32)
    co2 = co2_base * np.random.uniform(0.85, 1.15)
    water = water_base * np.random.uniform(0.75, 1.25)
    energy = energy_base * np.random.uniform(0.85, 1.15)
    
    return {
        'co2_kg': float(max(0.1, co2)),
        'water_liters': float(max(10, water)),
        'energy_mj': float(max(1, energy)),
        'acidification': float(co2 * 0.002),
        'eutrophisation': float(water * 0.0001)
    }

