"""
Service principal de calcul ACV
"""
import time
from typing import Dict, Any

from app import schemas
from app.databases.agribalyse_db import AgribalyseDB
from app.calculators.ingredient_impact_calc import IngredientImpactCalculator
from app.calculators.packaging_impact_calc import PackagingImpactCalculator
from app.calculators.transport_impact_calc import TransportImpactCalculator
from app.calculators.aggregator import ImpactAggregator


class LCAService:
    """Service principal de calcul d'Analyse du Cycle de Vie"""
    
    def __init__(self):
        # Initialiser les bases de données
        self.agribalyse_db = AgribalyseDB()
        
        # Initialiser les calculateurs
        self.ingredient_calc = IngredientImpactCalculator(self.agribalyse_db)
        self.packaging_calc = PackagingImpactCalculator()
        self.transport_calc = TransportImpactCalculator()
        self.aggregator = ImpactAggregator()
    
    def calculate_lca(self, request: schemas.LCACalcRequest) -> schemas.LCACalcResponse:
        """
        Calcule l'ACV complète pour un produit.
        
        Args:
            request: Requête de calcul ACV
        
        Returns:
            Réponse avec tous les impacts
        """
        start_time = time.time()
        
        # 1. Calculer impacts des ingrédients
        ingredients_result = self.ingredient_calc.calculate(
            request.ingredients,
            request.product_weight_kg
        )
        
        # 2. Calculer impacts de l'emballage
        packaging_impacts = self.packaging_calc.calculate(request.packaging)
        
        # 3. Calculer impacts du transport
        product_weight = request.product_weight_kg or 1.0
        transport_impacts = self.transport_calc.calculate(request.transport, product_weight)
        
        # 4. Agrégation totale
        aggregated = self.aggregator.aggregate(
            ingredients_result,
            packaging_impacts,
            transport_impacts
        )
        
        # 5. Construire la réponse
        processing_time = (time.time() - start_time) * 1000
        
        # Convertir en schémas
        total_impacts = schemas.TotalImpacts(**aggregated["total"])
        
        breakdown = {
            key: schemas.ImpactBreakdown(**value)
            for key, value in aggregated["breakdown"].items()
        }
        
        ingredients_impacts_list = [
            schemas.IngredientImpact(
                ingredient_name=ing["ingredient_name"],
                quantity_kg=ing["quantity_kg"],
                impacts=schemas.ImpactBreakdown(**ing["impacts"]),
                agribalyse_code=ing.get("agribalyse_code")
            )
            for ing in aggregated["ingredients_detail"]
        ]
        
        response = schemas.LCACalcResponse(
            total_impacts=total_impacts,
            breakdown=breakdown,
            ingredients_impacts=ingredients_impacts_list,
            product_weight_kg=request.product_weight_kg,
            processing_time_ms=processing_time
        )
        
        return response

