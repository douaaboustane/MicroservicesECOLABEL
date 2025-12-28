"""
Normalisation des données produits
"""
import pandas as pd
import sys
import re
from pathlib import Path
import ftfy

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import load_dataframe, save_dataframe


def normalize_text(text: str) -> str:
    """Normalise un texte"""
    if pd.isna(text):
        return ""
    
    text = str(text)
    # Correction encodage UTF-8
    text = ftfy.fix_text(text)
    # Suppression espaces multiples
    text = re.sub(r'\s+', ' ', text)
    # Trim
    text = text.strip()
    # Lowercase
    text = text.lower()
    
    return text


def normalize_grade(grade: str) -> str:
    """Normalise les notes (nutriscore, ecoscore)"""
    if pd.isna(grade) or grade == '' or grade == 'unknown':
        return 'unknown'
    
    grade = str(grade).strip().lower()
    # Standardiser les valeurs
    if grade in ['not-applicable', 'not applicable', 'n/a']:
        return 'not-applicable'
    
    return grade


def normalize_products(input_file: str, output_file: str):
    """Normalise les données produits"""
    log.info(f"Normalisation: {input_file}")
    
    df = load_dataframe(input_file)
    log.info(f"Chargé: {len(df)} produits")
    
    # Normalisation texte
    text_columns = ['product_name', 'ingredients_text', 'categories', 'labels', 
                    'packaging', 'origins', 'allergens']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(normalize_text)
    
    # Normalisation grades
    if 'nutriscore_grade' in df.columns:
        df['nutriscore_grade'] = df['nutriscore_grade'].apply(normalize_grade)
    if 'ecoscore_grade' in df.columns:
        df['ecoscore_grade'] = df['ecoscore_grade'].apply(normalize_grade)
    
    log.info(f"✓ Textes normalisés")
    
    save_dataframe(df, output_file)
    log.info(f"Sauvegardé: {output_file}")


def main():
    normalize_products(
        "datasets/raw/openfoodfacts_5k.csv",
        "datasets/cleaned/products_normalized.csv"
    )
    log.info("✅ Normalisation terminée")


if __name__ == "__main__":
    main()

