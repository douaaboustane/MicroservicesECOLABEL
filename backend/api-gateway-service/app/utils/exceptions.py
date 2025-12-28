"""
Exceptions personnalisées
"""
from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    """Exception pour les erreurs d'authentification"""
    def __init__(self, detail: str = "Authentification requise"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(HTTPException):
    """Exception pour les erreurs d'autorisation"""
    def __init__(self, detail: str = "Accès non autorisé"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

