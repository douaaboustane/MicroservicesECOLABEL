"""
API Gateway - Point d'entrée unique pour le frontend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import mobile, auth
from sqlalchemy import text

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# CORS pour Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(mobile.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup_event():
    """Événement au démarrage"""
    print("\n" + "=" * 80)
    print(" " * 25 + "🚀 API GATEWAY")
    print("=" * 80)
    print(f"📦 Version: {settings.API_VERSION}")
    print(f"🌐 Port: {settings.PORT}")
    print(f"🔗 Parser Service: {settings.PARSER_SERVICE_URL}")
    print(f"🧠 NLP Service: {settings.NLP_SERVICE_URL}")
    print(f"🌍 LCA Service: {settings.LCA_SERVICE_URL}")
    print(f"⭐ Scoring Service: {settings.SCORING_SERVICE_URL}")
    print("=" * 80 + "\n")


@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", response_model=dict, tags=["Health"])
async def health_check():
    """Health check"""
    from datetime import datetime
    from app.database import SessionLocal
    
    db_connected = True
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        db_connected = False
        print(f"⚠️  Erreur connexion DB: {e}")
    
    return {
        "status": "healthy" if db_connected else "unhealthy",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "database_connected": db_connected,
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )

