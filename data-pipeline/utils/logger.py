"""
Logger utilitaire pour le pipeline
"""
from loguru import logger
import sys
from pathlib import Path


def setup_logger(name: str, log_file: str = "outputs/logs/pipeline.log"):
    """Configure le logger pour un module"""
    
    # Créer le dossier de logs si nécessaire
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configuration
    logger.remove()  # Supprimer le handler par défaut
    
    # Console
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # Fichier
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="1 week",
        compression="zip"
    )
    
    return logger


# Logger global
log = setup_logger("pipeline")

