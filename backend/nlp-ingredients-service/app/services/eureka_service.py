"""
Service Eureka pour l'enregistrement et la découverte de services
"""
import py_eureka_client.eureka_client as eureka_client
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class EurekaService:
    """Gestion de l'enregistrement Eureka"""
    
    @staticmethod
    async def register():
        """Enregistre le service auprès d'Eureka"""
        try:
            await eureka_client.init_async(
                eureka_server=settings.EUREKA_SERVER_URL,
                app_name=settings.EUREKA_APP_NAME,
                instance_port=settings.PORT,
                instance_host=settings.HOST,
                instance_ip=settings.HOST,
                renewal_interval_in_secs=30,
                duration_in_secs=90,
                metadata={
                    "management.port": str(settings.PORT),
                    "statusPageUrl": f"http://{settings.HOST}:{settings.PORT}/health",
                    "healthCheckUrl": f"http://{settings.HOST}:{settings.PORT}/health"
                }
            )
            logger.info(f"Service {settings.EUREKA_APP_NAME} enregistré auprès d'Eureka")
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement Eureka: {str(e)}")
            # Ne pas bloquer le démarrage si Eureka n'est pas disponible
            pass
    
    @staticmethod
    async def deregister():
        """Désenregistre le service d'Eureka"""
        try:
            await eureka_client.stop()
            logger.info(f"Service {settings.EUREKA_APP_NAME} désenregistré d'Eureka")
        except Exception as e:
            logger.error(f"Erreur lors du désenregistrement Eureka: {str(e)}")



