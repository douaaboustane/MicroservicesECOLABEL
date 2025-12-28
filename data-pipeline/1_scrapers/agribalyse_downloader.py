"""
Loader pour Agribalyse 3.2
Charge et traite les données d'impact environnemental depuis Agribalyse/ADEME
Utilise le fichier CSV converti depuis le fichier Excel officiel
"""
import pandas as pd
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import save_dataframe, ensure_dir


class AgribalyseDownloader:
    """Loader pour base Agribalyse 3.2"""
    
    def __init__(self):
        # Chemin vers le fichier CSV converti depuis Excel
        self.csv_file = "datasets/reference/agribalyse_produits_alimentaires.csv"
        
    def load(self):
        """Charge les données Agribalyse depuis le CSV"""
        log.info("Chargement Agribalyse 3.2...")
        
        try:
            # Charger le CSV (header est maintenant la ligne 0)
            df = pd.read_csv(self.csv_file, encoding='utf-8')
            
            log.info(f"✅ Chargé: {len(df)} produits alimentaires")
            log.info(f"   Colonnes: {len(df.columns)}")
            
            return df
            
        except FileNotFoundError:
            log.error(f"Fichier introuvable: {self.csv_file}")
            log.error("Assurez-vous d'avoir converti le fichier Excel en CSV")
            raise
        except Exception as e:
            log.error(f"Erreur chargement: {e}")
            raise
    
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Traite les données Agribalyse"""
        log.info("Traitement des données...")
        
        # Mapping exact des colonnes basé sur les noms avec unités
        column_mapping = {
            'code_agb': 'Code\nAGB',
            'code_ciqual': 'Code\nCIQUAL',
            'group': "Groupe d'aliment",
            'subgroup': "Sous-groupe d'aliment",
            'product_name': 'Nom du Produit en Français',
            'lci_name': 'LCI Name',
            'ef_score_mpt': 'mPt/kg de produit',  # Score unique EF
            'climate_change_kg_co2': 'kg CO2 eq/kg de produit',  # Changement climatique total
            'ozone_depletion': 'kg CVC11 eq/kg de produit',
            'ionising_radiation': 'kBq U-235 eq/kg de produit',
            'photochemical_ozone': 'kg NMVOC eq/kg de produit',
            'particulate_matter': 'disease inc./kg de produit',
            'eutrophication_freshwater': 'kg P eq/kg de produit',  # Phosphore
            'eutrophication_marine': 'kg N eq/kg de produit',  # Azote
            'land_use': 'Pt/kg de produit',
            'water_depletion': 'm3 depriv./kg de produit',
            'energy_depletion': 'MJ/kg de produit',
            'mineral_depletion': 'kg Sb eq/kg de produit'
        }
        
        # Trouver les colonnes correspondantes (exact match)
        selected_cols = {}
        for new_name, col_name in column_mapping.items():
            if col_name in df.columns:
                selected_cols[col_name] = new_name
        
        if not selected_cols:
            log.warning("Impossible de mapper les colonnes, conservation de toutes")
            return df
        
        log.info(f"  {len(selected_cols)} colonnes sélectionnées sur {len(df.columns)}")
        
        # Sélectionner et renommer les colonnes
        df_processed = df[list(selected_cols.keys())].copy()
        df_processed.columns = list(selected_cols.values())
        
        # Nettoyer les données
        log.info("  Nettoyage des données...")
        
        # Supprimer les lignes vides
        df_processed = df_processed.dropna(subset=['product_name'])
        
        # Convertir les valeurs numériques
        numeric_cols = ['ef_score_mpt', 'climate_change_kg_co2', 'ozone_depletion',
                       'ionising_radiation', 'photochemical_ozone', 'particulate_matter',
                       'eutrophication_freshwater', 'eutrophication_marine', 
                       'land_use', 'water_depletion', 'energy_depletion', 'mineral_depletion']
        
        for col in numeric_cols:
            if col in df_processed.columns:
                df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
        
        log.info(f"✓ {len(df_processed)} produits après nettoyage")
        if 'group' in df_processed.columns:
            log.info(f"  Groupes alimentaires: {df_processed['group'].nunique()}")
        if 'climate_change_kg_co2' in df_processed.columns:
            avg_co2 = df_processed['climate_change_kg_co2'].mean()
            log.info(f"  Impact CO2 moyen: {avg_co2:.2f} kg CO2 eq/kg produit")
        
        return df_processed
    
    def save(self, df: pd.DataFrame, output_file="datasets/reference/agribalyse_processed.csv"):
        """Sauvegarde les données traitées"""
        ensure_dir(Path(output_file).parent)
        save_dataframe(df, output_file, compression='gzip')
        
        log.info(f"💾 Sauvegardé: {output_file}")
        log.info(f"📦 Total: {len(df)} produits alimentaires")


def main():
    """Point d'entrée"""
    loader = AgribalyseDownloader()
    df = loader.load()
    df_processed = loader.process(df)
    loader.save(df_processed)
    
    log.info("✅ Chargement et traitement Agribalyse terminé")


if __name__ == "__main__":
    main()

