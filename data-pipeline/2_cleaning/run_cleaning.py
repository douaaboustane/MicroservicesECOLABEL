"""
Script principal de nettoyage
Orchestre toutes les étapes de nettoyage des données
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from normalizer import normalize_products
from deduplicator import deduplicate_products
from missing_handler import clean_missing_values


def main():
    """Exécute le pipeline de nettoyage complet"""
    log.info("=" * 60)
    log.info("🧹 DÉMARRAGE DU NETTOYAGE DES DONNÉES")
    log.info("=" * 60)
    
    # Étape 1: Normalisation
    log.info("\n📝 Étape 1/3: Normalisation")
    normalize_products(
        "datasets/raw/openfoodfacts_5k.csv",
        "datasets/cleaned/products_normalized.csv"
    )
    
    # Étape 2: Déduplication
    log.info("\n🔍 Étape 2/3: Déduplication")
    deduplicate_products(
        "datasets/cleaned/products_normalized.csv",
        "datasets/cleaned/products_deduplicated.csv"
    )
    
    # Étape 3: Gestion des valeurs manquantes
    log.info("\n✨ Étape 3/3: Valeurs manquantes")
    clean_missing_values(
        "datasets/cleaned/products_deduplicated.csv",
        "datasets/cleaned/products_cleaned.csv"
    )
    
    log.info("\n" + "=" * 60)
    log.info("✅ NETTOYAGE TERMINÉ AVEC SUCCÈS")
    log.info("=" * 60)
    log.info(f"\n📁 Fichier final: datasets/cleaned/products_cleaned.csv")


if __name__ == "__main__":
    main()

