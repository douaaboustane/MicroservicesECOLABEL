"""
Configuration du service API Gateway
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration du service"""
    
    # API
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "API Gateway"
    API_DESCRIPTION: str = "Point d'entrée unique pour le frontend - Orchestration des microservices"
    
    # Database
    DATABASE_URL: str = "postgresql://ecolabel:ecolabel123@api-db:5432/ecolabel_api"
    
    # Microservices URLs (dans le réseau Docker)
    PARSER_SERVICE_URL: str = "http://parser-service:8001"
    NLP_SERVICE_URL: str = "http://nlp-service:8003"
    LCA_SERVICE_URL: str = "http://lca-service:8004"
    SCORING_SERVICE_URL: str = "http://scoring-service:8005"
    
    # Auth
    JWT_SECRET: str = "your-secret-key-change-in-production-please-use-strong-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # RabbitMQ
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "ecolabel"
    RABBITMQ_PASSWORD: str = "ecolabel123"
    RABBITMQ_VHOST: str = "/"
    
    # Queues
    QUEUE_PRODUCT_SCAN: str = "product_scan"
    QUEUE_OCR: str = "ocr"
    QUEUE_NLP: str = "nlp"
    QUEUE_LCA: str = "lca"
    QUEUE_SCORING: str = "scoring"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

