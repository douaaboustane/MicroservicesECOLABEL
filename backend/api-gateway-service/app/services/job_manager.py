"""
Gestionnaire de jobs
"""
from sqlalchemy.orm import Session
from typing import Optional
from app.models import Job, JobStatus
from datetime import datetime
import uuid


class JobManager:
    """Gère la création et le suivi des jobs"""
    
    def create_job(
        self,
        db: Session,
        user_id: Optional[str] = None
    ) -> Job:
        """Crée un nouveau job"""
        job = Job(
            id=str(uuid.uuid4()),
            user_id=user_id,
            status=JobStatus.PENDING,
            progress=0
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    
    def update_status(
        self,
        db: Session,
        job_id: str,
        status: JobStatus,
        progress: Optional[int] = None,
        current_step: Optional[str] = None
    ):
        """Met à jour le statut d'un job"""
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError(f"Job {job_id} non trouvé")
        
        job.status = status
        if progress is not None:
            job.progress = progress
        if current_step:
            job.current_step = current_step
        job.updated_at = datetime.utcnow()
        
        if status == JobStatus.DONE:
            job.completed_at = datetime.utcnow()
        
        db.commit()
    
    def get_job(self, db: Session, job_id: str) -> Optional[Job]:
        """Récupère un job par son ID"""
        return db.query(Job).filter(Job.id == job_id).first()

