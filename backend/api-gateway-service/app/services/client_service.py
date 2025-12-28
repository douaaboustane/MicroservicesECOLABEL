"""
Client HTTP pour communiquer avec les microservices
"""
import httpx
from typing import Dict, Any, List, Optional
from app.config import settings


class MicroserviceClient:
    """Client HTTP pour communiquer avec les microservices"""
    
    def __init__(self):
        self.parser_url = settings.PARSER_SERVICE_URL
        self.nlp_url = settings.NLP_SERVICE_URL
        self.lca_url = settings.LCA_SERVICE_URL
        self.scoring_url = settings.SCORING_SERVICE_URL
    
    async def call_parser_service(
        self,
        image_file: bytes,
        filename: str
    ) -> Dict[str, Any]:
        """Appelle le Parser Service pour OCR et extraction"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            files = {"file": (filename, image_file, "image/jpeg")}
            response = await client.post(
                f"{self.parser_url}/product/parse/single",
                files=files
            )
            response.raise_for_status()
            return response.json()
    
    async def call_nlp_service(
        self,
        ingredients_text: str,
        normalize: bool = True
    ) -> Dict[str, Any]:
        """Appelle le NLP Service pour extraction d'ingrédients"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.nlp_url}/nlp/extract",
                json={
                    "text": ingredients_text,
                    "normalize": normalize,
                    "detect_labels": True,
                    "detect_packaging": True,
                    "detect_origin": True
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def call_lca_service(
        self,
        ingredients: List[Dict[str, Any]],
        packaging: Optional[Dict[str, Any]] = None,
        transport: Optional[Dict[str, Any]] = None,
        product_weight_kg: float = 1.0
    ) -> Dict[str, Any]:
        """Appelle le LCA Service pour calcul d'impacts"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.lca_url}/lca/calc",
                json={
                    "ingredients": ingredients,
                    "packaging": packaging or {},
                    "transport": transport or {},
                    "product_weight_kg": product_weight_kg
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def call_scoring_service(
        self,
        lca_data: Dict[str, Any],
        nlp_data: Dict[str, Any],
        method: str = "hybrid"
    ) -> Dict[str, Any]:
        """Appelle le Scoring Service pour calcul du score"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Préparer les données pour le scoring
            ingredients_list = [
                ing.get("text", "") if isinstance(ing, dict) else str(ing)
                for ing in nlp_data.get("ingredients", [])
            ]
            
            labels_list = nlp_data.get("labels", [])
            packaging_info = nlp_data.get("packaging", {})
            
            response = await client.post(
                f"{self.scoring_url}/score/calculate",
                json={
                    "lca_data": {
                        "co2_kg": lca_data.get("total_impacts", {}).get("co2_kg", 0),
                        "water_liters": lca_data.get("total_impacts", {}).get("water_m3", 0) * 1000,
                        "energy_mj": lca_data.get("total_impacts", {}).get("energy_mj", 0),
                        "acidification": lca_data.get("total_impacts", {}).get("acidification", 0),
                        "eutrophisation": lca_data.get("total_impacts", {}).get("eutrophisation", 0)
                    },
                    "nlp_data": {
                        "ingredients": ingredients_list,
                        "allergens": [
                            allergen.get("text", "") if isinstance(allergen, dict) else str(allergen)
                            for allergen in nlp_data.get("allergens", [])
                        ],
                        "labels": labels_list,
                        "packaging_type": packaging_info.get("type") if isinstance(packaging_info, dict) else None,
                        "origin_country": nlp_data.get("origin", {}).get("country") if isinstance(nlp_data.get("origin"), dict) else None,
                        "has_bio_label": any("bio" in str(label).lower() for label in labels_list),
                        "has_fair_trade": any("fair" in str(label).lower() or "équitable" in str(label).lower() for label in labels_list),
                        "has_recyclable_packaging": packaging_info.get("recyclable", False) if isinstance(packaging_info, dict) else False,
                        "has_local_origin": nlp_data.get("origin", {}).get("is_local", False) if isinstance(nlp_data.get("origin"), dict) else False,
                        "has_palm_oil": any("palme" in str(ing).lower() for ing in ingredients_list),
                        "has_high_sugar": any("sucre" in str(ing).lower() for ing in ingredients_list),
                        "has_additives": any("e" in str(ing).lower() and str(ing).lower().startswith("e") for ing in ingredients_list)
                    },
                    "method": method
                }
            )
            response.raise_for_status()
            return response.json()

