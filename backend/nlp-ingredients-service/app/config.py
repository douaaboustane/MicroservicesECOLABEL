"""
Configuration du service NLP-Ingredients
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuration du service"""
    
    # API
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "NLP-Ingredients Service"
    API_DESCRIPTION: str = "Service d'extraction et normalisation des ingrédients"
    
    # Database
    DATABASE_URL: str = "postgresql://ecolabel:ecolabel123@nlp-db:5432/nlp_ingredients"
    
    # NLP Models
    NER_MODEL_PATH: str = "app/models/ner_ingredients_v3"
    SPACY_MODEL: str = "fr_core_news_md"
    
    # Taxonomies
    TAXONOMY_FILE: str = "app/data/taxonomies/ingredients.json"
    AGRIBALYSE_FILE: str = "app/data/taxonomies/agribalyse_processed.csv"
    ECOINVENT_FILE: str = "app/data/taxonomies/ecoinvent.csv"
    
    # Matching
    FUZZY_THRESHOLD: int = 80  # Score minimum pour fuzzy matching
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8003
    
    # Eureka Service Discovery
    EUREKA_SERVER_URL: str = "http://eureka-server:8761/eureka"
    EUREKA_APP_NAME: str = "NLP-SERVICE"
    EUREKA_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

