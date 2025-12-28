import cv2
import numpy as np
from typing import Tuple


class ImagePreprocessor:
    """Préprocessing d'images pour améliorer la qualité OCR"""
    
    @staticmethod
    def preprocess(image_path: str) -> np.ndarray:
        """
        Applique un preprocessing complet sur l'image
        Returns: Image binarisée optimisée pour OCR
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Impossible de charger l'image: {image_path}")
        
        # Conversion en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Réduction du bruit
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        
        # Amélioration du contraste (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # Binarisation adaptive
        binary = cv2.adaptiveThreshold(
            enhanced, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        return binary
    
    @staticmethod
    def preprocess_for_barcode(image_path: str) -> np.ndarray:
        """
        Preprocessing spécifique pour la détection de codes-barres
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Impossible de charger l'image: {image_path}")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Amélioration du contraste pour codes-barres
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        return enhanced
    
    @staticmethod
    def rotate_if_needed(image_path: str) -> Tuple[np.ndarray, float]:
        """
        Détecte et corrige la rotation de l'image si nécessaire
        Returns: (image_corrigée, angle_rotation)
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Impossible de charger l'image: {image_path}")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Détection des contours pour estimer l'orientation
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
        
        if lines is not None and len(lines) > 0:
            angles = []
            for rho, theta in lines[:5]:  # Prendre les 5 premières lignes
                angle = np.degrees(theta) - 90
                angles.append(angle)
            
            avg_angle = np.mean(angles)
            if abs(avg_angle) > 0.5:  # Seuil de 0.5 degrés
                # Rotation
                (h, w) = img.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, avg_angle, 1.0)
                rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                return rotated, avg_angle
        
        return img, 0.0

