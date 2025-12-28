#!/usr/bin/env python3
"""
Script de test interactif pour le modèle NER v3.0
=================================================
Permet de tester le modèle avec vos propres textes.

Usage:
    python test_mon_texte.py
    
Ou directement avec un texte:
    python test_mon_texte.py "CALCIUM 55 MAGNESIUM 19 SODIUM 24"
"""

import spacy
from pathlib import Path
import sys

def test_texte(nlp, text):
    """Teste un texte et affiche les résultats"""
    print("\n" + "=" * 80)
    print(f"📝 TEXTE: {text}")
    print("=" * 80)
    
    doc = nlp(text)
    entities = [(ent.text, ent.label_, ent.start_char, ent.end_char) for ent in doc.ents]
    
    if entities:
        print(f"\n✅ Détecté {len(entities)} entité(s):\n")
        
        # Grouper par label
        by_label = {}
        for text_ent, label, start, end in entities:
            if label not in by_label:
                by_label[label] = []
            by_label[label].append((text_ent, start, end))
        
        # Afficher par catégorie
        for label in sorted(by_label.keys()):
            items = by_label[label]
            print(f"🏷️  {label}:")
            for text_ent, start, end in items:
                print(f"   • {text_ent:30s} (position {start}-{end})")
        
        print()
    else:
        print("\n❌ Aucune entité détectée\n")
    
    print("=" * 80 + "\n")


def main():
    print("\n" + "=" * 80)
    print(" " * 20 + "🧪 TEST MODÈLE NER v3.0 - MODE INTERACTIF")
    print("=" * 80)
    
    # Charger le modèle
    print("\n📦 Chargement du modèle NER v3.0...")
    model_path = Path("models/ner_ingredients_v3")
    
    if not model_path.exists():
        print(f"❌ Modèle introuvable: {model_path}")
        print("   Assurez-vous d'être dans le dossier 'data-pipeline'")
        sys.exit(1)
    
    nlp = spacy.load(model_path)
    print(f"✅ Modèle chargé: {model_path}")
    print(f"   Labels disponibles: {', '.join(nlp.get_pipe('ner').labels)}")
    
    # Si un argument est passé, tester directement
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        test_texte(nlp, text)
        return
    
    # Mode interactif
    print("\n" + "=" * 80)
    print("💡 MODE INTERACTIF")
    print("=" * 80)
    print("\nEntrez vos textes à tester (ou 'quit' pour quitter)")
    print("Exemples de textes à tester:")
    print("  • CALCIUM 55 MAGNESIUM 19 SODIUM 24")
    print("  • colorant E150d, conservateur E330")
    print("  • farine de blé, eau, sel, levure")
    print("  • Vitamine A, Vitamine B12, Vitamine C")
    print()
    
    while True:
        try:
            text = input("\n📝 Votre texte ➜ ").strip()
            
            if not text:
                continue
            
            if text.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Au revoir !\n")
                break
            
            test_texte(nlp, text)
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !\n")
            break
        except EOFError:
            print("\n\n👋 Au revoir !\n")
            break


if __name__ == "__main__":
    main()

