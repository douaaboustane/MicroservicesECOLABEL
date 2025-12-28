#!/usr/bin/env python3
"""
Script de test rapide pour l'intégration NER
Teste le NERExtractor sans lancer le serveur FastAPI
"""
import sys
from pathlib import Path

# Ajouter le dossier app au path
sys.path.insert(0, str(Path(__file__).parent))

from app.extractors.ner_extractor import NERExtractor


def test_ner_extractor():
    """Test du NERExtractor"""
    
    print("\n" + "=" * 70)
    print(" " * 20 + "🧪 TEST NER EXTRACTOR")
    print("=" * 70)
    
    # Initialiser l'extracteur
    print("\n1️⃣  Initialisation du NERExtractor...")
    ner = NERExtractor()
    
    # Vérifier les infos du modèle
    print("\n2️⃣  Informations du modèle:")
    model_info = ner.get_model_info()
    for key, value in model_info.items():
        print(f"   • {key}: {value}")
    
    if not model_info.get("loaded"):
        print("\n❌ ERREUR: Le modèle NER n'est pas chargé !")
        return False
    
    # Tests d'extraction
    print("\n3️⃣  Tests d'extraction:")
    
    test_cases = [
        "farine de blé 60%, sucre 30%, beurre 10%",
        "Ingrédients: eau, sel, farine, levure",
        "Chocolat noir 70%, lait entier, vanille naturelle",
        "Tomates (45%), huile d'olive extra vierge, basilic frais",
        "Pommes de terre, oignons, carottes, sel, poivre"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n   Test {i}:")
        print(f"   📝 Texte: '{test_text}'")
        
        # Extraction détaillée
        ingredients = ner.extract_ingredients(test_text)
        print(f"   🔍 Trouvé: {len(ingredients)} ingrédients")
        
        for ing in ingredients:
            qty_str = f" ({ing['quantity']})" if ing.get('quantity') else ""
            print(f"      • {ing['name']}{qty_str}")
        
        # Extraction formatée
        ingredients_text = ner.extract_ingredients_as_text(test_text)
        print(f"   📄 Formaté: {ingredients_text}")
    
    print("\n" + "=" * 70)
    print(" " * 25 + "✅ TESTS TERMINÉS")
    print("=" * 70 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        success = test_ner_extractor()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

