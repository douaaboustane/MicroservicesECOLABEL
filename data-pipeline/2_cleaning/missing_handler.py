"""
Gestion des valeurs manquantes
"""
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import load_dataframe, save_dataframe


def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop', threshold: float = 0.3) -> pd.DataFrame:
    """
    Gère les valeurs manquantes
    
    Args:
        df: DataFrame
        strategy: 'drop', 'fill', or 'flag'
        threshold: Seuil pour supprimer les colonnes (0.3 = 30% manquant)
    """
    log.info("Gestion des valeurs manquantes:")
    
    # Analyser les valeurs manquantes
    missing_pct = df.isnull().sum() / len(df)
    
    for col in df.columns:
        pct = missing_pct[col]
        if pct > 0:
            log.info(f"  {col}: {pct:.1%} manquant")
    
    if strategy == 'drop':
        # Supprimer les colonnes avec trop de valeurs manquantes
        cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
        if cols_to_drop:
            log.info(f"  Suppression colonnes (>{threshold:.0%}): {cols_to_drop}")
            df = df.drop(columns=cols_to_drop)
        
        # Supprimer les lignes avec des valeurs manquantes dans les colonnes critiques
        critical_cols = ['code', 'product_name', 'ingredients_text']
        before = len(df)
        df = df.dropna(subset=[c for c in critical_cols if c in df.columns])
        after = len(df)
        if before > after:
            log.info(f"  Lignes supprimées (colonnes critiques): {before - after}")
    
    elif strategy == 'fill':
        # Remplir les valeurs manquantes
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('')
            else:
                df[col] = df[col].fillna(0)
        log.info(f"  Valeurs remplies")
    
    elif strategy == 'flag':
        # Ajouter des colonnes de flag pour les valeurs manquantes
        for col in df.columns:
            if missing_pct[col] > 0:
                df[f'{col}_is_missing'] = df[col].isnull()
        log.info(f"  Flags ajoutés")
    
    log.info(f"✓ Gestion des valeurs manquantes terminée: {len(df)} produits")
    
    return df


def clean_missing_values(input_file: str, output_file: str):
    """Nettoie les valeurs manquantes"""
    log.info(f"Nettoyage valeurs manquantes: {input_file}")
    
    df = load_dataframe(input_file)
    log.info(f"Chargé: {len(df)} produits")
    
    # Stratégie: fill (ne pas supprimer les données)
    df = handle_missing_values(df, strategy='fill')
    
    save_dataframe(df, output_file)
    log.info(f"Sauvegardé: {output_file}")


def main():
    clean_missing_values(
        "datasets/cleaned/products_deduplicated.csv",
        "datasets/cleaned/products_cleaned.csv"
    )
    log.info("✅ Nettoyage des valeurs manquantes terminé")


if __name__ == "__main__":
    main()

