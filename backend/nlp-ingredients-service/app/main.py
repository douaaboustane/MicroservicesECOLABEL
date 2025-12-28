"""
API FastAPI pour le service NLP-Ingredients
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import time
from typing import List

from app.config import settings
from app.database import get_db, engine, Base
from app import schemas
from app.services.ner_extractor import NERExtractor
from app.services.normalizer import EntityNormalizer
from app.services.label_detector import LabelDetector
from app.services.taxonomy_loader import TaxonomyLoader
from app.services.packaging_extractor import PackagingExtractor
from app.services.origin_extractor import OriginExtractor

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

# Charger la taxonomie au démarrage
taxonomy_loader = TaxonomyLoader()
taxonomy_data = taxonomy_loader.load_all()

# Initialiser les services avec la taxonomie
ner_extractor = NERExtractor()
entity_normalizer = EntityNormalizer(taxonomy_data=taxonomy_data)
label_detector = LabelDetector()
packaging_extractor = PackagingExtractor()
origin_extractor = OriginExtractor()


@app.on_event("startup")
async def startup_event():
    """Événement au démarrage"""
    print("\n" + "=" * 80)
    print(" " * 20 + "🚀 NLP-INGREDIENTS SERVICE")
    print("=" * 80)
    print(f"📦 Version: {settings.API_VERSION}")
    print(f"🌐 Port: {settings.PORT}")
    print(f"\n🧠 Modèle NER: {'✅ Chargé' if ner_extractor.loaded else '❌ Non chargé'}")
    if ner_extractor.loaded:
        model_info = ner_extractor.get_model_info()
        print(f"   • Modèle: {model_info.get('model_path', 'N/A')}")
        print(f"   • Version: {model_info.get('version', 'N/A')}")
        print(f"   • Labels: {', '.join(model_info.get('labels', []))}")
    
    print(f"\n📚 Taxonomie: {'✅ Chargée' if taxonomy_loader.loaded else '❌ Non chargée'}")
    if taxonomy_loader.loaded:
        stats = taxonomy_loader.get_statistics()
        print(f"   • Total ingrédients: {stats['total']}")
        print(f"   • Allergènes: {stats['allergens']}")
        print(f"   • Avec code Agribalyse: {stats['with_agribalyse_code']}")
        print(f"   • Sources: {', '.join(stats['sources'])}")
    
    print("=" * 80 + "\n")


@app.get("/", tags=["Root"])
async def root():
    """Page d'accueil"""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs",
        "model_loaded": ner_extractor.loaded,
        "taxonomy_loaded": taxonomy_loader.loaded,
        "taxonomy_items": len(taxonomy_data) if taxonomy_data else 0,
        "endpoints": {
            "extract": "POST /nlp/extract",
            "batch": "POST /nlp/extract/batch",
            "model_info": "GET /nlp/model/info",
            "taxonomy_stats": "GET /nlp/taxonomy/stats",
            "health": "GET /health"
        }
    }


@app.post("/nlp/extract", response_model=schemas.ExtractResponse, tags=["NLP"])
async def extract_entities(
    request: schemas.ExtractRequest,
    db: Session = Depends(get_db)
):
    """
    Extrait et normalise les entités d'un texte.
    
    - **text**: Texte à analyser
    - **normalize**: Normaliser les entités (défaut: True)
    - **detect_labels**: Détecter les labels (défaut: True)
    """
    try:
        # 1. Extraction NER
        entities_raw, processing_time_ner = ner_extractor.extract(request.text)
        
        # 2. Normalisation
        entities_normalized = []
        if request.normalize:
            entities_normalized = entity_normalizer.normalize_batch(entities_raw)
        
        # 3. Détection de labels
        labels = []
        if request.detect_labels:
            labels_raw = label_detector.detect(request.text)
            labels = [schemas.Label(**label) for label in labels_raw]
        
        # 4. Détection d'emballage
        packaging = None
        if request.detect_packaging:
            packaging_raw = packaging_extractor.extract(request.text)
            if packaging_raw:
                packaging = schemas.Packaging(**packaging_raw[0])
        
        # 5. Détection de provenance
        origin = None
        if request.detect_origin:
            origin_raw = origin_extractor.extract(request.text)
            if origin_raw:
                # Prendre la première origine détectée
                origin_data = origin_raw[0]
                if "geographic_labels" in origin_data:
                    # Si c'est juste les labels géographiques, chercher une origine
                    for o in origin_raw:
                        if "origin" in o:
                            origin_data = o
                            break
                if "origin" in origin_data:
                    origin = schemas.Origin(**origin_data)
        
        # 6. Statistiques
        stats = ner_extractor.get_statistics(entities_raw)
        confidence = ner_extractor.calculate_confidence(entities_raw)
        
        # 7. Créer la réponse
        response = schemas.ExtractResponse(
            entities=[schemas.Entity(**e) for e in entities_raw],
            entities_normalized=[schemas.NormalizedEntity(**e) for e in entities_normalized],
            labels=labels,
            packaging=packaging,
            origin=origin,
            total_entities=stats["total"],
            total_ingredients=stats["ingredients"],
            total_allergens=stats["allergens"],
            total_quantities=stats["quantities"],
            processing_time_ms=processing_time_ner,
            model_version=ner_extractor.model_version,
            confidence_score=confidence
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'extraction: {str(e)}"
        )


@app.post("/nlp/extract/batch", response_model=schemas.BatchExtractResponse, tags=["NLP"])
async def extract_entities_batch(
    request: schemas.BatchExtractRequest,
    db: Session = Depends(get_db)
):
    """
    Extrait et normalise les entités de plusieurs textes.
    
    - **texts**: Liste de textes à analyser
    - **normalize**: Normaliser les entités (défaut: True)
    - **detect_labels**: Détecter les labels (défaut: True)
    """
    try:
        start_time = time.time()
        results = []
        
        for text in request.texts:
            extract_request = schemas.ExtractRequest(
                text=text,
                normalize=request.normalize,
                detect_labels=request.detect_labels,
                detect_packaging=request.detect_packaging,
                detect_origin=request.detect_origin
            )
            result = await extract_entities(extract_request, db)
            results.append(result)
        
        total_time = (time.time() - start_time) * 1000
        
        return schemas.BatchExtractResponse(
            results=results,
            total_processed=len(results),
            total_time_ms=total_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'extraction batch: {str(e)}"
        )


@app.get("/nlp/model/info", tags=["NLP"])
async def get_model_info():
    """
    Retourne les informations sur le modèle NER chargé.
    """
    return ner_extractor.get_model_info()


@app.get("/nlp/taxonomy/stats", tags=["NLP"])
async def get_taxonomy_stats():
    """
    Retourne les statistiques sur la taxonomie chargée.
    """
    return taxonomy_loader.get_statistics()


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
    is_healthy = ner_extractor.loaded and db_connected
    
    return schemas.HealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        service=settings.API_TITLE,
        version=settings.API_VERSION,
        model_loaded=ner_extractor.loaded,
        database_connected=db_connected,
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

