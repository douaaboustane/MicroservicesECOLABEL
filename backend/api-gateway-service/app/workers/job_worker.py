"""
Worker pour traiter les jobs de scan de produit via RabbitMQ
"""
import base64
import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.rabbitmq_service import RabbitMQService
from app.services.orchestrator import Orchestrator
from app.models import Job, JobStatus
from app.services.job_manager import JobManager

logger = logging.getLogger(__name__)

orchestrator = Orchestrator()
job_manager = JobManager()
rabbitmq_service = RabbitMQService()


def process_scan_job(message: Dict[str, Any]):
    """
    Traite un job de scan de produit
    
    Args:
        message: Message RabbitMQ contenant job_id, image_data, filename, user_id
    """
    job_id = message.get("job_id")
    filename = message.get("filename")
    image_base64 = message.get("image_data")
    user_id = message.get("user_id")
    
    print(f"\n{'='*80}", flush=True)
    print(f"🔄 WORKER: Traitement job {job_id} (fichier: {filename})", flush=True)
    print(f"{'='*80}\n", flush=True)
    
    # Créer une session DB pour ce worker
    db: Session = SessionLocal()
    
    try:
        # Récupérer le job
        job = job_manager.get_job(db, job_id)
        if not job:
            print(f"❌ WORKER: Job {job_id} non trouvé", flush=True)
            return
        
        print(f"✅ WORKER: Job {job_id} trouvé, status: {job.status.value}", flush=True)
        
        # Décoder l'image
        image_data = base64.b64decode(image_base64)
        print(f"✅ WORKER: Image décodée, taille: {len(image_data)} bytes", flush=True)
        
        # Traiter le job (orchestrator gère tout le workflow)
        import asyncio
        print(f"🔄 WORKER: Démarrage du traitement asynchrone...", flush=True)
        result = asyncio.run(
            orchestrator.process_product_scan(
                job=job,
                image_file=image_data,
                filename=filename,
                db=db
            )
        )
        
        print(f"\n{'='*80}", flush=True)
        print(f"✅ WORKER: Job {job_id} terminé avec succès", flush=True)
        print(f"{'='*80}\n", flush=True)
        
    except Exception as e:
        import traceback
        print(f"\n{'='*80}", flush=True)
        print(f"❌ WORKER: Erreur traitement job {job_id}: {e}", flush=True)
        print(f"Traceback: {traceback.format_exc()}", flush=True)
        print(f"{'='*80}\n", flush=True)
        
        try:
            # Marquer le job comme ERROR
            job = job_manager.get_job(db, job_id)
            if job:
                job_manager.update_status(
                    db, job_id, JobStatus.ERROR, progress=0,
                    current_step=f"Erreur: {str(e)}"
                )
                job.error_message = str(e)
                db.commit()
                print(f"✅ WORKER: Job {job_id} marqué comme ERROR", flush=True)
        except Exception as db_error:
            print(f"❌ WORKER: Erreur mise à jour job: {db_error}", flush=True)
    finally:
        db.close()
        print(f"✅ WORKER: Session DB fermée pour job {job_id}\n", flush=True)


def start_worker():
    """Démarre le worker pour consommer les messages"""
    logger.info("🚀 Démarrage du worker de traitement de jobs")
    
    try:
        rabbitmq_service.consume_messages(
            queue="product_scan",
            callback=process_scan_job,
            auto_ack=False
        )
    except KeyboardInterrupt:
        logger.info("⏹️  Arrêt du worker")
        rabbitmq_service.close()
    except Exception as e:
        logger.error(f"❌ Erreur worker: {e}")
        import traceback
        logger.error(traceback.format_exc())
        rabbitmq_service.close()


if __name__ == "__main__":
    start_worker()

