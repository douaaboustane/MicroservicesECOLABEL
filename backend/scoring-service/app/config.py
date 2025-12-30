"""
Configuration du service Scoring
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration du service"""
    
    # API
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "Scoring Service"
    API_DESCRIPTION: str = "Service de calcul de score écologique (A-E) avec modèles ML"
    
    # Database
    DATABASE_URL: str = "postgresql://ecolabel:ecolabel123@scoring-db:5432/scoring"
    
    # ML Models
    CLASSIFICATION_MODEL_PATH: str = "app/models/classification_model.pkl"
    REGRESSION_MODEL_PATH: str = "app/models/regression_model.pkl"
    
    # Model Training (si entraînement à la volée)
    TRAIN_ON_STARTUP: bool = False
    TRAINING_DATA_PATH: str = "app/data/training_data.csv"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8005
    
    # Eureka Service Discovery
    EUREKA_SERVER_URL: str = "http://eureka-server:8761/eureka"
    EUREKA_APP_NAME: str = "SCORING-SERVICE"
    EUREKA_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

