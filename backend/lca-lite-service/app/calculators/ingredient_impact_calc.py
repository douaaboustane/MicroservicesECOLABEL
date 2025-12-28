"""
Calculateur d'impact pour les ingrédients
"""
from typing import List, Dict, Any, Optional
from app.databases.agribalyse_db import AgribalyseDB
from app import schemas


class IngredientImpactCalculator:
    """Calcule les impacts environnementaux des ingrédients"""
    
    def __init__(self, agribalyse_db: AgribalyseDB):
        self.agribalyse_db = agribalyse_db
    
    def calculate(self, ingredients: List[schemas.IngredientInput], total_weight_kg: Optional[float] = None) -> Dict[str, Any]:
        """
        Calcule les impacts totaux des ingrédients.
        
        Args:
            ingredients: Liste des ingrédients
            total_weight_kg: Poids total du produit (pour convertir % en kg)
        
        Returns:
            Dictionnaire avec impacts totaux et détails
        """
        total_impacts = {
            "co2_kg": 0.0,
            "water_m3": 0.0,
            "energy_mj": 0.0,
            "acidification": 0.0,
            "eutrophisation": 0.0
        }
        
        ingredients_impacts = []
        
        # Calculer le poids total si pas donné et qu'on a des pourcentages
        if total_weight_kg is None:
            # Essayer d'estimer à partir des quantités en kg
            total_kg = sum(ing.quantity_kg for ing in ingredients if ing.quantity_kg)
            if total_kg > 0:
                total_weight_kg = total_kg
            else:
                # Par défaut, estimer 1 kg
                total_weight_kg = 1.0
        
        for ingredient in ingredients:
            # Déterminer la quantité en kg
            quantity_kg = ingredient.quantity_kg
            if quantity_kg is None and ingredient.quantity_percentage:
                quantity_kg = (ingredient.quantity_percentage / 100.0) * total_weight_kg
            
            if quantity_kg is None or quantity_kg <= 0:
                continue  # Skip si pas de quantité
            
            # Récupérer les impacts depuis Agribalyse
            impacts_per_kg = None
            
            # Essayer d'abord par code
            if ingredient.agribalyse_code:
                impacts_data = self.agribalyse_db.get_impact_by_code(ingredient.agribalyse_code)
                if impacts_data:
                    impacts_per_kg = impacts_data
            
            # Sinon, essayer par nom
            if not impacts_per_kg:
                search_name = ingredient.normalized_name or ingredient.name
                impacts_data = self.agribalyse_db.get_impact_by_name(search_name)
                if impacts_data:
                    impacts_per_kg = impacts_data
            
            # Si toujours pas trouvé, utiliser des valeurs par défaut
            if not impacts_per_kg:
                impacts_per_kg = self._get_default_impacts()
            
            # Calculer les impacts pour cette quantité
            ingredient_impacts = {
                "co2_kg": impacts_per_kg.get("co2_kg_per_kg", 0.0) * quantity_kg,
                "water_m3": impacts_per_kg.get("water_m3_per_kg", 0.0) * quantity_kg,
                "energy_mj": impacts_per_kg.get("energy_mj_per_kg", 0.0) * quantity_kg,
                "acidification": impacts_per_kg.get("acidification_per_kg", 0.0) * quantity_kg,
                "eutrophisation": impacts_per_kg.get("eutrophisation_per_kg", 0.0) * quantity_kg
            }
            
            # Ajouter au total
            for key in total_impacts:
                total_impacts[key] += ingredient_impacts.get(key, 0.0)
            
            # Stocker le détail
            ingredients_impacts.append({
                "ingredient_name": ingredient.name,
                "quantity_kg": quantity_kg,
                "impacts": ingredient_impacts,
                "agribalyse_code": ingredient.agribalyse_code
            })
        
        return {
            "total": total_impacts,
            "ingredients": ingredients_impacts
        }
    
    def _get_default_impacts(self) -> Dict[str, float]:
        """
        Retourne des impacts par défaut pour un ingrédient non trouvé.
        
        Returns:
            Facteurs d'impact moyens (conservateurs)
        """
        return {
            "co2_kg_per_kg": 1.0,  # Valeur moyenne conservatrice
            "water_m3_per_kg": 0.01,
            "energy_mj_per_kg": 10.0,
            "acidification_per_kg": 0.005,
            "eutrophisation_per_kg": 0.001
        }

