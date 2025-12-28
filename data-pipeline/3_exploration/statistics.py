"""
Génération de statistiques descriptives
"""
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import load_dataframe, ensure_dir


def generate_statistics(input_file: str, output_dir: str = "outputs/statistics"):
    """Génère des statistiques descriptives"""
    log.info(f"Génération statistiques: {input_file}")
    
    ensure_dir(output_dir)
    df = load_dataframe(input_file)
    log.info(f"Chargé: {len(df)} produits")
    
    stats = {}
    
    # 1. Statistiques générales
    stats['total_products'] = len(df)
    stats['total_columns'] = len(df.columns)
    stats['memory_usage_mb'] = df.memory_usage(deep=True).sum() / (1024 * 1024)
    
    # 2. Statistiques par colonne
    stats['columns_info'] = {}
    for col in df.columns:
        stats['columns_info'][col] = {
            'type': str(df[col].dtype),
            'missing': int(df[col].isnull().sum()),
            'missing_pct': float(df[col].isnull().sum() / len(df) * 100),
            'unique': int(df[col].nunique()),
            'unique_pct': float(df[col].nunique() / len(df) * 100)
        }
    
    # 3. Nutri-Score distribution
    if 'nutriscore_grade' in df.columns:
        nutri_dist = df['nutriscore_grade'].value_counts().to_dict()
        stats['nutriscore_distribution'] = nutri_dist
        log.info(f"  Nutri-Score: {len(nutri_dist)} catégories")
    
    # 4. Eco-Score distribution
    if 'ecoscore_grade' in df.columns:
        eco_dist = df['ecoscore_grade'].value_counts().to_dict()
        stats['ecoscore_distribution'] = eco_dist
        log.info(f"  Eco-Score: {len(eco_dist)} catégories")
    
    # 5. Statistiques sur les ingrédients
    if 'ingredients_text' in df.columns:
        df['ingredients_length'] = df['ingredients_text'].str.len()
        stats['ingredients_stats'] = {
            'mean_length': float(df['ingredients_length'].mean()),
            'median_length': float(df['ingredients_length'].median()),
            'max_length': int(df['ingredients_length'].max()),
            'min_length': int(df['ingredients_length'].min())
        }
        log.info(f"  Longueur moyenne ingrédients: {stats['ingredients_stats']['mean_length']:.1f}")
    
    # 6. Statistiques sur les catégories
    if 'categories' in df.columns:
        non_empty_categories = df[df['categories'] != '']['categories']
        if len(non_empty_categories) > 0:
            # Compter le nombre de catégories par produit
            df['num_categories'] = df['categories'].apply(lambda x: len(str(x).split(',')) if x else 0)
            stats['categories_stats'] = {
                'products_with_categories': int((df['categories'] != '').sum()),
                'avg_categories_per_product': float(df['num_categories'].mean()),
                'max_categories': int(df['num_categories'].max())
            }
            log.info(f"  Produits avec catégories: {stats['categories_stats']['products_with_categories']}")
    
    # 7. Top produits
    if 'product_name' in df.columns:
        top_products = df['product_name'].value_counts().head(10)
        stats['top_products'] = top_products.to_dict()
    
    # Affichage résumé
    log.info("\n" + "=" * 60)
    log.info("📊 STATISTIQUES DESCRIPTIVES")
    log.info("=" * 60)
    log.info(f"Total produits: {stats['total_products']}")
    log.info(f"Colonnes: {stats['total_columns']}")
    log.info(f"Mémoire: {stats['memory_usage_mb']:.2f} MB")
    
    if 'nutriscore_distribution' in stats:
        log.info(f"\nNutri-Score (top 3):")
        for grade, count in list(stats['nutriscore_distribution'].items())[:3]:
            log.info(f"  {grade.upper()}: {count} ({count/stats['total_products']*100:.1f}%)")
    
    if 'ecoscore_distribution' in stats:
        log.info(f"\nEco-Score (top 3):")
        for grade, count in list(stats['ecoscore_distribution'].items())[:3]:
            log.info(f"  {grade.upper()}: {count} ({count/stats['total_products']*100:.1f}%)")
    
    # Sauvegarder en JSON
    import json
    output_file = Path(output_dir) / "statistics.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    log.info(f"\n✓ Statistiques sauvegardées: {output_file}")
    
    return stats


def main():
    generate_statistics(
        "datasets/cleaned/products_cleaned.csv",
        "outputs/statistics"
    )
    log.info("✅ Génération des statistiques terminée")


if __name__ == "__main__":
    main()
