import pytesseract
from PIL import Image
from app.config import settings
from app.ocr.preprocessor import ImagePreprocessor
import cv2
import numpy as np
from typing import Tuple


pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


class TesseractOCR:
    def __init__(self):
        self.lang = settings.TESSERACT_LANG
        self.preprocessor = ImagePreprocessor()
    
    def extract_text(self, image_path: str) -> Tuple[str, float]:
        """
        Extrait le texte d'une image avec Tesseract
        Returns: (text, confidence)
        """
        try:
            # Preprocessing
            preprocessed = self.preprocessor.preprocess(image_path)
            
            # OCR avec data (texte + confidence)
            data = pytesseract.image_to_data(
                preprocessed,
                lang=self.lang,
                output_type=pytesseract.Output.DICT
            )
            
            # Calcul confidence moyenne
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Extraction texte
            text = pytesseract.image_to_string(preprocessed, lang=self.lang)
            
            return text.strip(), avg_confidence / 100
        except Exception as e:
            raise Exception(f"Erreur OCR: {str(e)}")
    
    def extract_with_boxes(self, image_path: str) -> dict:
        """
        Extrait le texte avec les coordonnées des boîtes
        Returns: dict avec text, boxes, confidences
        """
        preprocessed = self.preprocessor.preprocess(image_path)
        
        data = pytesseract.image_to_data(
            preprocessed,
            lang=self.lang,
            output_type=pytesseract.Output.DICT
        )
        
        boxes = []
        texts = []
        confidences = []
        
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > 0:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                text = data['text'][i].strip()
                conf = int(data['conf'][i])
                
                if text:
                    boxes.append((x, y, w, h))
                    texts.append(text)
                    confidences.append(conf)
        
        return {
            "text": " ".join(texts),
            "boxes": boxes,
            "confidences": confidences,
            "avg_confidence": sum(confidences) / len(confidences) if confidences else 0
        }
    
    def _preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """Améliore la qualité OCR (méthode legacy, utilise maintenant preprocessor)"""
        # Cette méthode n'est plus utilisée, on utilise directement preprocessor.preprocess()
        return img

