"""
Routes d'authentification
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.auth_service import AuthService
from app.utils.dependencies import get_current_user
from app import schemas
import uuid

router = APIRouter(prefix="/mobile/auth", tags=["Auth"])

auth_service = AuthService()


@router.post("/login", response_model=schemas.AuthResponse)
async def login(
    request: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """Connexion utilisateur"""
    user = auth_service.authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    token = auth_service.create_access_token(user.id)
    
    return schemas.AuthResponse(
        user=schemas.UserResponse(
            id=user.id,
            email=user.email,
            name=user.name
        ),
        token=token
    )


@router.post("/signup", response_model=schemas.AuthResponse)
async def signup(
    request: schemas.SignupRequest,
    db: Session = Depends(get_db)
):
    """Inscription utilisateur"""
    # Vérifier si l'email existe déjà
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé"
        )
    
    # Créer l'utilisateur
    user = User(
        id=str(uuid.uuid4()),
        email=request.email,
        password_hash=auth_service.hash_password(request.password),
        name=request.name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = auth_service.create_access_token(user.id)
    
    return schemas.AuthResponse(
        user=schemas.UserResponse(
            id=user.id,
            email=user.email,
            name=user.name
        ),
        token=token
    )


@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_info(
    user: User = Depends(get_current_user)
):
    """Récupère l'utilisateur actuel depuis le token JWT"""
    return schemas.UserResponse(
        id=user.id,
        email=user.email,
        name=user.name
    )


@router.patch("/me", response_model=schemas.UserResponse)
async def update_current_user(
    updates: dict,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Met à jour le profil de l'utilisateur actuel"""
    if "name" in updates:
        user.name = updates["name"]
    
    db.commit()
    db.refresh(user)
    
    return schemas.UserResponse(
        id=user.id,
        email=user.email,
        name=user.name
    )


@router.post("/social", response_model=schemas.AuthResponse)
async def social_auth(
    request: schemas.SocialAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Authentification sociale (Google, Apple, Microsoft)
    
    Si l'utilisateur existe déjà (même email), on le connecte.
    Sinon, on crée un nouveau compte.
    """
    # Chercher un utilisateur existant avec cet email
    existing_user = db.query(User).filter(User.email == request.email).first()
    
    if existing_user:
        # Utilisateur existe déjà, on le connecte
        # Note: En production, vous devriez vérifier le token/idToken du provider
        user = existing_user
    else:
        # Créer un nouvel utilisateur
        # Pour l'auth sociale, on génère un password hash aléatoire
        # (l'utilisateur ne pourra pas se connecter avec email/password)
        # Bcrypt limite à 72 bytes, donc on génère un password de 50 caractères
        import secrets
        random_password = secrets.token_urlsafe(50)[:50]  # Limiter à 50 caractères pour être sûr
        
        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            password_hash=auth_service.hash_password(random_password),
            name=request.name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Créer le token JWT
    token = auth_service.create_access_token(user.id)
    
    return schemas.AuthResponse(
        user=schemas.UserResponse(
            id=user.id,
            email=user.email,
            name=user.name
        ),
        token=token
    )

