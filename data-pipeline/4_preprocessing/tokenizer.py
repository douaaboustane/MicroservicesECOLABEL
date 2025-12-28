"""
Tokenisation des textes d'ingrédients avec spaCy
"""
import pandas as pd
import spacy
import sys
from pathlib import Path
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import load_dataframe, save_dataframe, ensure_dir


def tokenize_ingredients(input_file: str, output_file: str):
    """Tokenise les textes d'ingrédients"""
    log.info(f"Tokenisation: {input_file}")
    
    # Charger le modèle spaCy français
    log.info("Chargement du modèle spaCy fr_core_news_md...")
    nlp = spacy.load("fr_core_news_md")
    
    # Charger les données
    df = load_dataframe(input_file)
    log.info(f"Chargé: {len(df)} produits")
    
    # Tokeniser les ingrédients
    tokenized_texts = []
    tokens_list = []
    pos_tags_list = []
    
    log.info("Tokenisation en cours...")
    for text in tqdm(df['ingredients_text'], desc="Tokenizing"):
        if text and len(text) > 0:
            doc = nlp(text)
            
            # Extraire tokens et POS tags
            tokens = [token.text for token in doc]
            pos_tags = [token.pos_ for token in doc]
            lemmas = [token.lemma_ for token in doc]
            
            tokenized_texts.append(" ".join(tokens))
            tokens_list.append(tokens)
            pos_tags_list.append(pos_tags)
        else:
            tokenized_texts.append("")
            tokens_list.append([])
            pos_tags_list.append([])
    
    # Ajouter au DataFrame
    df['ingredients_tokenized'] = tokenized_texts
    df['tokens_count'] = [len(t) for t in tokens_list]
    
    # Statistiques
    total_tokens = sum(df['tokens_count'])
    avg_tokens = df['tokens_count'].mean()
    
    log.info(f"✓ Tokenisation terminée")
    log.info(f"  Total tokens: {total_tokens:,}")
    log.info(f"  Moyenne tokens/produit: {avg_tokens:.1f}")
    log.info(f"  Max tokens: {df['tokens_count'].max()}")
    log.info(f"  Min tokens: {df['tokens_count'].min()}")
    
    # Sauvegarder
    ensure_dir(Path(output_file).parent)
    save_dataframe(df, output_file)
    log.info(f"Sauvegardé: {output_file}")
    
    return df


def main():
    tokenize_ingredients(
        "datasets/cleaned/products_cleaned.csv",
        "datasets/preprocessed/products_tokenized.csv"
    )
    log.info("✅ Tokenisation terminée")


if __name__ == "__main__":
    main()
