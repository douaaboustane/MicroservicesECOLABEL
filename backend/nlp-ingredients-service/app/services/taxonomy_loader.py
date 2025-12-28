"""
Chargeur de taxonomies
"""
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any

from app.config import settings


class TaxonomyLoader:
    """Charge les taxonomies d'ingrédients depuis différentes sources"""
    
    def __init__(self):
        self.taxonomy = {}
        self.loaded = False
        self.sources_loaded = []
    
    def load_from_json(self, file_path: str) -> Dict[str, Any]:
        """
        Charge une taxonomie depuis un fichier JSON.
        
        Args:
            file_path: Chemin du fichier JSON
        
        Returns:
            Dictionnaire de taxonomie
        """
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"⚠️  Fichier taxonomie introuvable: {file_path}")
                return {}
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ Taxonomie JSON chargée: {file_path} ({len(data)} items)")
            self.sources_loaded.append(f"JSON: {path.name}")
            return data
            
        except Exception as e:
            print(f"❌ Erreur chargement taxonomie JSON {file_path}: {e}")
            return {}
    
    def load_from_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Charge une taxonomie depuis un fichier CSV.
        
        Format attendu du CSV:
        - name: Nom de l'ingrédient
        - name_normalized: Nom normalisé
        - category: Catégorie
        - agribalyse_code: Code Agribalyse
        - ecoinvent_code: Code EcoInvent
        - synonyms: Synonymes séparés par des virgules
        - is_allergen: Booléen
        
        Args:
            file_path: Chemin du fichier CSV
        
        Returns:
            Dictionnaire de taxonomie
        """
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"⚠️  Fichier taxonomie introuvable: {file_path}")
                return {}
            
            df = pd.read_csv(path)
            taxonomy = {}
            
            for _, row in df.iterrows():
                # Utiliser le nom normalisé comme clé
                name = row.get('name_normalized', row.get('name', '')).lower().strip()
                if not name:
                    continue
                
                taxonomy[name] = {
                    'name': row.get('name', name),
                    'category': row.get('category'),
                    'agribalyse_code': row.get('agribalyse_code'),
                    'ecoinvent_code': row.get('ecoinvent_code'),
                    'synonyms': [],
                    'is_allergen': bool(row.get('is_allergen', False)),
                    'allergen_category': row.get('allergen_category')
                }
                
                # Parser les synonymes
                if 'synonyms' in row and pd.notna(row['synonyms']):
                    synonyms = str(row['synonyms']).split(',')
                    taxonomy[name]['synonyms'] = [s.strip() for s in synonyms if s.strip()]
            
            print(f"✅ Taxonomie CSV chargée: {file_path} ({len(taxonomy)} items)")
            self.sources_loaded.append(f"CSV: {path.name}")
            return taxonomy
            
        except Exception as e:
            print(f"❌ Erreur chargement taxonomie CSV {file_path}: {e}")
            return {}
    
    def merge_taxonomies(self, *taxonomies: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fusionne plusieurs taxonomies.
        
        La première taxonomie a la priorité, les suivantes complètent.
        
        Args:
            *taxonomies: Dictionnaires de taxonomies à fusionner
        
        Returns:
            Taxonomie fusionnée
        """
        merged = {}
        
        for taxonomy in taxonomies:
            for key, value in taxonomy.items():
                if key not in merged:
                    merged[key] = value
                else:
                    # Compléter les champs manquants
                    for field, val in value.items():
                        if field not in merged[key] or not merged[key][field]:
                            merged[key][field] = val
                    
                    # Fusionner les synonymes
                    if 'synonyms' in value:
                        existing_synonyms = set(merged[key].get('synonyms', []))
                        new_synonyms = set(value.get('synonyms', []))
                        merged[key]['synonyms'] = list(existing_synonyms | new_synonyms)
        
        return merged
    
    def load_all(self) -> Dict[str, Any]:
        """
        Charge toutes les taxonomies configurées.
        
        Ordre de chargement:
        1. Taxonomie principale (JSON)
        2. Agribalyse (CSV)
        3. EcoInvent (CSV)
        
        Returns:
            Taxonomie complète fusionnée
        """
        print("\n" + "=" * 70)
        print(" " * 20 + "📚 CHARGEMENT DES TAXONOMIES")
        print("=" * 70)
        
        taxonomies = []
        
        # 1. Taxonomie principale (JSON)
        if hasattr(settings, 'TAXONOMY_FILE'):
            main_taxonomy = self.load_from_json(settings.TAXONOMY_FILE)
            if main_taxonomy:
                taxonomies.append(main_taxonomy)
        
        # 2. Agribalyse (CSV)
        if hasattr(settings, 'AGRIBALYSE_FILE'):
            agribalyse = self.load_from_csv(settings.AGRIBALYSE_FILE)
            if agribalyse:
                taxonomies.append(agribalyse)
        
        # 3. EcoInvent (CSV)
        if hasattr(settings, 'ECOINVENT_FILE'):
            ecoinvent = self.load_from_csv(settings.ECOINVENT_FILE)
            if ecoinvent:
                taxonomies.append(ecoinvent)
        
        # Fusionner toutes les taxonomies
        if taxonomies:
            self.taxonomy = self.merge_taxonomies(*taxonomies)
            self.loaded = True
            
            print(f"\n✅ Taxonomie fusionnée: {len(self.taxonomy)} ingrédients")
            print(f"   Sources: {', '.join(self.sources_loaded)}")
        else:
            print("\n⚠️  Aucune taxonomie chargée")
            self.loaded = False
        
        print("=" * 70 + "\n")
        
        return self.taxonomy
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retourne des statistiques sur la taxonomie chargée"""
        if not self.taxonomy:
            return {
                "total": 0,
                "loaded": False
            }
        
        categories = {}
        allergens = 0
        with_agribalyse = 0
        with_ecoinvent = 0
        
        for item in self.taxonomy.values():
            # Compter par catégorie
            cat = item.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            # Compter les allergènes
            if item.get('is_allergen'):
                allergens += 1
            
            # Compter les codes
            if item.get('agribalyse_code'):
                with_agribalyse += 1
            if item.get('ecoinvent_code'):
                with_ecoinvent += 1
        
        return {
            "total": len(self.taxonomy),
            "loaded": self.loaded,
            "categories": categories,
            "allergens": allergens,
            "with_agribalyse_code": with_agribalyse,
            "with_ecoinvent_code": with_ecoinvent,
            "sources": self.sources_loaded
        }

