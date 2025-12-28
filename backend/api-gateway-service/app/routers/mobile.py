"""
Routes pour le frontend mobile
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Job, JobStatus, User
from app.services.orchestrator import Orchestrator
from app.services.job_manager import JobManager
from app.utils.dependencies import get_optional_user
from app import schemas

router = APIRouter(prefix="/mobile", tags=["Mobile"])

orchestrator = Orchestrator()
job_manager = JobManager()


@router.post("/products/scan", response_model=schemas.ScanJobResponse)
async def create_scan_job(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    """
    Crée un nouveau job de scan de produit
    
    Le traitement se fait de manière asynchrone :
    1. OCR (Parser Service)
    2. Extraction ingrédients (NLP Service)
    3. Calcul impacts (LCA Service)
    4. Calcul score (Scoring Service)
    
    Note: L'authentification est optionnelle. Si un token est fourni,
    le job sera associé à l'utilisateur.
    """
    try:
        # Lire le fichier
        image_data = await file.read()
        
        # Créer le job (avec user_id si authentifié)
        user_id = user.id if user else None
        job = job_manager.create_job(db, user_id=user_id)
        
        # Lancer le traitement de manière asynchrone
        background_tasks.add_task(
            orchestrator.process_product_scan,
            job, image_data, file.filename, db
        )
        
        return schemas.ScanJobResponse(
            job_id=job.id,
            status=job.status.value,
            created_at=job.created_at
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du job: {str(e)}"
        )


@router.get("/products/scan/{job_id}/status", response_model=schemas.JobStatusResponse)
async def get_job_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Récupère le statut d'un job
    
    Utilisé par le frontend pour le polling
    """
    job = job_manager.get_job(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} non trouvé"
        )
    
    response_data = {
        "job_id": job.id,
        "status": job.status.value,
        "progress": job.progress,
        "current_step": job.current_step,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat() if job.updated_at else None
    }
    
    # Si terminé, inclure le résultat
    if job.status == JobStatus.DONE and job.result:
        response_data["result"] = job.result
    
    # Si erreur, inclure le message
    if job.status == JobStatus.ERROR:
        response_data["error"] = job.error_message
    
    return response_data

