"""
Interface à la base de données Agribalyse
"""
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import json

from app.config import settings


class AgribalyseDB:
    """Gestionnaire de la base de données Agribalyse"""
    
    def __init__(self):
        self.data = None
        self.loaded = False
        self.load_data()
    
    def load_data(self):
        """Charge les données Agribalyse depuis le CSV (gzip ou non)"""
        try:
            file_path = Path(settings.AGRIBALYSE_FILE)
            if not file_path.exists():
                print(f"⚠️  Fichier Agribalyse introuvable: {file_path}")
                return
            
            # Détecter si le fichier est compressé (gzip)
            import gzip
            with open(file_path, 'rb') as f:
                first_bytes = f.read(2)
                is_gzipped = first_bytes == b'\x1f\x8b'
            
            # Charger le CSV
            if is_gzipped:
                print(f"📦 Fichier Agribalyse détecté comme gzip, décompression...")
                self.data = pd.read_csv(gzip.open(file_path, 'rt'), encoding='utf-8')
            else:
                # Essayer différents encodages pour les fichiers non compressés
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        self.data = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError("Impossible de décoder le fichier avec les encodages testés")
            
            self.loaded = True
            print(f"✅ Agribalyse chargé: {len(self.data)} produits")
            
        except Exception as e:
            print(f"❌ Erreur chargement Agribalyse: {e}")
            import traceback
            traceback.print_exc()
            self.loaded = False
    
    def get_impact_by_code(self, code: str) -> Optional[Dict[str, float]]:
        """
        Récupère les impacts pour un code Agribalyse.
        
        Args:
            code: Code Agribalyse
        
        Returns:
            Dictionnaire avec les impacts ou None
        """
        if not self.loaded or self.data is None:
            return None
        
        # Chercher par code (peut être dans différentes colonnes)
        code_columns = ['code_agribalyse', 'Code_Agribalyse', 'code', 'Code']
        
        for col in code_columns:
            if col in self.data.columns:
                match = self.data[self.data[col] == code]
                if not match.empty:
                    return self._extract_impacts(match.iloc[0])
        
        return None
    
    def get_impact_by_name(self, name: str, fuzzy: bool = False) -> Optional[Dict[str, float]]:
        """
        Récupère les impacts par nom d'ingrédient.
        
        Args:
            name: Nom de l'ingrédient
            fuzzy: Utiliser recherche floue
        
        Returns:
            Dictionnaire avec les impacts ou None
        """
        if not self.loaded or self.data is None:
            return None
        
        # Normaliser le nom
        name_lower = name.lower().strip()
        
        # Colonnes possibles pour le nom
        name_columns = ['nom', 'Nom', 'name', 'Name', 'libelle_francais', 'Libelle_francais']
        
        for col in name_columns:
            if col in self.data.columns:
                # Recherche exacte
                match = self.data[
                    self.data[col].str.lower().str.strip() == name_lower
                ]
                if not match.empty:
                    return self._extract_impacts(match.iloc[0])
                
                # Recherche partielle
                match = self.data[
                    self.data[col].str.lower().str.contains(name_lower, na=False)
                ]
                if not match.empty:
                    return self._extract_impacts(match.iloc[0])
        
        return None
    
    def _extract_impacts(self, row: pd.Series) -> Dict[str, float]:
        """
        Extrait les impacts d'une ligne Agribalyse.
        
        Args:
            row: Ligne du DataFrame
        
        Returns:
            Dictionnaire avec les impacts
        """
        impacts = {}
        
        # Mapper les colonnes Agribalyse aux impacts
        column_mapping = {
            # Changement climatique (CO2)
            'Changement_climatique': 'co2_kg_per_kg',
            'changement_climatique': 'co2_kg_per_kg',
            'EF_single_score': 'co2_kg_per_kg',  # Approximatif
            'ef_single_score': 'co2_kg_per_kg',
            'CO2': 'co2_kg_per_kg',
            'co2': 'co2_kg_per_kg',
            
            # Eau
            'Consommation_eau': 'water_m3_per_kg',
            'consommation_eau': 'water_m3_per_kg',
            'Eau': 'water_m3_per_kg',
            'eau': 'water_m3_per_kg',
            
            # Énergie
            'Consommation_energie': 'energy_mj_per_kg',
            'consommation_energie': 'energy_mj_per_kg',
            'Energie': 'energy_mj_per_kg',
            'energie': 'energy_mj_per_kg',
            
            # Acidification
            'Acidification': 'acidification_per_kg',
            'acidification': 'acidification_per_kg',
            
            # Eutrophisation
            'Eutrophisation': 'eutrophisation_per_kg',
            'eutrophisation': 'eutrophisation_per_kg',
        }
        
        for col, key in column_mapping.items():
            if col in row.index and pd.notna(row[col]):
                try:
                    impacts[key] = float(row[col])
                except (ValueError, TypeError):
                    pass
        
        return impacts
    
    def search(self, query: str, limit: int = 10) -> list:
        """
        Recherche dans Agribalyse.
        
        Args:
            query: Terme de recherche
            limit: Nombre de résultats max
        
        Returns:
            Liste de résultats
        """
        if not self.loaded or self.data is None:
            return []
        
        query_lower = query.lower()
        results = []
        
        # Chercher dans les colonnes de nom
        name_columns = ['nom', 'Nom', 'name', 'Name', 'libelle_francais']
        
        for col in name_columns:
            if col in self.data.columns:
                matches = self.data[
                    self.data[col].str.lower().str.contains(query_lower, na=False)
                ]
                
                for _, row in matches.head(limit).iterrows():
                    code_col = 'code_agribalyse' if 'code_agribalyse' in self.data.columns else 'Code_Agribalyse'
                    code = row.get(code_col, '')
                    name = row.get(col, '')
                    
                    results.append({
                        'code': str(code),
                        'name': str(name),
                        'impacts': self._extract_impacts(row)
                    })
                
                if results:
                    break
        
        return results[:limit]

