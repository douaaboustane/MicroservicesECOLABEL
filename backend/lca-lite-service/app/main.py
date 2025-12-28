"""
API FastAPI pour le service LCALite
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from app.config import settings
from app.database import get_db, engine, Base
from app import schemas
from app.services.lca_service import LCAService

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

# Initialiser le service LCA
lca_service = LCAService()


@app.on_event("startup")
async def startup_event():
    """Événement au démarrage"""
    print("\n" + "=" * 80)
    print(" " * 20 + "🌍 LCA-LITE SERVICE")
    print("=" * 80)
    print(f"📦 Version: {settings.API_VERSION}")
    print(f"🌐 Port: {settings.PORT}")
    print(f"✅ Base Agribalyse: {'Chargée' if lca_service.agribalyse_db.loaded else 'Non chargée'}")
    if lca_service.agribalyse_db.loaded:
        print(f"   • Produits: {len(lca_service.agribalyse_db.data) if lca_service.agribalyse_db.data is not None else 0}")
    print("=" * 80 + "\n")


@app.get("/", tags=["Root"])
async def root():
    """Page d'accueil"""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs",
        "agribalyse_loaded": lca_service.agribalyse_db.loaded,
        "endpoints": {
            "calc": "POST /lca/calc",
            "health": "GET /health"
        }
    }


@app.post("/lca/calc", response_model=schemas.LCACalcResponse, tags=["LCA"])
async def calculate_lca(
    request: schemas.LCACalcRequest,
    db: Session = Depends(get_db)
):
    """
    Calcule une Analyse du Cycle de Vie simplifiée pour un produit.
    
    - **ingredients**: Liste des ingrédients avec quantités
    - **packaging**: Informations sur l'emballage
    - **transport**: Informations sur le transport
    - **product_weight_kg**: Poids total du produit
    
    Retourne les impacts environnementaux (CO2, eau, énergie, etc.)
    """
    try:
        result = lca_service.calculate_lca(request)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du calcul ACV: {str(e)}"
        )


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
    is_healthy = lca_service.agribalyse_db.loaded and db_connected
    
    return schemas.HealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        service=settings.API_TITLE,
        version=settings.API_VERSION,
        agribalyse_loaded=lca_service.agribalyse_db.loaded,
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

