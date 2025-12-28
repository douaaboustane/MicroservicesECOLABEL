"""
Dépendances FastAPI pour l'authentification
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import User
from app.services.auth_service import AuthService

# Security scheme pour Swagger
# - security_required : pour les routes qui nécessitent obligatoirement un token
# - security_optional : pour les routes où l'auth est optionnelle
security_required = HTTPBearer(auto_error=True)
security_optional = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_required),
    db: Session = Depends(get_db)
) -> User:
    """
    Dépendance pour récupérer l'utilisateur actuel depuis le token JWT
    
    Requiert un token valide. Lance une exception 401 si le token est manquant ou invalide.
    
    Utilisation:
        @router.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"user_id": user.id}
    """
    auth_service = AuthService()
    
    # Extraire le token (credentials est garanti d'exister grâce à security_required)
    token = credentials.credentials
    
    # Vérifier le token
    user_id = auth_service.verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Récupérer l'utilisateur
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    return user


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dépendance optionnelle pour récupérer l'utilisateur si un token est fourni
    
    Utilisation:
        @router.get("/optional")
        async def optional_route(user: Optional[User] = Depends(get_optional_user)):
            if user:
                return {"user_id": user.id}
            return {"message": "Non authentifié"}
    """
    if not credentials:
        return None
    
    try:
        auth_service = AuthService()
        token = credentials.credentials
        user_id = auth_service.verify_token(token)
        
        if not user_id:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except Exception:
        return None


def get_token_from_header(
    authorization: Optional[str] = None
) -> Optional[str]:
    """
    Extrait le token JWT depuis le header Authorization
    
    Format attendu: "Bearer <token>"
    """
    if not authorization:
        return None
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        return token
    except ValueError:
        return None

