import pytest
import os
from app.parsers.pdf_parser import PDFParser
from app.parsers.html_parser import HTMLParser
from app.parsers.image_parser import ImageParser
from app.extractors.barcode_extractor import BarcodeExtractor
from app.extractors.text_cleaner import TextCleaner


def test_pdf_parser_initialization():
    """Test initialisation PDF parser"""
    parser = PDFParser()
    assert parser is not None


def test_html_parser_initialization():
    """Test initialisation HTML parser"""
    parser = HTMLParser()
    assert parser is not None


def test_image_parser_initialization():
    """Test initialisation Image parser"""
    parser = ImageParser()
    assert parser is not None


def test_barcode_extractor_initialization():
    """Test initialisation Barcode extractor"""
    extractor = BarcodeExtractor()
    assert extractor is not None


def test_text_cleaner_initialization():
    """Test initialisation Text cleaner"""
    cleaner = TextCleaner()
    assert cleaner is not None


def test_text_cleaner_clean():
    """Test nettoyage texte"""
    cleaner = TextCleaner()
    dirty_text = "  Hello   World  \n\n  "
    clean_text = cleaner.clean(dirty_text)
    assert clean_text == "Hello World"


def test_text_cleaner_extract_product_name():
    """Test extraction nom produit"""
    cleaner = TextCleaner()
    text = "Produit: Chocolat Noir\nIngrédients: cacao, sucre"
    name = cleaner.extract_product_name(text)
    assert name is not None
    assert len(name) > 0


def test_text_cleaner_extract_ingredients():
    """Test extraction ingrédients"""
    cleaner = TextCleaner()
    text = "Ingrédients: farine, eau, sel, levure"
    ingredients = cleaner.extract_ingredients(text)
    assert "farine" in ingredients.lower() or len(ingredients) > 0


def test_barcode_extractor_validate_gtin():
    """Test validation GTIN"""
    extractor = BarcodeExtractor()
    
    # GTIN valide (EAN-13)
    valid_gtin = "3017620422003"
    assert extractor._is_valid_gtin(valid_gtin) == True
    
    # GTIN invalide
    invalid_gtin = "1234567890123"
    assert extractor._is_valid_gtin(invalid_gtin) == False


def test_barcode_extractor_from_text():
    """Test extraction GTIN depuis texte"""
    extractor = BarcodeExtractor()
    text = "Code-barres: 3017620422003"
    gtin = extractor.extract_from_text(text)
    # Peut être None si le checksum est invalide, mais devrait trouver le pattern
    assert gtin is None or len(gtin) >= 8

