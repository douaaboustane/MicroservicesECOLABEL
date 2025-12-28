from app.ocr.tesseract_engine import TesseractOCR
from app.extractors.barcode_extractor import BarcodeExtractor
from typing import Dict
import os


class ImageParser:
    def __init__(self):
        self.ocr = TesseractOCR()
        self.barcode_extractor = BarcodeExtractor()
    
    def parse(self, file_path: str) -> Dict:
        """Parse une image (OCR + codes-barres)"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Fichier image introuvable: {file_path}")
        
        # OCR
        text, confidence = self.ocr.extract_text(file_path)
        
        # Extraction code-barres
        gtin = self.barcode_extractor.extract_gtin(file_path)
        
        # Si pas de GTIN dans l'image, chercher dans le texte OCR
        if not gtin:
            gtin = self.barcode_extractor.extract_from_text(text)
        
        return {
            "text": text,
            "gtin": gtin,
            "confidence": confidence,
            "method": "ocr_extraction"
        }
    
    def parse_with_boxes(self, file_path: str) -> Dict:
        """Parse avec coordonnées des boîtes de texte"""
        ocr_result = self.ocr.extract_with_boxes(file_path)
        gtin = self.barcode_extractor.extract_gtin(file_path)
        
        return {
            **ocr_result,
            "gtin": gtin,
            "method": "ocr_with_boxes"
        }

