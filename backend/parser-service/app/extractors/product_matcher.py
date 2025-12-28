from typing import Optional, Dict
from app.extractors.barcode_extractor import BarcodeExtractor


class ProductMatcher:
    """Matching de produits avec bases de données externes"""
    
    def __init__(self):
        self.barcode_extractor = BarcodeExtractor()
    
    def match_by_gtin(self, gtin: str) -> Optional[Dict]:
        """
        Match un produit par son GTIN
        TODO: Intégrer avec une API externe (Open Food Facts, etc.)
        """
        if not gtin or not self.barcode_extractor._is_valid_gtin(gtin):
            return None
        
        # Placeholder pour intégration future
        # Exemple: appeler Open Food Facts API
        # response = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{gtin}.json")
        
        return None
    
    def match_by_name(self, product_name: str) -> Optional[Dict]:
        """
        Match un produit par son nom
        TODO: Intégrer avec recherche sémantique
        """
        if not product_name or len(product_name) < 3:
            return None
        
        # Placeholder pour recherche future
        return None
    
    def enrich_product_data(self, parsed_data: Dict) -> Dict:
        """
        Enrichit les données parsées avec des informations externes
        """
        enriched = parsed_data.copy()
        
        # Essayer de matcher par GTIN
        if parsed_data.get('gtin'):
            match = self.match_by_gtin(parsed_data['gtin'])
            if match:
                enriched['external_data'] = match
        
        # Essayer de matcher par nom
        if parsed_data.get('product_name'):
            match = self.match_by_name(parsed_data['product_name'])
            if match:
                enriched['name_match'] = match
        
        return enriched

