"""
Script principal de preprocessing
Orchestre toutes les étapes de préparation des données pour le ML
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from tokenizer import tokenize_ingredients
from auto_annotator import create_ner_annotations
from train_test_splitter import split_annotations


def main():
    """Exécute le pipeline de preprocessing complet"""
    log.info("=" * 60)
    log.info("⚙️  DÉMARRAGE DU PREPROCESSING")
    log.info("=" * 60)
    
    # Étape 1: Tokenisation
    log.info("\n📝 Étape 1/3: Tokenisation")
    tokenize_ingredients(
        "datasets/cleaned/products_cleaned.csv",
        "datasets/preprocessed/products_tokenized.csv"
    )
    
    # Étape 2: Auto-annotation NER
    log.info("\n🏷️  Étape 2/3: Auto-annotation NER")
    create_ner_annotations(
        "datasets/preprocessed/products_tokenized.csv",
        "datasets/preprocessed/ner_annotations.jsonl",
        sample_size=1000
    )
    
    # Étape 3: Séparation train/val/test
    log.info("\n✂️  Étape 3/3: Séparation train/val/test")
    split_annotations(
        "datasets/preprocessed/ner_annotations.jsonl",
        "datasets/preprocessed/splits",
        test_size=0.15,
        val_size=0.15,
        random_seed=42
    )
    
    log.info("\n" + "=" * 60)
    log.info("✅ PREPROCESSING TERMINÉ AVEC SUCCÈS")
    log.info("=" * 60)
    log.info("\n📁 Fichiers générés:")
    log.info("   - datasets/preprocessed/products_tokenized.csv")
    log.info("   - datasets/preprocessed/ner_annotations.jsonl")
    log.info("   - datasets/preprocessed/splits/train.jsonl")
    log.info("   - datasets/preprocessed/splits/validation.jsonl")
    log.info("   - datasets/preprocessed/splits/test.jsonl")
    log.info("\n🚀 Prêt pour l'entraînement du modèle NER !")


if __name__ == "__main__":
    main()

