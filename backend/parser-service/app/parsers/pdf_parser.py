from PyPDF2 import PdfReader
import tempfile
from app.ocr.tesseract_engine import TesseractOCR
from typing import Dict
import os


class PDFParser:
    def __init__(self):
        self.ocr = TesseractOCR()
    
    def parse(self, file_path: str) -> Dict:
        """Parse un PDF (texte ou image)"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Fichier PDF introuvable: {file_path}")
        
        reader = PdfReader(file_path)
        
        # Tenter extraction texte natif
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if text.strip():
            # PDF avec texte natif
            return {
                "text": text.strip(),
                "confidence": 1.0,
                "method": "native_extraction",
                "pages": len(reader.pages)
            }
        else:
            # PDF scanné -> nécessite OCR (nécessiterait pdf2image)
            # Pour l'instant, on retourne un texte vide avec indication
            return {
                "text": "",
                "confidence": 0.0,
                "method": "ocr_required",
                "pages": len(reader.pages),
                "note": "PDF scanné détecté. OCR requis (nécessite pdf2image)"
            }
    
    def extract_metadata(self, file_path: str) -> Dict:
        """Extrait les métadonnées du PDF"""
        reader = PdfReader(file_path)
        metadata = reader.metadata or {}
        
        return {
            "title": metadata.get("/Title", ""),
            "author": metadata.get("/Author", ""),
            "subject": metadata.get("/Subject", ""),
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted
        }

