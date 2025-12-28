"""
Scraper pour Open Food Facts
Collecte les données produits depuis l'API publique OFF
"""
import requests
import pandas as pd
import time
from tqdm import tqdm
import yaml
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log
from utils.file_utils import save_dataframe, ensure_dir


class OpenFoodFactsScraper:
    """Scraper pour Open Food Facts"""
    
    def __init__(self, config_file="config/pipeline_config.yaml"):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        self.config = config['scraping']['openfoodfacts']
        self.base_url = "https://world.openfoodfacts.org/api/v2"
        self.products = []
        
    def scrape(self):
        """Lance le scraping"""
        log.info("Démarrage du scraping Open Food Facts")
        
        max_products = self.config['max_products']
        country = self.config['country']
        rate_limit = self.config['rate_limit']
        
        page = 1
        page_size = 100
        
        with tqdm(total=max_products, desc="Scraping OFF") as pbar:
            while len(self.products) < max_products:
                try:
                    # Appel API
                    url = f"{self.base_url}/search"
                    params = {
                        'countries': country,
                        'page': page,
                        'page_size': page_size,
                        'fields': 'code,product_name,ingredients_text,categories,labels,packaging,origins,nutriscore_grade,ecoscore_grade,allergens'
                    }
                    
                    response = requests.get(url, params=params, timeout=30)
                    response.raise_for_status()
                    
                    data = response.json()
                    products = data.get('products', [])
                    
                    if not products:
                        log.info("Plus de produits disponibles")
                        break
                    
                    # Filtrer et nettoyer
                    for product in products:
                        if len(self.products) >= max_products:
                            break
                        
                        if self._is_valid_product(product):
                            self.products.append(self._clean_product(product))
                    
                    pbar.update(len(products))
                    page += 1
                    
                    # Rate limiting
                    time.sleep(1 / rate_limit)
                    
                except Exception as e:
                    log.error(f"Erreur page {page}: {e}")
                    time.sleep(5)
                    continue
        
        log.info(f"Scraping terminé: {len(self.products)} produits collectés")
        
    def _is_valid_product(self, product: dict) -> bool:
        """Vérifie qu'un produit a les champs obligatoires"""
        return (
            product.get('code') and
            product.get('product_name') and
            product.get('ingredients_text')
        )
    
    def _clean_product(self, product: dict) -> dict:
        """Nettoie les données d'un produit"""
        return {
            'code': product.get('code', ''),
            'product_name': product.get('product_name', ''),
            'ingredients_text': product.get('ingredients_text', ''),
            'categories': product.get('categories', ''),
            'labels': product.get('labels', ''),
            'packaging': product.get('packaging', ''),
            'origins': product.get('origins', ''),
            'nutriscore_grade': product.get('nutriscore_grade', 'unknown'),
            'ecoscore_grade': product.get('ecoscore_grade', 'unknown'),
            'allergens': product.get('allergens', ''),
            'source': 'openfoodfacts'
        }
    
    def save(self, output_file="datasets/raw/openfoodfacts_5k.csv"):
        """Sauvegarde les produits"""
        if not self.products:
            log.warning("Aucun produit à sauvegarder")
            return
        
        ensure_dir(Path(output_file).parent)
        df = pd.DataFrame(self.products)
        save_dataframe(df, output_file, compression='gzip')
        
        log.info(f"Sauvegardé: {output_file}")
        log.info(f"Total: {len(df)} produits")


def main():
    """Point d'entrée"""
    scraper = OpenFoodFactsScraper()
    scraper.scrape()
    scraper.save()
    
    log.info("✅ Scraping Open Food Facts terminé")


if __name__ == "__main__":
    main()

