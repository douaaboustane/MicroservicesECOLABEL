"""
Auto-Annotateur NER v3.0 - VERSION FINALE
==========================================
Détecte :
- ✅ Ingrédients classiques (150+ items FR + EN)
- ✅ Additifs E-numbers (E100-E1999)
- ✅ Minéraux (30+ items)
- ✅ Vitamines (A, B1-B12, C, D, E, K)
- ✅ Quantités (%, g, mg, ml, etc.)
- ✅ Allergènes (14 catégories)

Auteur: EcoLabel-MS Data Pipeline
Date: 2025
"""

import pandas as pd
import spacy
import sys
import json
import re
from pathlib import Path
from tqdm import tqdm
from typing import List, Dict, Any, Tuple

sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import load_dataframe, ensure_dir


class FinalNERAnnotator:
    """Annotateur NER final avec détection complète"""
    
    def __init__(self):
        log.info("🚀 Initialisation de l'Auto-Annotateur NER v3.0 FINAL")
        
        # Charger le modèle français de spaCy
        try:
            self.nlp = spacy.load("fr_core_news_md")
        except OSError:
            log.error("Modèle spaCy 'fr_core_news_md' non trouvé. Installation...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "fr_core_news_md"])
            self.nlp = spacy.load("fr_core_news_md")
        
        # ===================================================================
        # 1. INGRÉDIENTS CLASSIQUES (FR + EN)
        # ===================================================================
        self.common_ingredients_fr = [
            # Bases
            "farine", "blé", "sucre", "sel", "beurre", "lait", "eau", "huile", "œuf",
            "chocolat", "vanille", "levure", "cacao", "tomate", "oignon", "carotte",
            "pomme de terre", "ail", "poivre", "basilic", "persil", "fromage", "viande",
            
            # Protéines
            "poulet", "bœuf", "porc", "agneau", "veau", "dinde", "canard",
            "poisson", "saumon", "thon", "cabillaud", "crevette", "moule", "crabe",
            
            # Céréales & légumineuses
            "riz", "maïs", "avoine", "seigle", "orge", "quinoa", "boulgour", "semoule",
            "sarrasin", "épeautre", "millet", "lentille", "pois chiche", "haricot",
            "pois", "fève", "soja",
            
            # Fruits
            "pomme", "poire", "orange", "citron", "banane", "fraise", "framboise",
            "myrtille", "raisin", "pêche", "abricot", "cerise", "prune", "mangue",
            "ananas", "kiwi", "melon", "pastèque",
            
            # Légumes
            "épinard", "brocoli", "chou", "concombre", "poivron", "courgette",
            "aubergine", "champignon", "salade", "laitue", "radis", "betterave",
            "navet", "céleri", "fenouil", "asperge",
            
            # Fruits secs & oléagineux
            "amande", "noix", "noisette", "cacahuète", "pistache", "noix de cajou",
            "noix de coco", "raisin sec", "datte", "figue",
            
            # Produits laitiers
            "crème", "yaourt", "yogourt", "fromage blanc", "mascarpone", "ricotta",
            "parmesan", "mozzarella", "cheddar", "emmental", "gruyère",
            
            # Matières grasses
            "margarine", "saindoux", "graisse", "shortening",
            
            # Condiments & épices
            "moutarde", "mayonnaise", "ketchup", "vinaigre", "sauce soja",
            "curry", "cumin", "curcuma", "paprika", "gingembre", "cannelle",
            "muscade", "clou de girofle", "cardamome", "safran", "piment",
            "thym", "romarin", "origan", "laurier", "menthe", "coriandre",
            
            # Édulcorants
            "miel", "sirop", "glucose", "fructose", "lactose", "maltose",
            "dextrose", "saccharose", "aspartame", "stévia",
            
            # Agents de texture
            "gélatine", "pectine", "amidon", "fécule", "agar-agar", "gomme",
            "carraghénane", "xanthane", "guar",
            
            # Arômes
            "arôme", "extrait", "essence", "concentré",
            
            # Conservateurs (mots clés)
            "conservateur", "antioxydant", "acidifiant", "émulsifiant",
            "stabilisant", "épaississant", "colorant", "agent de texture",
        ]
        
        # Ingrédients anglais (Open Food Facts est multilingue)
        self.common_ingredients_en = [
            "flour", "wheat", "sugar", "salt", "butter", "milk", "water", "oil", "egg",
            "chocolate", "vanilla", "yeast", "cocoa", "tomato", "onion", "carrot",
            "potato", "garlic", "pepper", "basil", "parsley", "cheese", "meat",
            "rice", "corn", "oat", "quinoa", "almond", "nut", "peanut", "soy",
            "lemon", "apple", "orange", "strawberry", "cream", "yogurt", "honey",
        ]
        
        self.all_ingredients = self.common_ingredients_fr + self.common_ingredients_en
        
        # ===================================================================
        # 2. MINÉRAUX (30+ éléments)
        # ===================================================================
        self.minerals = [
            # Macroéléments
            "calcium", "magnesium", "magnésium", "potassium", "sodium",
            "phosphorus", "phosphore", "chloride", "chlorure", "sulphur", "soufre",
            
            # Oligoéléments
            "iron", "fer", "zinc", "copper", "cuivre", "manganese", "manganèse",
            "selenium", "sélénium", "iodine", "iode", "fluoride", "fluorure",
            "chromium", "chrome", "molybdenum", "molybdène", "cobalt",
            
            # Sels/composés minéraux
            "bicarbonate", "carbonate", "sulfate", "nitrate", "nitrite",
            "phosphate", "oxide", "oxyde", "hydroxide", "hydroxyde",
            
            # Éléments traces
            "aluminium", "aluminum", "silica", "silice", "boron", "bore",
            "vanadium", "nickel", "tin", "étain", "lithium",
        ]
        
        # ===================================================================
        # 3. VITAMINES (A, B1-B12, C, D, E, K)
        # ===================================================================
        self.vitamins = [
            # Vitamine générique
            "vitamine", "vitamin",
            
            # Vitamine A
            "rétinol", "retinol", "bêta-carotène", "beta-carotene", "caroténoïde",
            
            # Vitamines B
            "thiamine", "thiamin",  # B1
            "riboflavine", "riboflavin",  # B2
            "niacine", "niacin", "nicotinamide",  # B3
            "acide pantothénique", "pantothenic acid", "pantothénate",  # B5
            "pyridoxine", "pyridoxin",  # B6
            "biotine", "biotin",  # B7/B8
            "acide folique", "folic acid", "folate", "folacine",  # B9
            "cobalamine", "cobalamin", "cyanocobalamine",  # B12
            
            # Vitamine C
            "acide ascorbique", "ascorbic acid", "ascorbate",
            
            # Vitamine D
            "cholécalciférol", "cholecalciferol", "ergocalciférol",
            
            # Vitamine E
            "tocophérol", "tocopherol", "tocotriénol",
            
            # Vitamine K
            "phylloquinone", "ménaquinone", "menaquinone",
        ]
        
        # ===================================================================
        # 4. ALLERGÈNES (14 catégories EU)
        # ===================================================================
        self.allergens = {
            "gluten": ["gluten", "blé", "wheat", "seigle", "rye", "orge", "barley", 
                      "avoine", "oat", "épeautre", "spelt", "kamut"],
            "crustacés": ["crustacé", "crustacean", "crevette", "shrimp", "crabe", 
                         "crab", "homard", "lobster", "langouste"],
            "œufs": ["œuf", "egg", "oeuf", "albumine", "albumin"],
            "poisson": ["poisson", "fish", "anchois", "anchovy"],
            "arachides": ["arachide", "peanut", "cacahuète"],
            "soja": ["soja", "soy", "soya"],
            "lait": ["lait", "milk", "lactose", "caséine", "casein", "whey", "lactosérum"],
            "fruits_à_coque": ["amande", "almond", "noisette", "hazelnut", "noix", "walnut",
                              "noix de cajou", "cashew", "noix de pécan", "pecan",
                              "pistache", "pistachio", "noix de macadamia"],
            "céleri": ["céleri", "celery"],
            "moutarde": ["moutarde", "mustard"],
            "sésame": ["sésame", "sesame"],
            "sulfites": ["sulfite", "sulphite", "dioxyde de soufre"],
            "lupin": ["lupin", "lupine"],
            "mollusques": ["mollusque", "mollusk", "moule", "mussel", "huître", 
                          "oyster", "coquille saint-jacques", "scallop"],
        }
        
        # Liste plate de tous les allergènes
        self.all_allergens = []
        for allergen_list in self.allergens.values():
            self.all_allergens.extend(allergen_list)
        
        log.info(f"✅ Chargé: {len(self.all_ingredients)} ingrédients")
        log.info(f"✅ Chargé: {len(self.minerals)} minéraux")
        log.info(f"✅ Chargé: {len(self.vitamins)} vitamines")
        log.info(f"✅ Chargé: {len(self.all_allergens)} allergènes")
    
    def annotate(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Annotate un texte avec les entités NER.
        
        Returns:
            Liste de tuples (start, end, label)
        """
        if not text or not isinstance(text, str):
            return []
        
        text = str(text).strip()
        if len(text) < 2:
            return []
        
        entities = []
        
        # ===================================================================
        # 1. DÉTECTER LES E-NUMBERS (E100 à E1999)
        # ===================================================================
        # Pattern: E suivi de 3 ou 4 chiffres, avec optionnellement une lettre
        # Ex: E123, E150d, E1505
        e_number_pattern = r'\bE\d{3,4}[a-z]?\b'
        for match in re.finditer(e_number_pattern, text, re.IGNORECASE):
            entities.append((match.start(), match.end(), 'INGREDIENT'))
        
        # ===================================================================
        # 2. DÉTECTER LES QUANTITÉS (%, g, mg, ml, etc.)
        # ===================================================================
        # Pattern: nombre + unité optionnelle
        quantity_pattern = r'\b\d+(?:[.,]\d+)?\s*(?:%|g|kg|mg|ml|l|cl|dl)\b'
        for match in re.finditer(quantity_pattern, text, re.IGNORECASE):
            entities.append((match.start(), match.end(), 'QUANTITY'))
        
        # Pattern: "moins de X", "minimum X%", etc.
        context_qty_pattern = r'(?:moins de|minimum|maximum|environ)\s+\d+(?:[.,]\d+)?\s*%?'
        for match in re.finditer(context_qty_pattern, text, re.IGNORECASE):
            entities.append((match.start(), match.end(), 'QUANTITY'))
        
        # ===================================================================
        # 3. DÉTECTER LES MINÉRAUX
        # ===================================================================
        for mineral in self.minerals:
            # Pattern flexible: capture le mot avec variations (ex: "calcium", "calcique")
            pattern = rf'\b{re.escape(mineral)}[a-zéèêàùç]*\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append((match.start(), match.end(), 'INGREDIENT'))
        
        # ===================================================================
        # 4. DÉTECTER LES VITAMINES
        # ===================================================================
        for vitamin in self.vitamins:
            pattern = rf'\b{re.escape(vitamin)}[a-zéèêàùç]*\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append((match.start(), match.end(), 'INGREDIENT'))
        
        # Détecter les formes "Vitamine A", "Vitamin B12", etc.
        vitamin_code_pattern = r'\b(?:vitamine|vitamin)\s*[A-K]\d{0,2}\b'
        for match in re.finditer(vitamin_code_pattern, text, re.IGNORECASE):
            entities.append((match.start(), match.end(), 'INGREDIENT'))
        
        # ===================================================================
        # 5. DÉTECTER LES ALLERGÈNES
        # ===================================================================
        for allergen in self.all_allergens:
            pattern = rf'\b{re.escape(allergen)}[a-zéèêàùç]*\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append((match.start(), match.end(), 'ALLERGEN'))
        
        # ===================================================================
        # 6. DÉTECTER LES INGRÉDIENTS CLASSIQUES
        # ===================================================================
        for ingredient in self.all_ingredients:
            # Pattern amélioré: capture les qualificatifs (ex: "farine de blé")
            # On cherche le mot exact + possibles variations grammaticales
            pattern = rf'\b{re.escape(ingredient)}[a-zéèêàùç]*\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append((match.start(), match.end(), 'INGREDIENT'))
        
        # Détecter les patterns composés (ex: "farine de blé", "huile d'olive")
        compound_pattern = r'\b[a-zéèêàùç]+\s+(?:de|d\')\s+[a-zéèêàùç]+\b'
        for match in re.finditer(compound_pattern, text, re.IGNORECASE):
            # Vérifier si l'un des mots est un ingrédient connu
            words = match.group(0).lower().split()
            for ingredient in self.all_ingredients:
                if ingredient in words:
                    entities.append((match.start(), match.end(), 'INGREDIENT'))
                    break
        
        # ===================================================================
        # 7. RÉSOUDRE LES CHEVAUCHEMENTS
        # ===================================================================
        # Trier par position, puis par priorité (ALLERGEN > QUANTITY > INGREDIENT)
        priority = {'ALLERGEN': 3, 'QUANTITY': 2, 'INGREDIENT': 1}
        entities = sorted(entities, key=lambda x: (x[0], -priority.get(x[2], 0)))
        
        # Supprimer les chevauchements
        non_overlapping = []
        for entity in entities:
            start, end, label = entity
            # Vérifier qu'il n'y a pas de chevauchement avec une entité déjà ajoutée
            overlaps = False
            for existing_start, existing_end, existing_label in non_overlapping:
                if not (end <= existing_start or start >= existing_end):
                    overlaps = True
                    break
            
            if not overlaps:
                non_overlapping.append(entity)
        
        return non_overlapping
    
    def create_spacy_format(self, text: str, entities: List[Tuple[int, int, str]]) -> Dict[str, Any]:
        """
        Convertit les entités au format spaCy .spacy.
        
        Returns:
            {"text": "...", "entities": [(start, end, label), ...]}
        """
        return {
            "text": text,
            "entities": entities
        }


def create_improved_annotations(
    input_file: str,
    output_file: str,
    sample_size: int = 2000
) -> None:
    """
    Crée des annotations NER améliorées v3.0 FINAL.
    
    Args:
        input_file: Chemin du fichier de données nettoyées
        output_file: Chemin du fichier de sortie (.jsonl)
        sample_size: Nombre de produits à annoter
    """
    log.info("=" * 80)
    log.info("🚀 AUTO-ANNOTATION NER v3.0 FINAL")
    log.info("=" * 80)
    log.info(f"   Input:  {input_file}")
    log.info(f"   Output: {output_file}")
    log.info(f"   Sample: {sample_size} produits")
    log.info("")
    
    # Charger les données
    df = load_dataframe(input_file)
    log.info(f"✅ Chargé: {len(df)} produits")
    
    # Échantillonner
    if len(df) > sample_size:
        df_sample = df.sample(n=sample_size, random_state=42)
        log.info(f"📊 Échantillon: {sample_size} produits")
    else:
        df_sample = df
    
    # Initialiser l'annotateur
    annotator = FinalNERAnnotator()
    
    # Annoter
    training_data = []
    log.info("🏷️  Annotation en cours...")
    
    for _, row in tqdm(df_sample.iterrows(), total=len(df_sample), desc="Annotation"):
        # Annoter le champ 'ingredients_text'
        if pd.notna(row.get('ingredients_text')):
            text = str(row['ingredients_text']).strip()
            if len(text) > 2:
                entities = annotator.annotate(text)
                if entities:  # Seulement si on a trouvé des entités
                    spacy_format = annotator.create_spacy_format(text, entities)
                    training_data.append(spacy_format)
    
    log.info(f"✅ Annoté: {len(training_data)} textes avec entités")
    
    # Statistiques
    total_entities = sum(len(item['entities']) for item in training_data)
    entity_counts = {}
    for item in training_data:
        for _, _, label in item['entities']:
            entity_counts[label] = entity_counts.get(label, 0) + 1
    
    log.info("\n📊 STATISTIQUES DES ANNOTATIONS:")
    log.info(f"   • Textes annotés: {len(training_data)}")
    log.info(f"   • Entités totales: {total_entities}")
    log.info(f"   • Moyenne par texte: {total_entities / len(training_data):.1f}")
    for label, count in sorted(entity_counts.items()):
        log.info(f"   • {label}: {count}")
    
    # Sauvegarder au format JSONL
    ensure_dir(Path(output_file).parent)
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in training_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    log.info(f"\n✅ Annotations sauvegardées: {output_file}")
    log.info("=" * 80)


if __name__ == "__main__":
    # Chemins des fichiers
    input_file = "datasets/cleaned/products_cleaned.csv"
    output_file = "datasets/preprocessed/ner_annotations_v3.jsonl"
    
    # Créer les annotations v3.0 FINAL
    create_improved_annotations(
        input_file=input_file,
        output_file=output_file,
        sample_size=2000
    )
    
    log.info("\n🎉 AUTO-ANNOTATION NER v3.0 FINAL TERMINÉE !")

