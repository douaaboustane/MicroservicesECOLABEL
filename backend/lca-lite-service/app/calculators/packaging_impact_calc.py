"""
Calculateur d'impact pour les emballages
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional

from app.config import settings
from app import schemas


class PackagingImpactCalculator:
    """Calcule les impacts environnementaux des emballages"""
    
    def __init__(self):
        self.impacts_data = {}
        self.load_data()
    
    def load_data(self):
        """Charge les facteurs d'impact des emballages"""
        try:
            file_path = Path(settings.PACKAGING_IMPACTS_FILE)
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.impacts_data = json.load(f)
                print(f"✅ Facteurs emballage chargés: {len(self.impacts_data)} types")
            else:
                print(f"⚠️  Fichier emballage introuvable: {file_path}")
        except Exception as e:
            print(f"❌ Erreur chargement emballage: {e}")
    
    def calculate(self, packaging: Optional[schemas.PackagingInput]) -> Dict[str, Any]:
        """
        Calcule les impacts d'un emballage.
        
        Args:
            packaging: Informations sur l'emballage
        
        Returns:
            Dictionnaire avec impacts
        """
        if not packaging:
            return {
                "co2_kg": 0.0,
                "water_m3": 0.0,
                "energy_mj": 0.0,
                "acidification": 0.0,
                "eutrophisation": 0.0
            }
        
        # Déterminer le poids en kg
        weight_kg = packaging.weight_kg
        if weight_kg is None and packaging.weight_g:
            weight_kg = packaging.weight_g / 1000.0
        
        if weight_kg is None or weight_kg <= 0:
            # Poids par défaut si non spécifié
            weight_kg = 0.1  # 100g par défaut
        
        # Normaliser le type d'emballage
        packaging_type = packaging.type.lower()
        
        # Chercher les facteurs d'impact
        factors = self.impacts_data.get(packaging_type)
        if not factors:
            # Valeur par défaut (plastique moyen)
            factors = {
                "co2_kg_per_kg": 1.5,
                "water_m3_per_kg": 0.01,
                "energy_mj_per_kg": 45.0
            }
        
        # Calculer les impacts
        impacts = {
            "co2_kg": factors.get("co2_kg_per_kg", 0.0) * weight_kg,
            "water_m3": factors.get("water_m3_per_kg", 0.0) * weight_kg,
            "energy_mj": factors.get("energy_mj_per_kg", 0.0) * weight_kg,
            "acidification": 0.0,  # Non disponible dans les facteurs simples
            "eutrophisation": 0.0
        }
        
        # Bonus recyclabilité (réduction de 10% si recyclable)
        if packaging.recyclable:
            impacts["co2_kg"] *= 0.9
            impacts["energy_mj"] *= 0.9
        
        return impacts

