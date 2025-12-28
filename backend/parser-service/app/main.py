from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime

from app.config import settings
from app.database import get_db, engine, Base
from app.models import ProductMetadata
from app.schemas import BatchParseResponse, ParseResponse, HealthResponse
from app.ocr.tesseract_engine import TesseractOCR
from app.parsers.pdf_parser import PDFParser
from app.parsers.html_parser import HTMLParser
from app.parsers.image_parser import ImageParser
from app.extractors.barcode_extractor import BarcodeExtractor
from app.extractors.text_cleaner import TextCleaner
from app.extractors.ner_extractor import NERExtractor
from app.utils.file_handler import FileHandler

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Parser Service",
    description="Service d'extraction et parsing de données produits",
    version=settings.API_VERSION
)

# Initialiser les services
ocr = TesseractOCR()
pdf_parser = PDFParser()
html_parser = HTMLParser()
image_parser = ImageParser()
barcode_extractor = BarcodeExtractor()
text_cleaner = TextCleaner()
ner_extractor = NERExtractor()  # Modèle NER pour extraction avancée d'ingrédients

# Créer le dossier d'upload
FileHandler.ensure_upload_dir()


@app.post("/product/parse", response_model=BatchParseResponse)
async def parse_products(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Parse un lot de fichiers produits"""
    results = []
    successful = 0
    failed = 0
    
    for file in files:
        file_path = None
        try:
            # Valider le format
            if not FileHandler.is_supported_format(file.filename):
                raise ValueError(f"Format non supporté: {FileHandler.get_file_extension(file.filename)}")
            
            # Sauvegarder temporairement
            file_path = await FileHandler.save_file_async(file)
            
            # Valider la taille
            if not FileHandler.validate_file_size(file_path):
                raise ValueError(f"Fichier trop volumineux (max {settings.MAX_FILE_SIZE / 1024 / 1024}MB)")
            
            # Parser selon le type
            file_ext = FileHandler.get_file_extension(file.filename)
            parsed_data = {}
            
            if file_ext == 'pdf':
                parsed_data = pdf_parser.parse(file_path)
            elif file_ext in ['html', 'htm']:
                parsed_data = html_parser.parse(file_path)
            elif file_ext in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
                parsed_data = image_parser.parse(file_path)
            else:
                raise ValueError(f"Type de fichier non géré: {file_ext}")
            
            # Extraire informations structurées
            text = parsed_data.get("text", "")
            product_name = parsed_data.get("product_name") or text_cleaner.extract_product_name(text)
            
            # Utiliser le modèle NER pour extraction avancée d'ingrédients
            ingredients_ner = ner_extractor.extract_ingredients_as_text(text)
            # Fallback sur extraction basique si NER ne trouve rien
            ingredients = parsed_data.get("ingredients_raw") or ingredients_ner or text_cleaner.extract_ingredients(text)
            
            packaging = parsed_data.get("packaging_info") or text_cleaner.extract_packaging_info(text)
            
            # GTIN
            gtin = parsed_data.get("gtin")
            if not gtin and text:
                gtin = barcode_extractor.extract_from_text(text)
            
            # Nettoyer le texte
            cleaned_text = text_cleaner.clean(text)
            
            # Sauvegarder en DB
            product = ProductMetadata(
                gtin=gtin,
                product_name=product_name,
                ingredients_raw=ingredients,
                packaging_info=packaging,
                filename=file.filename,
                file_type=file_ext,
                file_size=FileHandler.get_file_size(file_path),
                ocr_text=cleaned_text,
                ocr_confidence=parsed_data.get("confidence", 0.0),
                raw_data=parsed_data
            )
            
            db.add(product)
            db.commit()
            db.refresh(product)
            
            results.append(ParseResponse(
                product_id=product.id,
                gtin=product.gtin,
                product_name=product.product_name,
                ingredients_raw=product.ingredients_raw or "",
                packaging_info=product.packaging_info,
                metadata={
                    "filename": product.filename,
                    "confidence": product.ocr_confidence,
                    "file_type": product.file_type,
                    "file_size": product.file_size,
                    "method": parsed_data.get("method", "unknown")
                }
            ))
            
            successful += 1
            
        except Exception as e:
            failed += 1
            print(f"Error parsing {file.filename}: {str(e)}")
        finally:
            # Nettoyer le fichier temporaire
            if file_path and os.path.exists(file_path):
                FileHandler.delete_file(file_path)
    
    return BatchParseResponse(
        status="completed",
        total_files=len(files),
        successful=successful,
        failed=failed,
        products=results
    )


@app.post("/product/parse/single", response_model=ParseResponse)
async def parse_single_product(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Parse un seul fichier produit"""
    file_path = None
    try:
        # Valider le format
        if not FileHandler.is_supported_format(file.filename):
            raise HTTPException(status_code=400, detail=f"Format non supporté: {FileHandler.get_file_extension(file.filename)}")
        
        # Sauvegarder temporairement
        file_path = await FileHandler.save_file_async(file)
        
        # Valider la taille
        if not FileHandler.validate_file_size(file_path):
            raise HTTPException(status_code=400, detail=f"Fichier trop volumineux (max {settings.MAX_FILE_SIZE / 1024 / 1024}MB)")
        
        # Parser selon le type
        file_ext = FileHandler.get_file_extension(file.filename)
        parsed_data = {}
        
        if file_ext == 'pdf':
            parsed_data = pdf_parser.parse(file_path)
        elif file_ext in ['html', 'htm']:
            parsed_data = html_parser.parse(file_path)
        elif file_ext in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
            parsed_data = image_parser.parse(file_path)
        else:
            raise HTTPException(status_code=400, detail=f"Type de fichier non géré: {file_ext}")
        
        # Extraire informations structurées
        text = parsed_data.get("text", "")
        confidence = parsed_data.get("confidence", 0.0)
        
        # Vérifier que du texte a été extrait
        if not text or not text.strip():
            error_msg = (
                f"Aucun texte extrait de l'image '{file.filename}'. "
                f"Confiance OCR: {confidence:.2%}. "
                "Causes possibles: image sans texte visible, qualité d'image insuffisante, "
                "ou erreur OCR. Veuillez utiliser une image avec du texte clairement visible."
            )
            print(f"ERROR: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        product_name = parsed_data.get("product_name") or text_cleaner.extract_product_name(text)
        
        # Utiliser le modèle NER pour extraction avancée d'ingrédients
        ingredients_ner = ner_extractor.extract_ingredients_as_text(text)
        # Fallback sur extraction basique si NER ne trouve rien
        ingredients = parsed_data.get("ingredients_raw") or ingredients_ner or text_cleaner.extract_ingredients(text)
        
        packaging = parsed_data.get("packaging_info") or text_cleaner.extract_packaging_info(text)
        
        # GTIN
        gtin = parsed_data.get("gtin")
        if not gtin and text:
            gtin = barcode_extractor.extract_from_text(text)
        
        # Nettoyer le texte
        cleaned_text = text_cleaner.clean(text)
        
        # Log pour débogage
        print(f"Parser: Texte brut extrait: {len(text)} caracteres")
        print(f"Parser: Texte nettoye: {len(cleaned_text)} caracteres")
        print(f"Parser: Ingredients extraits: {ingredients[:100] if ingredients else 'AUCUN'}")
        print(f"Parser: Confiance OCR: {confidence:.2%}")
        
        # Sauvegarder en DB
        product = ProductMetadata(
            gtin=gtin,
            product_name=product_name,
            ingredients_raw=ingredients,
            packaging_info=packaging,
            filename=file.filename,
            file_type=file_ext,
            file_size=FileHandler.get_file_size(file_path),
            ocr_text=cleaned_text,
            ocr_confidence=parsed_data.get("confidence", 0.0),
            raw_data=parsed_data
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        return ParseResponse(
            product_id=product.id,
            gtin=product.gtin,
            product_name=product.product_name,
            ingredients_raw=product.ingredients_raw or "",
            packaging_info=product.packaging_info,
            metadata={
                "filename": product.filename,
                "confidence": product.ocr_confidence,
                "file_type": product.file_type,
                "file_size": product.file_size,
                "method": parsed_data.get("method", "unknown")
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Erreur lors du parsing: {str(e)}")
        print(f"📋 Traceback complet:\n{error_trace}")
        raise HTTPException(status_code=500, detail=f"Erreur lors du parsing: {str(e)}")
    finally:
        # Nettoyer le fichier temporaire
        if file_path and os.path.exists(file_path):
            FileHandler.delete_file(file_path)


@app.get("/product/{product_id}", response_model=ParseResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Récupère un produit parsé par son ID"""
    product = db.query(ProductMetadata).filter(ProductMetadata.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    return ParseResponse(
        product_id=product.id,
        gtin=product.gtin,
        product_name=product.product_name,
        ingredients_raw=product.ingredients_raw or "",
        packaging_info=product.packaging_info,
        metadata={
            "filename": product.filename,
            "confidence": product.ocr_confidence,
            "file_type": product.file_type,
            "file_size": product.file_size,
            "created_at": product.created_at.isoformat() if product.created_at else None
        }
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="parser-service",
        timestamp=datetime.now()
    )


@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "service": "Parser Service",
        "version": settings.API_VERSION,
        "status": "running",
        "features": {
            "ocr": "Tesseract OCR (images, PDF)",
            "barcode": "GTIN extraction",
            "ner": "spaCy NER model (ingredients extraction)",
            "parsers": ["PDF", "HTML", "Images"]
        }
    }


@app.get("/model/info")
async def get_model_info():
    """Retourne les informations sur le modèle NER"""
    return ner_extractor.get_model_info()


@app.post("/ingredients/extract")
async def extract_ingredients_endpoint(text: str):
    """
    Extrait les ingrédients d'un texte avec le modèle NER
    
    Args:
        text: Texte contenant les ingrédients
        
    Returns:
        Liste des ingrédients extraits avec métadonnées
    """
    ingredients = ner_extractor.extract_ingredients(text)
    ingredients_text = ner_extractor.extract_ingredients_as_text(text)
    
    return {
        "text": text,
        "ingredients": ingredients,
        "ingredients_text": ingredients_text,
        "count": len(ingredients)
    }

