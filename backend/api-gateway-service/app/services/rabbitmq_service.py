"""
Service RabbitMQ pour la gestion des messages asynchrones
"""
import pika
import json
import base64
from typing import Dict, Any, Optional, Callable
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class RabbitMQService:
    """Service pour publier et consommer des messages RabbitMQ"""
    
    def __init__(self):
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        self._connect()
    
    def _connect(self):
        """Établit la connexion à RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(
                settings.RABBITMQ_USER,
                settings.RABBITMQ_PASSWORD
            )
            parameters = pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                virtual_host=settings.RABBITMQ_VHOST,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Déclarer les queues
            self._declare_queues()
            
            logger.info("✅ Connexion RabbitMQ établie")
        except Exception as e:
            logger.error(f"❌ Erreur connexion RabbitMQ: {e}")
            raise
    
    def _declare_queues(self):
        """Déclare toutes les queues nécessaires"""
        queues = [
            settings.QUEUE_PRODUCT_SCAN,
            settings.QUEUE_OCR,
            settings.QUEUE_NLP,
            settings.QUEUE_LCA,
            settings.QUEUE_SCORING
        ]
        
        for queue in queues:
            # Queue durable pour survivre aux redémarrages
            self.channel.queue_declare(queue=queue, durable=True)
            logger.info(f"✅ Queue déclarée: {queue}")
    
    def publish_message(
        self,
        queue: str,
        message: Dict[str, Any],
        priority: int = 0
    ):
        """
        Publie un message dans une queue
        
        Args:
            queue: Nom de la queue
            message: Dictionnaire à sérialiser en JSON
            priority: Priorité du message (0-255)
        """
        try:
            if not self.connection or self.connection.is_closed:
                self._connect()
            
            # Sérialiser le message
            body = json.dumps(message, ensure_ascii=False)
            
            # Publier avec persistence
            self.channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistence
                    priority=priority
                )
            )
            
            logger.info(f"📤 Message publié dans {queue}: {message.get('job_id', 'N/A')}")
        except Exception as e:
            logger.error(f"❌ Erreur publication message: {e}")
            raise
    
    def publish_scan_job(
        self,
        job_id: str,
        image_data: bytes,
        filename: str,
        user_id: Optional[str] = None
    ):
        """
        Publie un job de scan de produit
        
        Args:
            job_id: ID du job
            image_data: Données de l'image (bytes)
            filename: Nom du fichier
            user_id: ID de l'utilisateur (optionnel)
        """
        # Encoder l'image en base64 pour le transport
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        message = {
            "job_id": job_id,
            "filename": filename,
            "image_data": image_base64,
            "user_id": user_id
        }
        
        self.publish_message(settings.QUEUE_PRODUCT_SCAN, message)
    
    def consume_messages(
        self,
        queue: str,
        callback: Callable[[Dict[str, Any]], None],
        auto_ack: bool = False
    ):
        """
        Consomme des messages d'une queue
        
        Args:
            queue: Nom de la queue
            callback: Fonction à appeler pour chaque message
            auto_ack: Si True, les messages sont automatiquement acquittés
        """
        try:
            if not self.connection or self.connection.is_closed:
                self._connect()
            
            def on_message(ch, method, properties, body):
                try:
                    # Désérialiser le message
                    message = json.loads(body.decode('utf-8'))
                    
                    # Appeler le callback
                    callback(message)
                    
                    # Acquitter le message
                    if not auto_ack:
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    logger.error(f"❌ Erreur traitement message: {e}")
                    if not auto_ack:
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
            # Configurer QoS pour ne traiter qu'un message à la fois
            self.channel.basic_qos(prefetch_count=1)
            
            # Démarrer la consommation
            self.channel.basic_consume(
                queue=queue,
                on_message_callback=on_message,
                auto_ack=auto_ack
            )
            
            logger.info(f"👂 Écoute de la queue: {queue}")
            self.channel.start_consuming()
            
        except Exception as e:
            logger.error(f"❌ Erreur consommation messages: {e}")
            raise
    
    def close(self):
        """Ferme la connexion RabbitMQ"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("✅ Connexion RabbitMQ fermée")
        except Exception as e:
            logger.error(f"❌ Erreur fermeture connexion: {e}")


# Instance globale
rabbitmq_service = RabbitMQService()

