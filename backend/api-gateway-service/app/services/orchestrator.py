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
            
            # Extraire le texte depuis différents champs possibles
            ingredients_text = parser_result.get("ingredients_raw", "") or ""
            
            # Vérifier aussi dans metadata si disponible (le Parser Service stocke ocr_text dans metadata)
            metadata = parser_result.get("metadata", {})
            if not ingredients_text and metadata:
                # Le Parser Service ne retourne pas directement ocr_text, mais on peut vérifier
                # Si ingredients_raw est vide, on essaie de continuer quand même avec un texte vide
                pass
            
            # Vérifier la confiance OCR
            ocr_confidence = metadata.get("confidence", 0.0) if metadata else 0.0
            
            # Si pas de texte extrait
            if not ingredients_text or not ingredients_text.strip():
                error_msg = (
                    f"Aucun texte extrait de l'image '{filename}'. "
                    f"Confiance OCR: {ocr_confidence:.2%}. "
                    "Causes possibles : image sans texte visible, qualité d'image insuffisante, ou erreur OCR. "
                    "Veuillez utiliser une image avec du texte clairement visible (étiquette de produit avec liste d'ingrédients)."
                )
                raise ValueError(error_msg)
            
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
            # Le NLP Service retourne entities_normalized (liste de NormalizedEntity)
            # On filtre pour ne garder que les INGREDIENT (pas les ALLERGEN, QUANTITY, etc.)
            ingredients_for_lca = []
            
            # Utiliser entities_normalized si disponible, sinon entities
            entities_list = nlp_result.get("entities_normalized", []) or nlp_result.get("entities", [])
            
            print(f"🔍 NLP Result: {len(entities_list)} entités trouvées")
            print(f"🔍 Structure NLP: {list(nlp_result.keys())}")
            
            for entity in entities_list:
                if not isinstance(entity, dict):
                    continue
                
                # Filtrer uniquement les INGREDIENT
                label = entity.get("label", "").upper()
                if label != "INGREDIENT":
                    continue
                
                # Extraire le nom de l'ingrédient
                ing_name = entity.get("text", "") or entity.get("normalized_name", "")
                
                # Ignorer les ingrédients sans nom
                if not ing_name or not ing_name.strip():
                    continue
                
                ing_dict = {
                    "name": ing_name.strip(),  # Obligatoire, ne doit pas être vide
                    "normalized_name": entity.get("normalized_name"),
                    "agribalyse_code": entity.get("agribalyse_code"),
                    "quantity_percentage": None  # TODO: extraire depuis quantity si disponible
                }
                
                ingredients_for_lca.append(ing_dict)
                print(f"✅ Ingrédient préparé pour LCA: {ing_dict}")
            
            # Vérifier qu'on a au moins un ingrédient
            if not ingredients_for_lca:
                print(f"❌ Aucun ingrédient valide. Entités disponibles: {[e.get('label') for e in entities_list if isinstance(e, dict)]}")
                raise ValueError("Aucun ingrédient valide extrait pour le calcul ACV")
            
            # ============================================
            # ÉTAPE 3: LCA SERVICE (Calcul impacts)
            # ============================================
            self.job_manager.update_status(
                db, job.id, JobStatus.ACV, progress=60,
                current_step="Calcul des impacts environnementaux (ACV)"
            )
            
            # Extraire packaging depuis NLP
            # Le LCA Service requiert que packaging.type soit une string non vide si packaging est fourni
            packaging = None
            if nlp_result.get("packaging"):
                packaging_info = nlp_result["packaging"]
                if isinstance(packaging_info, dict):
                    packaging_type = packaging_info.get("type")
                    # Ne créer packaging que si type est valide
                    if packaging_type and isinstance(packaging_type, str) and packaging_type.strip():
                        # Convertir weight si disponible (peut être en g ou kg)
                        weight_g = packaging_info.get("weight_g")
                        if not weight_g and packaging_info.get("weight"):
                            weight = packaging_info.get("weight")
                            weight_unit = packaging_info.get("weight_unit", "g")
                            if weight_unit == "kg":
                                weight_g = weight * 1000 if weight else None
                            else:
                                weight_g = weight
                        
                        packaging = {
                            "type": packaging_type.strip(),  # Obligatoire, ne doit pas être vide
                            "weight_g": weight_g,
                            "recyclable": packaging_info.get("recyclable", False)
                        }
            
            print(f"📤 Envoi au LCA Service: {len(ingredients_for_lca)} ingrédients, packaging={packaging is not None}")
            print(f"📤 Payload LCA: ingredients={ingredients_for_lca[:2]}...")  # Afficher les 2 premiers
            
            lca_result = await self.client.call_lca_service(
                ingredients=ingredients_for_lca,
                packaging=packaging,  # None si pas de packaging valide
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

