"""
API FastAPI pour le service Scoring
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.config import settings
from app.database import get_db, engine, Base
from app import schemas
from app.services.scoring_service import ScoringService

# Créer les tables
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser le service Scoring
scoring_service = ScoringService()


@app.on_event("startup")
async def startup_event():
    """Événement au démarrage"""
    print("\n" + "=" * 80)
    print(" " * 20 + "⭐ SCORING SERVICE")
    print("=" * 80)
    print(f"📦 Version: {settings.API_VERSION}")
    print(f"🌐 Port: {settings.PORT}")
    print(f"🤖 Classification Model: {'✅ Chargé' if scoring_service.models.classifier_loaded else '⚠️  Non entraîné'}")
    print(f"📊 Regression Model: {'✅ Chargé' if scoring_service.models.regressor_loaded else '⚠️  Non entraîné'}")
    print("=" * 80 + "\n")


@app.get("/", tags=["Root"])
async def root():
    """Endpoint racine"""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running"
    }


@app.post("/score/calculate", response_model=schemas.ScoreResponse, tags=["Scoring"])
async def calculate_score(
    request: schemas.ScoreRequest,
    method: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Calcule le score écologique (A-E) à partir des données LCA et NLP.
    
    Méthodes disponibles:
    - **classification**: Prédit directement A-E avec le modèle de classification
    - **regression**: Prédit score 0-100 puis convertit en A-E
    - **hybrid**: Combine les deux méthodes (recommandé)
    """
    try:
        # Utiliser la méthode spécifiée ou celle de la requête
        method_to_use = method or request.method or "hybrid"
        
        # Calculer le score
        result = scoring_service.calculate_score(request, method=method_to_use)
        
        # Sauvegarder dans l'historique (optionnel)
        # TODO: Implémenter la sauvegarde en DB
        
        return result
    
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Modèle non entraîné: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du calcul du score: {str(e)}"
        )


@app.get("/score/calculate/classification", response_model=schemas.ScoreResponse, tags=["Scoring"])
async def calculate_score_classification(
    request: schemas.ScoreRequest,
    db: Session = Depends(get_db)
):
    """Calcule le score avec la méthode de classification uniquement"""
    return await calculate_score(request, method="classification", db=db)


@app.get("/score/calculate/regression", response_model=schemas.ScoreResponse, tags=["Scoring"])
async def calculate_score_regression(
    request: schemas.ScoreRequest,
    db: Session = Depends(get_db)
):
    """Calcule le score avec la méthode de régression uniquement"""
    return await calculate_score(request, method="regression", db=db)


@app.get("/score/models/info", tags=["Models"])
async def get_models_info():
    """Retourne les informations sur les modèles chargés"""
    return {
        "classification": {
            "loaded": scoring_service.models.classifier_loaded,
            "type": "RandomForestClassifier",
            "path": settings.CLASSIFICATION_MODEL_PATH
        },
        "regression": {
            "loaded": scoring_service.models.regressor_loaded,
            "type": "RandomForestRegressor",
            "path": settings.REGRESSION_MODEL_PATH
        },
        "features": {
            "count": len(scoring_service.feature_extractor.get_feature_names()),
            "names": scoring_service.feature_extractor.get_feature_names()
        }
    }


@app.get("/health", response_model=schemas.HealthResponse, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    Vérifie l'état de santé du service.
    """
    # Vérifier la connexion DB
    db_connected = True
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_connected = False
        print(f"⚠️  Erreur connexion DB: {e}")
    
    # État global
    is_healthy = (
        (scoring_service.models.classifier_loaded or scoring_service.models.regressor_loaded)
        and db_connected
    )
    
    return schemas.HealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        service=settings.API_TITLE,
        version=settings.API_VERSION,
        classification_model_loaded=scoring_service.models.classifier_loaded,
        regression_model_loaded=scoring_service.models.regressor_loaded,
        timestamp=datetime.now()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )

