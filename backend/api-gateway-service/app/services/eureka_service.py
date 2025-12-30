"""
Service Eureka pour la découverte de services
"""
import py_eureka_client.eureka_client as eureka_client
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class EurekaDiscovery:
    """Gestion de la découverte de services via Eureka"""
    
    @staticmethod
    async def get_service_url(service_name: str) -> str:
        """
        Récupère l'URL d'un service depuis Eureka
        
        Args:
            service_name: Nom du service dans Eureka
            
        Returns:
            URL du service (ex: http://parser-service:8001)
        """
        try:
            # Essayer de récupérer l'instance depuis Eureka
            instances = await eureka_client.get_applications()
            
            # Chercher le service dans les applications enregistrées
            if instances and hasattr(instances, 'applications'):
                for app in instances.applications:
                    if app.name.upper() == service_name.upper():
                        if app.instances and len(app.instances) > 0:
                            instance = app.instances[0]
                            # Gérer différents formats d'instance
                            port = instance.port.port if hasattr(instance.port, 'port') else (instance.port if isinstance(instance.port, int) else 8000)
                            ip = instance.ipAddr if hasattr(instance, 'ipAddr') else (instance.hostName if hasattr(instance, 'hostName') else 'localhost')
                            return f"http://{ip}:{port}"
            
            # Fallback: utiliser les URLs par défaut si Eureka n'est pas disponible
            logger.warning(f"Service {service_name} non trouvé dans Eureka, utilisation de l'URL par défaut")
            return _get_default_url(service_name)
            
        except Exception as e:
            logger.warning(f"Erreur lors de la découverte Eureka: {str(e)}, utilisation de l'URL par défaut")
            return _get_default_url(service_name)


def _get_default_url(service_name: str) -> str:
    """Retourne l'URL par défaut d'un service"""
    default_urls = {
        "PARSER-SERVICE": settings.PARSER_SERVICE_URL,
        "NLP-SERVICE": settings.NLP_SERVICE_URL,
        "LCA-SERVICE": settings.LCA_SERVICE_URL,
        "SCORING-SERVICE": settings.SCORING_SERVICE_URL,
    }
    return default_urls.get(service_name.upper(), f"http://{service_name.lower()}:8000")

