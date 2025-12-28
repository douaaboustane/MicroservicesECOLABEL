"""
Tests pour le NER Extractor
"""
import pytest
from app.services.ner_extractor import NERExtractor


@pytest.fixture
def ner_extractor():
    """Fixture pour le NER extractor"""
    return NERExtractor()


def test_ner_extractor_loads(ner_extractor):
    """Test que le modèle NER se charge correctement"""
    assert ner_extractor.loaded is True
    assert ner_extractor.nlp is not None


def test_extract_ingredients(ner_extractor):
    """Test l'extraction d'ingrédients"""
    text = "farine de blé, eau, sel, levure"
    entities, processing_time = ner_extractor.extract(text)
    
    assert len(entities) > 0
    assert processing_time > 0
    assert any(e["label"] == "INGREDIENT" for e in entities)


def test_extract_enumbers(ner_extractor):
    """Test l'extraction d'E-numbers"""
    text = "colorant E150d, conservateur E330"
    entities, _ = ner_extractor.extract(text)
    
    e_numbers = [e for e in entities if "E" in e["text"] and e["text"][1:].isdigit()]
    assert len(e_numbers) >= 2


def test_extract_minerals(ner_extractor):
    """Test l'extraction de minéraux"""
    text = "CALCIUM 55 MAGNESIUM 19 SODIUM 24"
    entities, _ = ner_extractor.extract(text)
    
    minerals = [e for e in entities if e["text"].upper() in ["CALCIUM", "MAGNESIUM", "SODIUM"]]
    assert len(minerals) >= 3


def test_get_model_info(ner_extractor):
    """Test les infos du modèle"""
    info = ner_extractor.get_model_info()
    
    assert info["loaded"] is True
    assert "labels" in info
    assert "INGREDIENT" in info["labels"]
    assert "ALLERGEN" in info["labels"]


def test_get_statistics(ner_extractor):
    """Test le calcul des statistiques"""
    entities = [
        {"label": "INGREDIENT", "text": "farine"},
        {"label": "INGREDIENT", "text": "sucre"},
        {"label": "ALLERGEN", "text": "lait"},
        {"label": "QUANTITY", "text": "50%"}
    ]
    
    stats = ner_extractor.get_statistics(entities)
    
    assert stats["total"] == 4
    assert stats["ingredients"] == 2
    assert stats["allergens"] == 1
    assert stats["quantities"] == 1

