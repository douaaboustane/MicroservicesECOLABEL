"""
Agrégateur d'impacts - Combine tous les impacts
"""
from typing import Dict, Any, List


class ImpactAggregator:
    """Agrège les impacts de toutes les sources"""
    
    @staticmethod
    def aggregate(
        ingredients_impacts: Dict[str, Any],
        packaging_impacts: Dict[str, float],
        transport_impacts: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Agrège tous les impacts.
        
        Args:
            ingredients_impacts: Impacts des ingrédients (avec total et détails)
            packaging_impacts: Impacts de l'emballage
            transport_impacts: Impacts du transport
        
        Returns:
            Dictionnaire avec impacts totaux et décomposition
        """
        # Impacts totaux
        total_impacts = {
            "co2_kg": ingredients_impacts["total"]["co2_kg"] + packaging_impacts["co2_kg"] + transport_impacts["co2_kg"],
            "water_m3": ingredients_impacts["total"]["water_m3"] + packaging_impacts["water_m3"] + transport_impacts["water_m3"],
            "energy_mj": ingredients_impacts["total"]["energy_mj"] + packaging_impacts["energy_mj"] + transport_impacts["energy_mj"],
            "acidification": ingredients_impacts["total"]["acidification"] + packaging_impacts["acidification"] + transport_impacts["acidification"],
            "eutrophisation": ingredients_impacts["total"]["eutrophisation"] + packaging_impacts["eutrophisation"] + transport_impacts["eutrophisation"]
        }
        
        # Détail par catégorie
        total_co2 = total_impacts["co2_kg"]
        
        breakdown = {
            "ingredients": {
                **ingredients_impacts["total"],
                "contribution_percentage": (ingredients_impacts["total"]["co2_kg"] / total_co2 * 100) if total_co2 > 0 else 0.0
            },
            "packaging": {
                **packaging_impacts,
                "contribution_percentage": (packaging_impacts["co2_kg"] / total_co2 * 100) if total_co2 > 0 else 0.0
            },
            "transport": {
                **transport_impacts,
                "contribution_percentage": (transport_impacts["co2_kg"] / total_co2 * 100) if total_co2 > 0 else 0.0
            }
        }
        
        return {
            "total": total_impacts,
            "breakdown": breakdown,
            "ingredients_detail": ingredients_impacts["ingredients"]
        }

