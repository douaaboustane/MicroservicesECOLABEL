"""
Schémas Pydantic pour validation des requêtes/réponses
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime


# ============================================
# SCAN / JOBS
# ============================================

class ScanJobResponse(BaseModel):
    """Réponse lors de la création d'un job de scan"""
    job_id: str
    status: str
    created_at: datetime


class JobStatusResponse(BaseModel):
    """Réponse pour le statut d'un job"""
    job_id: str
    status: str
    progress: int
    current_step: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ============================================
# AUTHENTIFICATION
# ============================================

class LoginRequest(BaseModel):
    """Requête de connexion"""
    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    """Requête d'inscription"""
    email: EmailStr
    password: str
    name: Optional[str] = None


class UserResponse(BaseModel):
    """Réponse utilisateur"""
    id: str
    email: str
    name: Optional[str] = None


class AuthResponse(BaseModel):
    """Réponse d'authentification"""
    user: UserResponse
    token: str


# ============================================
# HEALTH
# ============================================

class HealthResponse(BaseModel):
    """Réponse de health check"""
    status: str
    service: str
    version: str
    database_connected: bool
    timestamp: datetime

