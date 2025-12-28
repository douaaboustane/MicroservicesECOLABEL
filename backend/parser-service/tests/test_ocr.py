import pytest
import os
import numpy as np
from PIL import Image
from app.ocr.tesseract_engine import TesseractOCR
from app.ocr.preprocessor import ImagePreprocessor


@pytest.fixture
def sample_image_path(tmp_path):
    """Créer une image de test"""
    # Créer une image simple avec du texte
    img = Image.new('RGB', (200, 100), color='white')
    # Note: Pour un vrai test, il faudrait ajouter du texte avec PIL ou utiliser une image réelle
    img_path = tmp_path / "test_image.png"
    img.save(img_path)
    return str(img_path)


def test_tesseract_ocr_initialization():
    """Test initialisation OCR"""
    ocr = TesseractOCR()
    assert ocr is not None
    assert ocr.lang is not None


def test_preprocessor_initialization():
    """Test initialisation preprocessor"""
    preprocessor = ImagePreprocessor()
    assert preprocessor is not None


@pytest.mark.skipif(not os.path.exists("/usr/bin/tesseract"), reason="Tesseract not installed")
def test_ocr_extract_text(sample_image_path):
    """Test extraction texte OCR"""
    ocr = TesseractOCR()
    text, confidence = ocr.extract_text(sample_image_path)
    assert isinstance(text, str)
    assert 0 <= confidence <= 1


def test_preprocessor_preprocess(sample_image_path):
    """Test preprocessing image"""
    preprocessor = ImagePreprocessor()
    processed = preprocessor.preprocess(sample_image_path)
    assert processed is not None
    assert isinstance(processed, np.ndarray)

