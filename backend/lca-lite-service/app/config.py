"""
Configuration du service LCALite
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration du service"""
    
    # API
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "LCA-Lite Service"
    API_DESCRIPTION: str = "Service de calcul d'Analyse du Cycle de Vie simplifiée"
    
    # Database
    DATABASE_URL: str = "postgresql://ecolabel:ecolabel123@postgres:5432/lca_lite"
    
    # Data files
    AGRIBALYSE_FILE: str = "app/data/agribalyse_processed.csv"
    TRANSPORT_FACTORS_FILE: str = "app/data/transport_factors.json"
    PACKAGING_IMPACTS_FILE: str = "app/data/packaging_impacts.json"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8004
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

