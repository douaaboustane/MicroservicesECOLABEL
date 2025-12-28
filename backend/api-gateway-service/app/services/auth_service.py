"""
Service d'authentification
"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
from typing import Optional
from app.models import User
from app.config import settings


class AuthService:
    """Service d'authentification"""
    
    def hash_password(self, password: str) -> str:
        """Hash un mot de passe avec bcrypt"""
        # Bcrypt has a 72-byte limit, truncate if necessary
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Vérifie un mot de passe avec bcrypt"""
        try:
            # Bcrypt has a 72-byte limit, truncate if necessary
            password_bytes = plain_password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False
    
    def create_access_token(self, user_id: str) -> str:
        """Crée un token JWT"""
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        payload = {
            "sub": user_id,
            "exp": expire
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    def verify_token(self, token: str) -> Optional[str]:
        """Vérifie et décode un token JWT"""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            return payload.get("sub")
        except JWTError:
            return None
    
    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        """Authentifie un utilisateur"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user

