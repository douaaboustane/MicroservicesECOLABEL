"""
Script principal d'exploration des données
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from generate_statistics import generate_statistics
from generate_visualizations import create_visualizations


def main():
    """Exécute le pipeline d'exploration complet"""
    log.info("=" * 60)
    log.info("📊 DÉMARRAGE DE L'EXPLORATION DES DONNÉES")
    log.info("=" * 60)
    
    input_file = "datasets/cleaned/products_cleaned.csv"
    
    # Étape 1: Statistiques
    log.info("\n📈 Étape 1/2: Génération des statistiques")
    generate_statistics(input_file, "outputs/statistics")
    
    # Étape 2: Visualisations
    log.info("\n📊 Étape 2/2: Génération des visualisations")
    create_visualizations(input_file, "outputs/visualizations")
    
    log.info("\n" + "=" * 60)
    log.info("✅ EXPLORATION TERMINÉE AVEC SUCCÈS")
    log.info("=" * 60)
    log.info("\n📁 Résultats:")
    log.info("   - Statistiques: outputs/statistics/statistics.json")
    log.info("   - Visualisations: outputs/visualizations/*.png")
    log.info("\n💡 Conseil: Ouvrez le notebook Jupyter pour une exploration interactive:")
    log.info("   jupyter lab 3_exploration/notebooks/")


if __name__ == "__main__":
    main()

