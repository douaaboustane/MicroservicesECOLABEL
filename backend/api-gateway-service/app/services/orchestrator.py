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
    
    def _calculate_fallback_score(
        self,
        lca_data: Dict[str, Any],
        nlp_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calcule un score de fallback basé sur les données LCA quand les modèles ML ne sont pas disponibles
        
        Score basé sur:
        - CO2: < 1kg = A, < 2kg = B, < 4kg = C, < 6kg = D, >= 6kg = E
        - Eau: < 100L = A, < 500L = B, < 1000L = C, < 2000L = D, >= 2000L = E
        - Labels bio/équitable: bonus
        """
        total_impacts = lca_data.get("total_impacts", {})
        co2_kg = total_impacts.get("co2_kg", 0)
        water_m3 = total_impacts.get("water_m3", 0)
        water_liters = water_m3 * 1000
        
        # Calculer score basé sur CO2
        if co2_kg < 1.0:
            co2_score = 90
        elif co2_kg < 2.0:
            co2_score = 75
        elif co2_kg < 4.0:
            co2_score = 60
        elif co2_kg < 6.0:
            co2_score = 40
        else:
            co2_score = 20
        
        # Calculer score basé sur eau
        if water_liters < 100:
            water_score = 90
        elif water_liters < 500:
            water_score = 75
        elif water_liters < 1000:
            water_score = 60
        elif water_liters < 2000:
            water_score = 40
        else:
            water_score = 20
        
        # Score moyen
        base_score = (co2_score + water_score) / 2
        
        # Bonus pour labels
        labels = nlp_data.get("labels", [])
        labels_str = [str(label).lower() for label in labels]
        if any("bio" in label for label in labels_str):
            base_score += 5
        if any("fair" in label or "équitable" in label for label in labels_str):
            base_score += 5
        
        # Clamp entre 0 et 100
        final_score = max(0, min(100, base_score))
        
        # Convertir en lettre
        if final_score >= 80:
            letter = "A"
        elif final_score >= 60:
            letter = "B"
        elif final_score >= 40:
            letter = "C"
        elif final_score >= 20:
            letter = "D"
        else:
            letter = "E"
        
        return {
            "score_letter": letter,
            "score_numeric": round(final_score, 1),
            "confidence": 0.7,  # Confiance moyenne pour fallback
            "method": "fallback",
            "details": {
                "note": "Score calculé avec méthode de fallback (modèles ML non disponibles)",
                "co2_impact": co2_kg,
                "water_impact": water_liters
            }
        }
    
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
            # Le NLP Service retourne entities_normalized (liste de NormalizedEntity) et entities (liste brute)
            ingredients_for_lca = []
            
            # Combiner entities_normalized et entities pour avoir toutes les entités
            entities_normalized = nlp_result.get("entities_normalized", []) or []
            entities_raw = nlp_result.get("entities", []) or []
            
            # Utiliser entities_normalized en priorité, puis entities si normalisées vides
            all_entities = entities_normalized if entities_normalized else entities_raw
            
            print(f"NLP Result: {len(entities_normalized)} entités normalisées, {len(entities_raw)} entités brutes", flush=True)
            print(f"Structure NLP: {list(nlp_result.keys())}", flush=True)
            print(f"Total entities to process: {len(all_entities)}", flush=True)
            
            # Afficher toutes les entités pour debug
            all_labels = {}
            for entity in all_entities:
                if isinstance(entity, dict):
                    label = entity.get("label", "UNKNOWN")
                    all_labels[label] = all_labels.get(label, 0) + 1
            print(f"Labels trouvés: {all_labels}", flush=True)
            
            # Essayer d'abord de trouver les INGREDIENT (avec différentes variantes de casse)
            for entity in all_entities:
                if not isinstance(entity, dict):
                    continue
                
                label = entity.get("label", "").upper()
                
                # Filtrer uniquement les INGREDIENT (accepter différentes variantes)
                if label not in ["INGREDIENT", "INGREDIENTS"]:
                    continue
                
                # Extraire le nom de l'ingrédient (priorité: normalized_name, puis text)
                ing_name = entity.get("normalized_name", "") or entity.get("text", "")
                
                # Ignorer les ingrédients sans nom
                if not ing_name or not ing_name.strip():
                    continue
                
                # Ignorer les entités trop courtes (probablement des erreurs)
                if len(ing_name.strip()) < 2:
                    continue
                
                # Construire le dictionnaire en omettant les valeurs None
                ing_dict = {
                    "name": ing_name.strip()  # Obligatoire, ne doit pas être vide
                }
                
                # Ajouter les champs optionnels seulement s'ils ne sont pas None
                if entity.get("normalized_name") and entity.get("normalized_name") != ing_name.strip():
                    ing_dict["normalized_name"] = entity.get("normalized_name")
                if entity.get("agribalyse_code"):
                    ing_dict["agribalyse_code"] = entity.get("agribalyse_code")
                
                ingredients_for_lca.append(ing_dict)
                print(f"Ingredient prepared for LCA: {ing_dict}", flush=True)
            
            # Si aucun INGREDIENT trouvé, utiliser toutes les entités sauf ALLERGEN et QUANTITY
            # (fallback pour les cas où le modèle n'a pas bien labellisé)
            if not ingredients_for_lca:
                print("WARNING: Aucun INGREDIENT trouvé, utilisation de toutes les entités (sauf ALLERGEN/QUANTITY)", flush=True)
                print(f"WARNING: Total entities available: {len(all_entities)}", flush=True)
                print(f"WARNING: All labels: {all_labels}", flush=True)
                
                for entity in all_entities:
                    if not isinstance(entity, dict):
                        continue
                    
                    label = entity.get("label", "").upper()
                    
                    # Exclure ALLERGEN et QUANTITY
                    if label in ["ALLERGEN", "QUANTITY", "QUANTITIES"]:
                        continue
                    
                    # Utiliser toutes les autres entités comme ingrédients potentiels
                    ing_name = entity.get("normalized_name", "") or entity.get("text", "")
                    
                    if not ing_name or not ing_name.strip():
                        continue
                    
                    # Ignorer les entités trop courtes (probablement des erreurs)
                    if len(ing_name.strip()) < 2:
                        continue
                    
                    # Ignorer les entités qui sont clairement des quantités (contiennent des chiffres uniquement)
                    if ing_name.strip().replace(".", "").replace(",", "").isdigit():
                        continue
                    
                    ing_dict = {
                        "name": ing_name.strip()
                    }
                    
                    if entity.get("normalized_name") and entity.get("normalized_name") != ing_name.strip():
                        ing_dict["normalized_name"] = entity.get("normalized_name")
                    if entity.get("agribalyse_code"):
                        ing_dict["agribalyse_code"] = entity.get("agribalyse_code")
                    
                    ingredients_for_lca.append(ing_dict)
                    print(f"Fallback ingredient prepared: {ing_dict} (label: {label})", flush=True)
                
                print(f"WARNING: After fallback, {len(ingredients_for_lca)} ingredients prepared", flush=True)
            
            # Vérifier qu'on a au moins un ingrédient
            if not ingredients_for_lca:
                labels = [e.get('label', 'UNKNOWN') for e in all_entities if isinstance(e, dict)]
                print(f"ERROR: No valid ingredients. Available entities: {labels}", flush=True)
                print(f"ERROR: NLP result keys: {list(nlp_result.keys())}", flush=True)
                print(f"ERROR: Total entities: {len(all_entities)}", flush=True)
                print(f"ERROR: entities_normalized: {len(entities_normalized)}, entities_raw: {len(entities_raw)}", flush=True)
                
                # Si on a du texte mais pas d'entités, essayer d'extraire des mots du texte original
                if ingredients_text and len(ingredients_text.strip()) > 10:
                    print(f"WARNING: Tentative d'extraction manuelle depuis le texte...", flush=True)
                    # Nettoyer le texte (enlever caractères spéciaux, normaliser)
                    import re
                    # Remplacer les caractères spéciaux par des espaces
                    cleaned_text = re.sub(r'[^\w\s]', ' ', ingredients_text)
                    # Extraire les mots (séparés par virgules ou espaces)
                    words = re.split(r'[,;:]\s*|\s+', cleaned_text)
                    
                    # Mots à ignorer
                    stop_words = {
                        'le', 'la', 'les', 'de', 'du', 'des', 'et', 'ou', 'pour', 'avec', 'sans',
                        'en', 'poudre', 'complet', 'complete', 'completes', 'mineraux', 'mineraux',
                        'sel', 'sucre', 'eau', 'eau', 'pate', 'pate', 'pates'
                    }
                    
                    # Extraire les ingrédients potentiels
                    for word in words:
                        cleaned = word.strip('.,;:!?()[]{}').lower().strip()
                        # Ignorer les mots trop courts, les chiffres, et les stop words
                        if (len(cleaned) >= 3 and 
                            not cleaned.isdigit() and 
                            cleaned not in stop_words and
                            not cleaned.replace('.', '').replace(',', '').isdigit()):
                            # Nettoyer encore plus (enlever caractères étranges)
                            cleaned = re.sub(r'[^\w\s-]', '', cleaned).strip()
                            if len(cleaned) >= 3:
                                ingredients_for_lca.append({"name": cleaned})
                                print(f"Manual ingredient extracted: {cleaned}", flush=True)
                                if len(ingredients_for_lca) >= 15:  # Augmenter la limite
                                    break
                
                if not ingredients_for_lca:
                    raise ValueError(f"Aucun ingrédient valide extrait pour le calcul ACV. Entités trouvées: {labels}")
            
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
            packaging_info = nlp_result.get("packaging")
            # Vérifier que packaging_info existe, n'est pas None, et n'est pas un dict vide
            if packaging_info and isinstance(packaging_info, dict) and len(packaging_info) > 0:
                packaging_type = packaging_info.get("type")
                # Ne créer packaging que si type est valide et non vide
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
                    print(f"INFO: Packaging créé: {packaging}", flush=True)
                else:
                    print(f"WARNING: Packaging info exists but type is invalid or empty: {packaging_type}", flush=True)
                    print(f"WARNING: packaging_info = {packaging_info}", flush=True)
            else:
                print(f"INFO: No packaging info in NLP result (packaging_info={packaging_info})", flush=True)
            
            import json
            print(f"Sending to LCA Service: {len(ingredients_for_lca)} ingredients, packaging={packaging is not None}", flush=True)
            print(f"LCA Payload preview: {json.dumps(ingredients_for_lca[:2] if len(ingredients_for_lca) >= 2 else ingredients_for_lca, indent=2, ensure_ascii=False)}", flush=True)
            
            # Vérification finale avant envoi (déjà faite plus haut, mais double vérification)
            if not ingredients_for_lca:
                labels = [e.get('label', 'UNKNOWN') for e in all_entities if isinstance(e, dict)]
                error_msg = f"Aucun ingrédient valide extrait. Entités disponibles: {labels}. NLP keys: {list(nlp_result.keys())}"
                print(f"ERROR: {error_msg}", flush=True)
                raise ValueError(error_msg)
            
            # Vérifier que chaque ingrédient a un nom
            for idx, ing in enumerate(ingredients_for_lca):
                if not ing.get("name") or not ing["name"].strip():
                    error_msg = f"Ingrédient {idx} n'a pas de nom valide: {ing}"
                    print(f"ERROR: {error_msg}", flush=True)
                    raise ValueError(error_msg)
            
            # Log final avant envoi
            import json
            print(f"FINAL PAYLOAD TO LCA: {json.dumps({'ingredients': ingredients_for_lca, 'product_weight_kg': 1.0, 'packaging': packaging if packaging else None}, indent=2, ensure_ascii=False)}", flush=True)
            print(f"Number of ingredients: {len(ingredients_for_lca)}", flush=True)
            print(f"Packaging: {packaging if packaging else 'None'}", flush=True)
            
            if not ingredients_for_lca:
                print(f"ERROR: No ingredients prepared for LCA!", flush=True)
                print(f"NLP entities: {len(all_entities)}", flush=True)
                print(f"Labels found: {all_labels}", flush=True)
                raise ValueError("Aucun ingrédient valide pour le calcul ACV")
            
            # S'assurer que packaging est None si vide ou sans type
            final_packaging = None
            if packaging and isinstance(packaging, dict) and len(packaging) > 0:
                packaging_type = packaging.get("type")
                if packaging_type and isinstance(packaging_type, str) and packaging_type.strip():
                    final_packaging = packaging
                else:
                    print(f"WARNING: Packaging has no valid type, sending None", flush=True)
            
            lca_result = await self.client.call_lca_service(
                ingredients=ingredients_for_lca,
                packaging=final_packaging,
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
            
            # Appeler le scoring service (gère automatiquement le fallback si modèles non disponibles)
            try:
                scoring_result = await self.client.call_scoring_service(
                    lca_data=lca_result,
                    nlp_data=nlp_result,
                    method="hybrid"
                )
            except Exception as scoring_error:
                # Si le scoring service est complètement inaccessible (erreur réseau), utiliser fallback
                print(f"⚠️  Scoring service inaccessible, utilisation d'un score de fallback: {scoring_error}", flush=True)
                scoring_result = self._calculate_fallback_score(lca_result, nlp_result)
            
            job.scoring_result = scoring_result
            db.commit()
            
            # ============================================
            # ÉTAPE 5: AGRÉGER LE RÉSULTAT FINAL
            # ============================================
            total_impacts = lca_result.get("total_impacts", {})
            
            # Extraire les ingrédients depuis entities_normalized ou entities
            # Le NLP service retourne entities_normalized (liste de NormalizedEntity) et entities (liste brute)
            entities_normalized = nlp_result.get("entities_normalized", []) or []
            entities_raw = nlp_result.get("entities", []) or []
            all_entities = entities_normalized if entities_normalized else entities_raw
            
            # Extraire les ingrédients (label INGREDIENT ou INGREDIENTS)
            ingredients_list = []
            for entity in all_entities:
                if not isinstance(entity, dict):
                    continue
                label = entity.get("label", "").upper()
                if label in ["INGREDIENT", "INGREDIENTS"]:
                    # Utiliser normalized_name si disponible, sinon text
                    ing_name = entity.get("normalized_name", "") or entity.get("text", "")
                    if ing_name and ing_name.strip():
                        ingredients_list.append(ing_name.strip())
            
            # Si aucun ingrédient trouvé avec label INGREDIENT, utiliser toutes les entités sauf ALLERGEN et QUANTITY
            if not ingredients_list:
                for entity in all_entities:
                    if not isinstance(entity, dict):
                        continue
                    label = entity.get("label", "").upper()
                    if label not in ["ALLERGEN", "QUANTITY", "QUANTITIES"]:
                        ing_name = entity.get("normalized_name", "") or entity.get("text", "")
                        if ing_name and ing_name.strip() and len(ing_name.strip()) >= 2:
                            # Ignorer les entités qui sont clairement des quantités
                            if not ing_name.strip().replace(".", "").replace(",", "").isdigit():
                                ingredients_list.append(ing_name.strip())
            
            # Extraire les allergènes
            allergens_list = []
            for entity in all_entities:
                if not isinstance(entity, dict):
                    continue
                label = entity.get("label", "").upper()
                if label in ["ALLERGEN", "ALLERGENS"]:
                    allergen_name = entity.get("normalized_name", "") or entity.get("text", "")
                    if allergen_name and allergen_name.strip():
                        allergens_list.append(allergen_name.strip())
            
            # Extraire les labels
            labels_list = []
            labels_data = nlp_result.get("labels", [])
            for label in labels_data:
                if isinstance(label, dict):
                    labels_list.append(label.get("label_name", "") or label.get("label_type", ""))
                elif isinstance(label, str):
                    labels_list.append(label)
            
            final_result = {
                "score_letter": scoring_result.get("score_letter", "C"),
                "score_value": scoring_result.get("score_numeric", 50.0),
                "confidence": scoring_result.get("confidence"),
                "acv_data": {
                    "co2_kg": total_impacts.get("co2_kg", 0),
                    "water_liters": total_impacts.get("water_m3", 0) * 1000,
                    "energy_mj": total_impacts.get("energy_mj", 0)
                },
                "ingredients": ingredients_list,
                "allergens": allergens_list,
                "labels": labels_list,
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
            # En cas d'erreur, sauvegarder les résultats partiels avant de lever l'exception
            error_msg = str(e)
            print(f"ERROR in orchestrator: {error_msg}", flush=True)
            import traceback
            print(f"Traceback: {traceback.format_exc()}", flush=True)
            
            # S'assurer que tous les résultats partiels sont sauvegardés
            try:
                db.refresh(job)
                # Les résultats partiels (parser_result, nlp_result, lca_result) 
                # sont déjà sauvegardés dans les étapes précédentes
                # On s'assure juste qu'ils sont bien commités
                db.commit()
            except Exception as commit_error:
                print(f"ERROR committing partial results: {commit_error}", flush=True)
            
            # Mettre à jour le statut d'erreur
            self.job_manager.update_status(
                db, job.id, JobStatus.ERROR, progress=0,
                current_step=f"Erreur: {error_msg}"
            )
            job.error_message = error_msg
            db.commit()
            
            # Ne pas lever l'exception pour que les résultats partiels soient accessibles
            # Le statut ERROR indique déjà qu'il y a eu un problème

