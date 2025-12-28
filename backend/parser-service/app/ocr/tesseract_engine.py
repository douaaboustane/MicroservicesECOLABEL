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
            import os
            if not os.path.exists(image_path):
                raise ValueError(f"Image introuvable: {image_path}")
            
            # Vérifier la taille de l'image
            from PIL import Image as PILImage
            img_pil = PILImage.open(image_path)
            width, height = img_pil.size
            print(f"OCR: Image size: {width}x{height} pixels")
            
            # Preprocessing
            preprocessed = self.preprocessor.preprocess(image_path)
            print(f"OCR: Preprocessing terminé")
            
            # Essayer différents modes PSM (Page Segmentation Mode) pour mieux détecter tout le texte
            # PSM 6 = Assume a single uniform block of text
            # PSM 11 = Sparse text. Find as much text as possible in no particular order
            # PSM 12 = Sparse text with OSD
            psm_modes = [6, 11, 12, 3]  # Essayer plusieurs modes
            best_text = ""
            best_confidence = 0.0
            best_psm = 6
            
            for psm in psm_modes:
                try:
                    # OCR avec data (texte + confidence)
                    config = f'--psm {psm}'
                    data = pytesseract.image_to_data(
                        preprocessed,
                        lang=self.lang,
                        config=config,
                        output_type=pytesseract.Output.DICT
                    )
                    
                    # Calcul confidence moyenne
                    confidences = [int(conf) for conf in data['conf'] if conf != '-1']
                    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                    
                    # Extraction texte avec ce mode
                    text = pytesseract.image_to_string(preprocessed, lang=self.lang, config=config)
                    text_cleaned = text.strip()
                    
                    # Garder le meilleur résultat (plus de texte ou meilleure confiance)
                    if len(text_cleaned) > len(best_text) or (len(text_cleaned) == len(best_text) and avg_confidence > best_confidence):
                        best_text = text_cleaned
                        best_confidence = avg_confidence
                        best_psm = psm
                        print(f"OCR: Mode PSM {psm} - {len(text_cleaned)} caracteres, confiance: {avg_confidence:.2f}%")
                except Exception as e:
                    print(f"OCR: Erreur avec PSM {psm}: {e}")
                    continue
            
            text_cleaned = best_text
            avg_confidence = best_confidence
            print(f"OCR: Meilleur resultat avec PSM {best_psm}: {len(text_cleaned)} caracteres")
            
            # Si peu de texte extrait, essayer avec différentes langues
            if len(text_cleaned) < 50:  # Si moins de 50 caractères, essayer d'autres langues
                print(f"OCR: Peu de texte extrait ({len(text_cleaned)} caracteres), essai avec langues alternatives...")
                
                # Essayer sans langue spécifique avec PSM 11 (sparse text)
                try:
                    text = pytesseract.image_to_string(preprocessed, lang=None, config='--psm 11')
                    alt_text = text.strip()
                    if len(alt_text) > len(text_cleaned):
                        text_cleaned = alt_text
                        avg_confidence = 0.7  # Estimation
                        print(f"OCR: Plus de texte trouve sans langue specifique (PSM 11): {len(alt_text)} caracteres")
                except:
                    pass
                
                # Si toujours peu, essayer avec anglais seulement
                if len(text_cleaned) < 50 and 'eng' not in self.lang:
                    try:
                        text = pytesseract.image_to_string(preprocessed, lang='eng', config='--psm 11')
                        alt_text = text.strip()
                        if len(alt_text) > len(text_cleaned):
                            text_cleaned = alt_text
                            avg_confidence = 0.7  # Estimation
                            print(f"OCR: Plus de texte trouve avec anglais seulement (PSM 11): {len(alt_text)} caracteres")
                    except:
                        pass
            
            print(f"OCR: Texte extrait: {len(text_cleaned)} caracteres, confiance: {avg_confidence:.2f}%")
            if text_cleaned:
                print(f"OCR: Apercu texte: {text_cleaned[:100]}...")
            else:
                print(f"OCR: ATTENTION - Aucun texte extrait de l'image")
                print(f"OCR: Nombre de mots detectes: {len([w for w in data.get('text', []) if w.strip()])}")
                print(f"OCR: Taille image: {width}x{height} pixels")
                print(f"OCR: Langue utilisee: {self.lang}")
            
            return text_cleaned, avg_confidence / 100
        except Exception as e:
            import traceback
            print(f"OCR ERROR: {str(e)}")
            print(f"OCR TRACEBACK: {traceback.format_exc()}")
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

