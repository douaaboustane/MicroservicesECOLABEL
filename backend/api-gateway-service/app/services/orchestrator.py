"""
Orchestrateur du workflow de traitement
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import Job, JobStatus
from app.services.client_service import MicroserviceClient
from app.services.job_manager import JobManager


class Orchestrator:
    """Orchestre le workflow complet de traitement"""
    
    def __init__(self):
        self.client = MicroserviceClient()
        self.job_manager = JobManager()
    
    async def process_product_scan(
        self,
        job: Job,
        image_file: bytes,
        filename: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Traite un scan de produit de bout en bout
        
        Workflow:
        1. Parser (OCR) → 2. NLP → 3. LCA → 4. Scoring → 5. Résultat
        """
        try:
            # ============================================
            # ÉTAPE 1: PARSER SERVICE (OCR + Extraction)
            # ============================================
            self.job_manager.update_status(
                db, job.id, JobStatus.OCR, progress=10,
                current_step="Extraction du texte (OCR)"
            )
            
            parser_result = await self.client.call_parser_service(image_file, filename)
            job.parser_result = parser_result
            db.commit()
            
            ingredients_text = (
                parser_result.get("ingredients_raw") or
                parser_result.get("ocr_text", "")
            )
            
            if not ingredients_text:
                raise ValueError("Aucun texte extrait de l'image")
            
            # ============================================
            # ÉTAPE 2: NLP SERVICE (Extraction ingrédients)
            # ============================================
            self.job_manager.update_status(
                db, job.id, JobStatus.NLP, progress=40,
                current_step="Extraction des ingrédients (NLP)"
            )
            
            nlp_result = await self.client.call_nlp_service(ingredients_text)
            job.nlp_result = nlp_result
            db.commit()
            
            # Préparer les ingrédients pour LCA
            ingredients_for_lca = []
            for ing in nlp_result.get("ingredients", []):
                ing_dict = {
                    "name": ing.get("text", "") if isinstance(ing, dict) else str(ing),
                    "normalized_name": None,
                    "agribalyse_code": None,
                    "quantity_percentage": None
                }
                
                # Extraire les infos normalisées si disponibles
                if isinstance(ing, dict) and "normalized" in ing:
                    normalized = ing["normalized"]
                    if isinstance(normalized, dict):
                        ing_dict["normalized_name"] = normalized.get("name")
                        ing_dict["agribalyse_code"] = normalized.get("agribalyse_code")
                
                ingredients_for_lca.append(ing_dict)
            
            # ============================================
            # ÉTAPE 3: LCA SERVICE (Calcul impacts)
            # ============================================
            self.job_manager.update_status(
                db, job.id, JobStatus.ACV, progress=60,
                current_step="Calcul des impacts environnementaux (ACV)"
            )
            
            # Extraire packaging depuis NLP
            packaging = None
            if nlp_result.get("packaging"):
                packaging_info = nlp_result["packaging"]
                if isinstance(packaging_info, dict):
                    packaging = {
                        "type": packaging_info.get("type"),
                        "weight_g": None,
                        "recyclable": packaging_info.get("recyclable", False)
                    }
            
            lca_result = await self.client.call_lca_service(
                ingredients=ingredients_for_lca,
                packaging=packaging,
                product_weight_kg=1.0  # Par défaut
            )
            job.lca_result = lca_result
            db.commit()
            
            # ============================================
            # ÉTAPE 4: SCORING SERVICE (Calcul score)
            # ============================================
            self.job_manager.update_status(
                db, job.id, JobStatus.SCORE, progress=80,
                current_step="Calcul du score écologique"
            )
            
            scoring_result = await self.client.call_scoring_service(
                lca_data=lca_result,
                nlp_data=nlp_result,
                method="hybrid"
            )
            job.scoring_result = scoring_result
            db.commit()
            
            # ============================================
            # ÉTAPE 5: AGRÉGER LE RÉSULTAT FINAL
            # ============================================
            total_impacts = lca_result.get("total_impacts", {})
            
            final_result = {
                "score_letter": scoring_result.get("score_letter", "C"),
                "score_value": scoring_result.get("score_numeric", 50.0),
                "confidence": scoring_result.get("confidence"),
                "acv_data": {
                    "co2_kg": total_impacts.get("co2_kg", 0),
                    "water_liters": total_impacts.get("water_m3", 0) * 1000,
                    "energy_mj": total_impacts.get("energy_mj", 0)
                },
                "ingredients": [
                    ing.get("text", "") if isinstance(ing, dict) else str(ing)
                    for ing in nlp_result.get("ingredients", [])
                ],
                "allergens": [
                    allergen.get("text", "") if isinstance(allergen, dict) else str(allergen)
                    for allergen in nlp_result.get("allergens", [])
                ],
                "labels": nlp_result.get("labels", []),
                "breakdown": lca_result.get("breakdown", {})
            }
            
            job.result = final_result
            self.job_manager.update_status(
                db, job.id, JobStatus.DONE, progress=100,
                current_step="Analyse terminée"
            )
            db.commit()
            
            return final_result
        
        except Exception as e:
            # En cas d'erreur
            error_msg = str(e)
            self.job_manager.update_status(
                db, job.id, JobStatus.ERROR, progress=0,
                current_step=f"Erreur: {error_msg}"
            )
            job.error_message = error_msg
            db.commit()
            raise

