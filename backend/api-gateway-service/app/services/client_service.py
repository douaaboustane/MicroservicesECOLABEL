"""
Client HTTP pour communiquer avec les microservices
"""
import httpx
from typing import Dict, Any, List, Optional
from app.config import settings
from app.services.eureka_service import EurekaDiscovery


class MicroserviceClient:
    """Client HTTP pour communiquer avec les microservices"""
    
    def __init__(self):
        # Utiliser Eureka pour la découverte de services si activé
        self._use_eureka = settings.EUREKA_ENABLED
        self._eureka_discovery = EurekaDiscovery() if self._use_eureka else None
        # URLs par défaut (fallback si Eureka n'est pas disponible)
        self.parser_url = settings.PARSER_SERVICE_URL
        self.nlp_url = settings.NLP_SERVICE_URL
        self.lca_url = settings.LCA_SERVICE_URL
        self.scoring_url = settings.SCORING_SERVICE_URL
    
    async def _get_service_url(self, service_name: str, default_url: str) -> str:
        """Récupère l'URL d'un service depuis Eureka ou utilise l'URL par défaut"""
        if self._use_eureka and self._eureka_discovery:
            try:
                return await self._eureka_discovery.get_service_url(service_name)
            except Exception as e:
                print(f"Warning: Eureka discovery failed for {service_name}, using default URL: {e}")
        return default_url
    
    async def call_parser_service(
        self,
        image_file: bytes,
        filename: str
    ) -> Dict[str, Any]:
        """Appelle le Parser Service pour OCR et extraction"""
        try:
            # Récupérer l'URL depuis Eureka si disponible
            parser_url = await self._get_service_url("PARSER-SERVICE", self.parser_url)
            
            # Déterminer le type MIME basé sur l'extension
            file_ext = filename.split('.')[-1].lower() if '.' in filename else 'jpg'
            mime_type_map = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'bmp': 'image/bmp',
                'tiff': 'image/tiff',
                'pdf': 'application/pdf'
            }
            mime_type = mime_type_map.get(file_ext, 'image/jpeg')
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                files = {"file": (filename, image_file, mime_type)}
                response = await client.post(
                    f"{parser_url}/product/parse/single",
                    files=files
                )
                
                # Si erreur, logger les détails avant de lever l'exception
                if response.status_code != 200:
                    error_detail = response.text
                    print(f"❌ Erreur Parser Service ({response.status_code}): {error_detail}")
                    try:
                        error_json = response.json()
                        error_detail = error_json.get('detail', error_detail)
                    except:
                        pass
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = f"Parser Service error {e.response.status_code}: {e.response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg) from e
        except Exception as e:
            print(f"❌ Erreur lors de l'appel au Parser Service: {str(e)}")
            raise
    
    async def call_nlp_service(
        self,
        ingredients_text: str,
        normalize: bool = True
    ) -> Dict[str, Any]:
        """Appelle le NLP Service pour extraction d'ingrédients"""
        # Récupérer l'URL depuis Eureka si disponible
        nlp_url = await self._get_service_url("NLP-SERVICE", self.nlp_url)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{nlp_url}/nlp/extract",
                json={
                    "text": ingredients_text,
                    "normalize": normalize,
                    "detect_labels": True,
                    "detect_packaging": True,
                    "detect_origin": True
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def call_lca_service(
        self,
        ingredients: List[Dict[str, Any]],
        packaging: Optional[Dict[str, Any]] = None,
        transport: Optional[Dict[str, Any]] = None,
        product_weight_kg: float = 1.0
    ) -> Dict[str, Any]:
        """Appelle le LCA Service pour calcul d'impacts"""
        try:
            # Récupérer l'URL depuis Eureka si disponible
            lca_url = await self._get_service_url("LCA-SERVICE", self.lca_url)
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Nettoyer les ingrédients pour enlever les None explicites
                cleaned_ingredients = []
                for ing in ingredients:
                    cleaned_ing = {k: v for k, v in ing.items() if v is not None}
                    cleaned_ingredients.append(cleaned_ing)
                
                payload = {
                    "ingredients": cleaned_ingredients,
                    "product_weight_kg": product_weight_kg
                }
                # Ne pas envoyer packaging si c'est None ou un dict vide
                if packaging and isinstance(packaging, dict) and packaging.get("type"):
                    # Nettoyer aussi le packaging
                    cleaned_packaging = {k: v for k, v in packaging.items() if v is not None}
                    # S'assurer que type est présent et non vide
                    if cleaned_packaging.get("type"):
                        payload["packaging"] = cleaned_packaging
                if transport and isinstance(transport, dict) and any(transport.values()):
                    cleaned_transport = {k: v for k, v in transport.items() if v is not None}
                    if cleaned_transport:
                        payload["transport"] = cleaned_transport
                
                import json
                payload_str = json.dumps(payload, indent=2, ensure_ascii=False)
                print(f"LCA Request payload: {payload_str}", flush=True)
                
                response = await client.post(
                    f"{lca_url}/lca/calc",
                    json=payload
                )
                
                # Si erreur, logger les détails avant de lever l'exception
                if response.status_code != 200:
                    error_detail = response.text
                    print(f"\n{'='*80}", flush=True)
                    print(f"ERROR LCA Service ({response.status_code})", flush=True)
                    print(f"{'='*80}", flush=True)
                    print(f"Payload envoyé:", flush=True)
                    print(f"{payload_str}", flush=True)
                    print(f"\nRéponse d'erreur: {error_detail}", flush=True)
                    try:
                        error_json = response.json()
                        error_detail = error_json.get('detail', error_detail)
                        if isinstance(error_detail, list):
                            # Erreurs de validation Pydantic - format détaillé
                            print(f"\nErreurs de validation Pydantic:", flush=True)
                            error_messages = []
                            for e in error_detail:
                                if isinstance(e, dict):
                                    loc = e.get('loc', [])
                                    msg = e.get('msg', '')
                                    error_type = e.get('type', '')
                                    error_msg = f"{' -> '.join(str(l) for l in loc)}: {msg} (type: {error_type})"
                                    error_messages.append(error_msg)
                                    print(f"  - {error_msg}", flush=True)
                                else:
                                    error_messages.append(str(e))
                            error_detail = "; ".join(error_messages)
                        print(f"{'='*80}\n", flush=True)
                    except Exception as parse_error:
                        print(f"Impossible de parser l'erreur JSON: {parse_error}", flush=True)
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = f"LCA Service error {e.response.status_code}: {e.response.text}"
            if e.response.status_code == 422:
                try:
                    error_json = e.response.json()
                    detail = error_json.get('detail', 'Validation error')
                    if isinstance(detail, list):
                        detail = "; ".join([str(d) for d in detail])
                    error_msg = f"Erreur de validation LCA Service: {detail}"
                except:
                    pass
            print(f"❌ {error_msg}")
            raise ValueError(error_msg) from e
        except httpx.RequestError as e:
            raise ValueError(f"Erreur de connexion au LCA Service: {str(e)}") from e
        except Exception as e:
            raise ValueError(f"Erreur inattendue lors de l'appel au LCA Service: {str(e)}") from e
    
    async def call_scoring_service(
        self,
        lca_data: Dict[str, Any],
        nlp_data: Dict[str, Any],
        method: str = "hybrid"
    ) -> Dict[str, Any]:
        """Appelle le Scoring Service pour calcul du score"""
        # Récupérer l'URL depuis Eureka si disponible
        scoring_url = await self._get_service_url("SCORING-SERVICE", self.scoring_url)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Préparer les données pour le scoring
            ingredients_list = [
                ing.get("text", "") if isinstance(ing, dict) else str(ing)
                for ing in nlp_data.get("ingredients", [])
            ]
            
            labels_list = nlp_data.get("labels", [])
            packaging_info = nlp_data.get("packaging", {})
            
            response = await client.post(
                f"{scoring_url}/score/calculate",
                json={
                    "lca_data": {
                        "co2_kg": lca_data.get("total_impacts", {}).get("co2_kg", 0),
                        "water_liters": lca_data.get("total_impacts", {}).get("water_m3", 0) * 1000,
                        "energy_mj": lca_data.get("total_impacts", {}).get("energy_mj", 0),
                        "acidification": lca_data.get("total_impacts", {}).get("acidification", 0),
                        "eutrophisation": lca_data.get("total_impacts", {}).get("eutrophisation", 0)
                    },
                    "nlp_data": {
                        "ingredients": ingredients_list,
                        "allergens": [
                            allergen.get("text", "") if isinstance(allergen, dict) else str(allergen)
                            for allergen in nlp_data.get("allergens", [])
                        ],
                        "labels": labels_list,
                        "packaging_type": packaging_info.get("type") if isinstance(packaging_info, dict) else None,
                        "origin_country": nlp_data.get("origin", {}).get("country") if isinstance(nlp_data.get("origin"), dict) else None,
                        "has_bio_label": any("bio" in str(label).lower() for label in labels_list),
                        "has_fair_trade": any("fair" in str(label).lower() or "équitable" in str(label).lower() for label in labels_list),
                        "has_recyclable_packaging": packaging_info.get("recyclable", False) if isinstance(packaging_info, dict) else False,
                        "has_local_origin": nlp_data.get("origin", {}).get("is_local", False) if isinstance(nlp_data.get("origin"), dict) else False,
                        "has_palm_oil": any("palme" in str(ing).lower() for ing in ingredients_list),
                        "has_high_sugar": any("sucre" in str(ing).lower() for ing in ingredients_list),
                        "has_additives": any("e" in str(ing).lower() and str(ing).lower().startswith("e") for ing in ingredients_list)
                    },
                    "method": method
                }
            )
            response.raise_for_status()
            return response.json()

