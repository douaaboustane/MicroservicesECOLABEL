from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ecolabel"
    
    # Tesseract
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    TESSERACT_LANG: str = "fra+eng"
    
    # File Storage
    UPLOAD_DIR: str = "/tmp/uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # API
    API_VERSION: str = "v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # Eureka Service Discovery
    EUREKA_SERVER_URL: str = "http://eureka-server:8761/eureka"
    EUREKA_APP_NAME: str = "PARSER-SERVICE"
    EUREKA_ENABLED: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()

