"""
Génération de visualisations
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import load_dataframe, ensure_dir


def create_visualizations(input_file: str, output_dir: str = "outputs/visualizations"):
    """Crée des visualisations des données"""
    log.info(f"Génération visualisations: {input_file}")
    
    ensure_dir(output_dir)
    df = load_dataframe(input_file)
    log.info(f"Chargé: {len(df)} produits")
    
    # Configuration matplotlib
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    
    # 1. Distribution Nutri-Score
    if 'nutriscore_grade' in df.columns:
        plt.figure(figsize=(10, 6))
        nutri_counts = df['nutriscore_grade'].value_counts()
        colors = ['#038141', '#85BB2F', '#FECB02', '#EE8100', '#E63E11', '#CCCCCC', '#999999']
        nutri_counts.plot(kind='bar', color=colors[:len(nutri_counts)])
        plt.title('Distribution Nutri-Score', fontsize=16, fontweight='bold')
        plt.xlabel('Nutri-Score')
        plt.ylabel('Nombre de produits')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/nutriscore_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        log.info("  ✓ nutriscore_distribution.png")
    
    # 2. Distribution Eco-Score
    if 'ecoscore_grade' in df.columns:
        plt.figure(figsize=(10, 6))
        eco_counts = df['ecoscore_grade'].value_counts()
        colors_eco = ['#008D36', '#51B84D', '#8FC459', '#FFCA03', '#FF6F00', '#E51F00', '#666666', '#999999']
        eco_counts.plot(kind='bar', color=colors_eco[:len(eco_counts)])
        plt.title('Distribution Eco-Score', fontsize=16, fontweight='bold')
        plt.xlabel('Eco-Score')
        plt.ylabel('Nombre de produits')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/ecoscore_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        log.info("  ✓ ecoscore_distribution.png")
    
    # 3. Longueur des ingrédients
    if 'ingredients_text' in df.columns:
        plt.figure(figsize=(12, 6))
        lengths = df['ingredients_text'].str.len()
        plt.hist(lengths[lengths < lengths.quantile(0.95)], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
        plt.title('Distribution de la longueur des listes d\'ingrédients', fontsize=14, fontweight='bold')
        plt.xlabel('Nombre de caractères')
        plt.ylabel('Nombre de produits')
        plt.axvline(lengths.median(), color='red', linestyle='--', label=f'Médiane: {lengths.median():.0f}')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{output_dir}/ingredients_length_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        log.info("  ✓ ingredients_length_distribution.png")
    
    # 4. Matrice de valeurs manquantes
    plt.figure(figsize=(12, 8))
    missing = df.isnull().sum() / len(df) * 100
    missing = missing[missing > 0].sort_values(ascending=True)
    if len(missing) > 0:
        missing.plot(kind='barh', color='coral')
        plt.title('Pourcentage de valeurs manquantes par colonne', fontsize=14, fontweight='bold')
        plt.xlabel('% manquant')
        plt.ylabel('Colonnes')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/missing_values.png", dpi=300, bbox_inches='tight')
        plt.close()
        log.info("  ✓ missing_values.png")
    
    # 5. Nutri-Score vs Eco-Score (heatmap)
    if 'nutriscore_grade' in df.columns and 'ecoscore_grade' in df.columns:
        plt.figure(figsize=(12, 8))
        # Filtrer les valeurs 'unknown' et 'not-applicable'
        df_filtered = df[(df['nutriscore_grade'].isin(['a', 'b', 'c', 'd', 'e'])) & 
                         (df['ecoscore_grade'].isin(['a', 'a-plus', 'b', 'c', 'd', 'e', 'f']))]
        
        if len(df_filtered) > 100:
            crosstab = pd.crosstab(df_filtered['nutriscore_grade'], df_filtered['ecoscore_grade'])
            sns.heatmap(crosstab, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Nombre de produits'})
            plt.title('Nutri-Score vs Eco-Score', fontsize=14, fontweight='bold')
            plt.xlabel('Eco-Score')
            plt.ylabel('Nutri-Score')
            plt.tight_layout()
            plt.savefig(f"{output_dir}/nutri_vs_eco_heatmap.png", dpi=300, bbox_inches='tight')
            plt.close()
            log.info("  ✓ nutri_vs_eco_heatmap.png")
    
    # 6. Top 15 catégories
    if 'categories' in df.columns:
        # Extraire toutes les catégories (split par virgule)
        all_categories = []
        for cats in df['categories']:
            if cats and cats != '':
                all_categories.extend([c.strip() for c in str(cats).split(',')])
        
        if len(all_categories) > 0:
            plt.figure(figsize=(12, 8))
            cat_series = pd.Series(all_categories)
            top_cats = cat_series.value_counts().head(15)
            top_cats.plot(kind='barh', color='teal')
            plt.title('Top 15 Catégories de produits', fontsize=14, fontweight='bold')
            plt.xlabel('Nombre de produits')
            plt.ylabel('Catégorie')
            plt.tight_layout()
            plt.savefig(f"{output_dir}/top_categories.png", dpi=300, bbox_inches='tight')
            plt.close()
            log.info("  ✓ top_categories.png")
    
    log.info(f"\n✓ Visualisations sauvegardées dans: {output_dir}/")


def main():
    create_visualizations(
        "datasets/cleaned/products_cleaned.csv",
        "outputs/visualizations"
    )
    log.info("✅ Génération des visualisations terminée")


if __name__ == "__main__":
    main()

