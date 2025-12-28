from bs4 import BeautifulSoup
import re
from typing import Optional, Dict


class HTMLParser:
    def parse(self, file_path: str) -> Dict:
        """Parse un fichier HTML de fiche produit"""
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Extraction des éléments clés
        product_name = self._extract_product_name(soup)
        ingredients = self._extract_ingredients(soup)
        gtin = self._extract_gtin(soup)
        packaging = self._extract_packaging(soup)
        
        # Texte brut complet
        text = soup.get_text(separator=' ', strip=True)
        
        return {
            "product_name": product_name,
            "ingredients_raw": ingredients,
            "gtin": gtin,
            "packaging_info": packaging,
            "text": text,
            "confidence": 0.95,
            "method": "html_parsing"
        }
    
    def _extract_product_name(self, soup: BeautifulSoup) -> str:
        """Cherche le nom du produit dans les balises communes"""
        selectors = [
            'h1.product-name',
            '.product-title',
            'h1',
            'title',
            '[itemprop="name"]',
            '.product-name',
            '#product-name'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                name = element.get_text(strip=True)
                if name and len(name) > 3:
                    return name
        
        return "Unknown Product"
    
    def _extract_ingredients(self, soup: BeautifulSoup) -> str:
        """Extrait la liste d'ingrédients"""
        keywords = ['ingrédients', 'ingredients', 'composition', 'constituants']
        
        # Chercher dans les ID/class contenant le mot-clé
        for keyword in keywords:
            # Par ID
            element = soup.find(id=re.compile(keyword, re.I))
            if element:
                return element.get_text(strip=True)
            
            # Par class
            element = soup.find(class_=re.compile(keyword, re.I))
            if element:
                return element.get_text(strip=True)
            
            # Par itemprop
            element = soup.find(itemprop=re.compile(keyword, re.I))
            if element:
                return element.get_text(strip=True)
            
            # Par texte dans les balises
            for tag in soup.find_all(['div', 'p', 'span', 'li']):
                text = tag.get_text().lower()
                if keyword in text and len(text) > 20:
                    # Vérifier que c'est bien une liste d'ingrédients
                    if any(char in text for char in [',', ';', '•', '-']):
                        return tag.get_text(strip=True)
        
        return ""
    
    def _extract_gtin(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait le GTIN depuis le HTML"""
        # Chercher dans les meta tags
        meta_selectors = [
            {'property': 'product:gtin'},
            {'name': 'gtin'},
            {'name': 'ean'},
            {'itemprop': 'gtin'},
            {'itemprop': 'ean'}
        ]
        
        for selector in meta_selectors:
            gtin_meta = soup.find('meta', selector)
            if gtin_meta:
                content = gtin_meta.get('content')
                if content and content.isdigit():
                    return content
        
        # Chercher dans le texte avec regex
        text = soup.get_text()
        pattern = r'(?:GTIN|EAN|Barcode|Code-barres)[\s:]*(\d{8,14})'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None
    
    def _extract_packaging(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait les informations d'emballage"""
        keywords = ['emballage', 'packaging', 'conditionnement']
        
        for keyword in keywords:
            element = soup.find(
                lambda tag: tag.name in ['div', 'p', 'span'] and
                keyword in str(tag.get('class', '')).lower()
            )
            
            if element:
                return element.get_text(strip=True)
        
        return None

