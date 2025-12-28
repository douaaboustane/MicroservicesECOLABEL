"""
Séparation des données en train/validation/test
"""
import pandas as pd
import json
import sys
from pathlib import Path
from sklearn.model_selection import train_test_split

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import ensure_dir


def split_annotations(input_file: str, output_dir: str, test_size: float = 0.15, val_size: float = 0.15, random_seed: int = 42):
    """
    Sépare les annotations en train/validation/test
    
    Args:
        input_file: Fichier JSONL d'annotations
        output_dir: Dossier de sortie
        test_size: Proportion du test set
        val_size: Proportion du validation set
        random_seed: Seed pour la reproductibilité
    """
    log.info(f"Séparation train/val/test: {input_file}")
    
    # Charger les annotations
    annotations = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            annotations.append(json.loads(line))
    
    log.info(f"Chargé: {len(annotations)} annotations")
    
    # Première séparation: train+val vs test
    train_val, test = train_test_split(
        annotations,
        test_size=test_size,
        random_state=random_seed
    )
    
    # Deuxième séparation: train vs val
    val_proportion = val_size / (1 - test_size)
    train, val = train_test_split(
        train_val,
        test_size=val_proportion,
        random_state=random_seed
    )
    
    log.info(f"✓ Séparation effectuée:")
    log.info(f"  Train: {len(train)} ({len(train)/len(annotations)*100:.1f}%)")
    log.info(f"  Validation: {len(val)} ({len(val)/len(annotations)*100:.1f}%)")
    log.info(f"  Test: {len(test)} ({len(test)/len(annotations)*100:.1f}%)")
    
    # Sauvegarder
    ensure_dir(output_dir)
    
    # Train
    train_file = Path(output_dir) / "train.jsonl"
    with open(train_file, 'w', encoding='utf-8') as f:
        for item in train:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    log.info(f"  Sauvegardé: {train_file}")
    
    # Validation
    val_file = Path(output_dir) / "validation.jsonl"
    with open(val_file, 'w', encoding='utf-8') as f:
        for item in val:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    log.info(f"  Sauvegardé: {val_file}")
    
    # Test
    test_file = Path(output_dir) / "test.jsonl"
    with open(test_file, 'w', encoding='utf-8') as f:
        for item in test:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    log.info(f"  Sauvegardé: {test_file}")
    
    return train, val, test


def main():
    split_annotations(
        "datasets/preprocessed/ner_annotations.jsonl",
        "datasets/preprocessed/splits",
        test_size=0.15,
        val_size=0.15,
        random_seed=42
    )
    log.info("✅ Séparation train/val/test terminée")


if __name__ == "__main__":
    main()

