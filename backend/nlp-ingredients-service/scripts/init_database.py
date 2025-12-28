"""
Script d'initialisation de la base de données
Peuple les tables avec les données de référence
"""
import sys
from pathlib import Path
import pandas as pd

# Ajouter le chemin parent pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine, Base
from app.models import IngredientTaxonomy, LabelDetection
from app.services.taxonomy_loader import TaxonomyLoader


def init_taxonomy_table():
    """Initialise la table ingredient_taxonomy avec les données de la taxonomie"""
    print("📚 Initialisation de la table ingredient_taxonomy...")
    
    db = SessionLocal()
    try:
        # Charger la taxonomie
        taxonomy_loader = TaxonomyLoader()
        taxonomy_data = taxonomy_loader.load_all()
        
        if not taxonomy_data:
            print("⚠️  Aucune taxonomie chargée")
            return
        
        # Compter les insertions
        inserted = 0
        updated = 0
        
        for normalized_name, data in taxonomy_data.items():
            # Vérifier si l'ingrédient existe déjà
            existing = db.query(IngredientTaxonomy).filter_by(
                name_normalized=normalized_name
            ).first()
            
            if existing:
                # Mettre à jour
                existing.category = data.get('category')
                existing.agribalyse_code = data.get('agribalyse_code')
                existing.ecoinvent_code = data.get('ecoinvent_code')
                existing.synonyms = data.get('synonyms', [])
                existing.is_allergen = data.get('is_allergen', False)
                existing.allergen_category = data.get('allergen_category')
                updated += 1
            else:
                # Créer nouveau
                ingredient = IngredientTaxonomy(
                    name=data.get('name', normalized_name),
                    name_normalized=normalized_name,
                    category=data.get('category'),
                    agribalyse_code=data.get('agribalyse_code'),
                    ecoinvent_code=data.get('ecoinvent_code'),
                    synonyms=data.get('synonyms', []),
                    is_allergen=data.get('is_allergen', False),
                    allergen_category=data.get('allergen_category')
                )
                db.add(ingredient)
                inserted += 1
        
        db.commit()
        print(f"✅ Taxonomie initialisée: {inserted} nouveaux, {updated} mis à jour")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'initialisation: {e}")
        raise
    finally:
        db.close()


def create_tables():
    """Crée toutes les tables si elles n'existent pas"""
    print("🗄️  Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées")


def main():
    """Fonction principale"""
    print("=" * 80)
    print(" " * 25 + "🚀 INITIALISATION BASE DE DONNÉES")
    print("=" * 80)
    print()
    
    # 1. Créer les tables
    create_tables()
    print()
    
    # 2. Peupler la taxonomie
    init_taxonomy_table()
    print()
    
    print("=" * 80)
    print(" " * 25 + "✅ INITIALISATION TERMINÉE")
    print("=" * 80)


if __name__ == "__main__":
    main()

