"""
Training Script NER v3.0 - VERSION FINALE
==========================================
Entraîne un modèle spaCy NER pour détecter :
- ✅ INGREDIENT (classiques + E-numbers + minéraux + vitamines)
- ✅ QUANTITY (%, g, mg, ml, etc.)
- ✅ ALLERGEN (14 catégories EU)

Auteur: EcoLabel-MS Data Pipeline
Date: 2025
"""

import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import json
import random
from pathlib import Path
import sys
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import ensure_dir


def load_annotations(jsonl_file: str):
    """Charge les annotations depuis un fichier JSONL"""
    training_data = []
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            training_data.append((
                data['text'],
                {'entities': data['entities']}
            ))
    
    log.info(f"✅ Chargé: {len(training_data)} exemples depuis {jsonl_file}")
    return training_data


def split_data(data, train_ratio=0.7, val_ratio=0.15):
    """
    Divise les données en train/validation/test.
    
    Args:
        data: Liste de tuples (text, annotations)
        train_ratio: Ratio d'entraînement (0.7 = 70%)
        val_ratio: Ratio de validation (0.15 = 15%)
    
    Returns:
        train_data, val_data, test_data
    """
    random.shuffle(data)
    
    n = len(data)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    
    train_data = data[:train_end]
    val_data = data[train_end:val_end]
    test_data = data[val_end:]
    
    log.info(f"📊 Split des données:")
    log.info(f"   • Train:      {len(train_data):4d} ({len(train_data)/n*100:.1f}%)")
    log.info(f"   • Validation: {len(val_data):4d} ({len(val_data)/n*100:.1f}%)")
    log.info(f"   • Test:       {len(test_data):4d} ({len(test_data)/n*100:.1f}%)")
    
    return train_data, val_data, test_data


def save_split_data(train_data, val_data, test_data, output_dir):
    """Sauvegarde les splits dans des fichiers JSONL séparés"""
    ensure_dir(output_dir)
    
    splits = {
        'train': train_data,
        'validation': val_data,
        'test': test_data
    }
    
    for split_name, data in splits.items():
        output_file = Path(output_dir) / f"{split_name}.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for text, annotations in data:
                item = {
                    'text': text,
                    'entities': annotations['entities']
                }
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        log.info(f"✅ Sauvegardé: {output_file} ({len(data)} exemples)")


def evaluate_model(nlp, examples):
    """Évalue le modèle sur un ensemble d'exemples"""
    if not examples:
        return {}
    
    scorer = nlp.evaluate(examples)
    return scorer


def train_ner_model(
    train_data,
    val_data,
    output_dir,
    n_iter=50,
    batch_size=16,
    drop=0.2
):
    """
    Entraîne un modèle NER spaCy.
    
    Args:
        train_data: Données d'entraînement
        val_data: Données de validation
        output_dir: Répertoire de sortie du modèle
        n_iter: Nombre d'itérations
        batch_size: Taille des batches
        drop: Taux de dropout
    
    Returns:
        nlp: Modèle entraîné
    """
    log.info("=" * 80)
    log.info("🚀 ENTRAÎNEMENT DU MODÈLE NER v3.0 FINAL")
    log.info("=" * 80)
    log.info(f"   • Itérations: {n_iter}")
    log.info(f"   • Batch size: {batch_size}")
    log.info(f"   • Dropout:    {drop}")
    log.info(f"   • Output:     {output_dir}")
    log.info("")
    
    # Charger le modèle de base français
    log.info("📦 Chargement du modèle de base 'fr_core_news_md'...")
    nlp = spacy.load("fr_core_news_md")
    
    # Créer le pipeline NER s'il n'existe pas
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")
    
    # Ajouter les labels
    log.info("🏷️  Ajout des labels NER...")
    labels = set()
    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            labels.add(ent[2])
    
    for label in labels:
        ner.add_label(label)
    
    log.info(f"✅ Labels: {sorted(labels)}")
    
    # Préparer les exemples d'entraînement
    log.info("\n📝 Préparation des exemples...")
    train_examples = []
    for text, annotations in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        train_examples.append(example)
    
    # Préparer les exemples de validation
    val_examples = []
    if val_data:
        for text, annotations in val_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            val_examples.append(example)
    
    log.info(f"✅ Train:      {len(train_examples)} exemples")
    log.info(f"✅ Validation: {len(val_examples)} exemples")
    
    # Désactiver les autres pipes pendant l'entraînement
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    # Entraînement
    log.info(f"\n🎯 DÉBUT DE L'ENTRAÎNEMENT ({n_iter} itérations)...")
    log.info("")
    
    start_time = datetime.now()
    best_f1 = 0.0
    best_iteration = 0
    
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.resume_training()
        
        for iteration in range(n_iter):
            random.shuffle(train_examples)
            losses = {}
            
            # Batch training
            batches = minibatch(train_examples, size=compounding(4.0, batch_size, 1.001))
            for batch in batches:
                nlp.update(
                    batch,
                    drop=drop,
                    sgd=optimizer,
                    losses=losses
                )
            
            # Évaluation sur validation tous les 5 itérations
            if (iteration + 1) % 5 == 0 or iteration == 0:
                if val_examples:
                    scores = evaluate_model(nlp, val_examples)
                    f1 = scores.get("ents_f", 0.0) * 100
                    precision = scores.get("ents_p", 0.0) * 100
                    recall = scores.get("ents_r", 0.0) * 100
                    
                    # Suivre le meilleur F1
                    if f1 > best_f1:
                        best_f1 = f1
                        best_iteration = iteration + 1
                    
                    log.info(
                        f"Iter {iteration + 1:3d} | "
                        f"Loss: {losses.get('ner', 0.0):8.2f} | "
                        f"P: {precision:5.2f}% | "
                        f"R: {recall:5.2f}% | "
                        f"F1: {f1:5.2f}% "
                        f"{'🔥' if f1 == best_f1 else ''}"
                    )
                else:
                    log.info(
                        f"Iter {iteration + 1:3d} | "
                        f"Loss: {losses.get('ner', 0.0):8.2f}"
                    )
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    log.info("")
    log.info("✅ ENTRAÎNEMENT TERMINÉ !")
    log.info(f"   • Durée:      {duration}")
    log.info(f"   • Meilleur F1: {best_f1:.2f}% (itération {best_iteration})")
    
    # Sauvegarder le modèle
    log.info(f"\n💾 Sauvegarde du modèle dans {output_dir}...")
    ensure_dir(output_dir)
    nlp.to_disk(output_dir)
    log.info("✅ Modèle sauvegardé !")
    
    return nlp


def test_model(nlp, test_data):
    """Teste le modèle sur l'ensemble de test"""
    log.info("\n" + "=" * 80)
    log.info("🧪 ÉVALUATION SUR L'ENSEMBLE DE TEST")
    log.info("=" * 80)
    
    # Préparer les exemples de test
    test_examples = []
    for text, annotations in test_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        test_examples.append(example)
    
    # Évaluer
    scores = evaluate_model(nlp, test_examples)
    
    # Afficher les résultats
    log.info(f"\n📊 RÉSULTATS GLOBAUX:")
    log.info(f"   • Précision: {scores.get('ents_p', 0.0) * 100:.2f}%")
    log.info(f"   • Rappel:    {scores.get('ents_r', 0.0) * 100:.2f}%")
    log.info(f"   • F1-Score:  {scores.get('ents_f', 0.0) * 100:.2f}%")
    
    # Résultats par entité
    if 'ents_per_type' in scores:
        log.info(f"\n📊 RÉSULTATS PAR TYPE D'ENTITÉ:")
        for ent_type, metrics in sorted(scores['ents_per_type'].items()):
            p = metrics.get('p', 0.0) * 100
            r = metrics.get('r', 0.0) * 100
            f = metrics.get('f', 0.0) * 100
            log.info(f"   • {ent_type:12s} → P: {p:5.2f}%  R: {r:5.2f}%  F1: {f:5.2f}%")
    
    log.info("=" * 80)
    
    return scores


def main():
    """Fonction principale"""
    # Configuration
    ANNOTATIONS_FILE = "datasets/preprocessed/ner_annotations_v3.jsonl"
    SPLITS_DIR = "datasets/preprocessed/splits_v3"
    MODEL_OUTPUT_DIR = "models/ner_ingredients_v3"
    
    N_ITER = 50
    BATCH_SIZE = 16
    DROPOUT = 0.2
    
    # 1. Charger les annotations
    log.info("=" * 80)
    log.info("📦 CHARGEMENT DES DONNÉES")
    log.info("=" * 80)
    all_data = load_annotations(ANNOTATIONS_FILE)
    
    # 2. Diviser en train/val/test
    train_data, val_data, test_data = split_data(all_data)
    
    # 3. Sauvegarder les splits
    save_split_data(train_data, val_data, test_data, SPLITS_DIR)
    
    # 4. Entraîner le modèle
    nlp = train_ner_model(
        train_data=train_data,
        val_data=val_data,
        output_dir=MODEL_OUTPUT_DIR,
        n_iter=N_ITER,
        batch_size=BATCH_SIZE,
        drop=DROPOUT
    )
    
    # 5. Tester sur l'ensemble de test
    test_scores = test_model(nlp, test_data)
    
    # 6. Résumé final
    log.info("\n" + "=" * 80)
    log.info("🎉 MODÈLE NER v3.0 FINAL ENTRAÎNÉ AVEC SUCCÈS !")
    log.info("=" * 80)
    log.info(f"📁 Modèle sauvegardé: {MODEL_OUTPUT_DIR}")
    log.info(f"🎯 F1-Score final:    {test_scores.get('ents_f', 0.0) * 100:.2f}%")
    log.info("")
    log.info("💡 PROCHAINES ÉTAPES:")
    log.info("   1. Copier le modèle dans backend/parser-service/app/models/")
    log.info("   2. Tester avec le Parser Service")
    log.info("   3. Intégrer dans le pipeline complet")
    log.info("=" * 80)


if __name__ == "__main__":
    random.seed(42)
    main()

