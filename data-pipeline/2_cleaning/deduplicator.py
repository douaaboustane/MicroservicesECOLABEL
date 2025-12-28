"""
Déduplication des produits
"""
import pandas as pd
import sys
from pathlib import Path
from fuzzywuzzy import fuzz

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import load_dataframe, save_dataframe


def deduplicate_by_code(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les doublons basés sur le code produit"""
    before = len(df)
    df = df.drop_duplicates(subset=['code'], keep='first')
    after = len(df)
    log.info(f"  Doublons par code: {before - after} supprimés")
    return df


def deduplicate_by_name(df: pd.DataFrame, threshold: float = 0.85) -> pd.DataFrame:
    """Détecte les doublons basés sur la similarité du nom"""
    # Pour 5000 produits, on peut faire une comparaison directe
    # Pour de plus gros volumes, utiliser des méthodes plus efficaces (blocking)
    
    duplicates = []
    products = df.to_dict('records')
    
    for i in range(len(products)):
        if i in duplicates:
            continue
        for j in range(i + 1, len(products)):
            if j in duplicates:
                continue
            
            name1 = products[i].get('product_name', '')
            name2 = products[j].get('product_name', '')
            
            if len(name1) > 0 and len(name2) > 0:
                similarity = fuzz.ratio(name1, name2) / 100.0
                if similarity >= threshold:
                    duplicates.append(j)
    
    before = len(df)
    df = df.drop(df.index[duplicates])
    after = len(df)
    log.info(f"  Doublons par nom (seuil {threshold}): {before - after} supprimés")
    
    return df


def deduplicate_products(input_file: str, output_file: str, threshold: float = 0.85):
    """Déduplique les produits"""
    log.info(f"Déduplication: {input_file}")
    
    df = load_dataframe(input_file)
    log.info(f"Chargé: {len(df)} produits")
    
    # Déduplication par code exact
    df = deduplicate_by_code(df)
    
    # Déduplication par similarité de nom (optionnel - peut être lent)
    # df = deduplicate_by_name(df, threshold)
    
    log.info(f"✓ Déduplication terminée: {len(df)} produits restants")
    
    save_dataframe(df, output_file)
    log.info(f"Sauvegardé: {output_file}")


def main():
    deduplicate_products(
        "datasets/cleaned/products_normalized.csv",
        "datasets/cleaned/products_deduplicated.csv"
    )
    log.info("✅ Déduplication terminée")


if __name__ == "__main__":
    main()

