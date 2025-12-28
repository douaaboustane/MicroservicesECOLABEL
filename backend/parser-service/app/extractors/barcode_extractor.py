from pyzbar.pyzbar import decode
from PIL import Image
import re
from typing import Optional


class BarcodeExtractor:
    def extract_gtin(self, image_path: str) -> Optional[str]:
        """Extrait le code-barres GTIN d'une image"""
        try:
            img = Image.open(image_path)
            barcodes = decode(img)
            
            for barcode in barcodes:
                data = barcode.data.decode('utf-8')
                # Vérifier si c'est un GTIN valide (8, 12, 13 ou 14 chiffres)
                if self._is_valid_gtin(data):
                    return data
        except Exception:
            pass
        
        return None
    
    def extract_from_text(self, text: str) -> Optional[str]:
        """Extrait GTIN depuis du texte OCR"""
        # Pattern pour GTIN (8, 12, 13 ou 14 chiffres)
        pattern = r'\b\d{8}\b|\b\d{12}\b|\b\d{13}\b|\b\d{14}\b'
        matches = re.findall(pattern, text)
        
        for match in matches:
            if self._is_valid_gtin(match):
                return match
        
        return None
    
    def _is_valid_gtin(self, code: str) -> bool:
        """Valide un GTIN avec checksum"""
        if not code.isdigit():
            return False
        
        if len(code) not in [8, 12, 13, 14]:
            return False
        
        # Validation checksum (algorithme GTIN)
        digits = [int(d) for d in code]
        check_digit = digits[-1]
        
        # Calcul du checksum
        weighted_sum = sum(
            d * (3 if i % 2 == 0 else 1)
            for i, d in enumerate(reversed(digits[:-1]))
        )
        
        calculated_check = (10 - (weighted_sum % 10)) % 10
        return check_digit == calculated_check

