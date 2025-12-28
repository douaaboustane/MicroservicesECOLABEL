"""
Script de test complet du workflow end-to-end
Teste: OCR -> NLP -> LCA -> Scoring via API Gateway
"""
import requests
import time
import json
import sys
from typing import Optional, Dict, Any

API_GATEWAY_URL = "http://localhost:8000"
TIMEOUT = 30
MAX_POLL_ATTEMPTS = 60  # 2 minutes max (60 * 2s)


class Colors:
    """Couleurs pour le terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Affiche un en-tête"""
    print(f"\n{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")


def print_success(text: str):
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")


def print_error(text: str):
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}[ERROR] {text}{Colors.RESET}")


def print_warning(text: str):
    """Affiche un avertissement"""
    print(f"{Colors.YELLOW}[WARNING] {text}{Colors.RESET}")


def print_info(text: str):
    """Affiche une information"""
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")


def test_api_gateway_health() -> bool:
    """Teste si l'API Gateway est accessible"""
    print_header("TEST 1: Verification API Gateway")
    try:
        response = requests.get(f"{API_GATEWAY_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"API Gateway accessible")
            print_info(f"  Status: {data.get('status')}")
            print_info(f"  Database: {'[OK] Connectee' if data.get('database_connected') else '[KO] Non connectee'}")
            return True
        else:
            print_error(f"API Gateway retourne {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Impossible de contacter l'API Gateway: {e}")
        print_info("Verifiez que les services sont demarres: docker-compose up")
        return False


def upload_image(image_path: str) -> Optional[str]:
    """Upload une image et retourne le job_id"""
    print_header("TEST 2: Upload de l'image")
    try:
        print_info(f"Image: {image_path}")
        
        with open(image_path, 'rb') as f:
            files = {
                'file': (
                    image_path.split('\\')[-1] if '\\' in image_path else image_path.split('/')[-1],
                    f,
                    'image/jpeg'
                )
            }
            response = requests.post(
                f"{API_GATEWAY_URL}/mobile/products/scan",
                files=files,
                timeout=TIMEOUT
            )
        
        if response.status_code == 200:
            data = response.json()
            job_id = data.get("job_id")
            print_success(f"Image uploadee avec succes")
            print_info(f"  Job ID: {job_id}")
            print_info(f"  Status initial: {data.get('status')}")
            return job_id
        else:
            print_error(f"Erreur upload: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except FileNotFoundError:
        print_error(f"Fichier introuvable: {image_path}")
        return None
    except Exception as e:
        print_error(f"Erreur lors de l'upload: {e}")
        return None


def poll_job_status(job_id: str) -> Optional[Dict[str, Any]]:
    """Pole le statut du job jusqu'à completion ou erreur"""
    print_header("TEST 3: Polling du statut du job")
    print_info(f"Job ID: {job_id}")
    print_info("Polling toutes les 2 secondes...\n")
    
    attempt = 0
    last_status = None
    
    while attempt < MAX_POLL_ATTEMPTS:
        try:
            response = requests.get(
                f"{API_GATEWAY_URL}/mobile/products/scan/{job_id}/status",
                timeout=10
            )
            
            if response.status_code != 200:
                print_error(f"Erreur recuperation statut: {response.status_code}")
                return None
            
            data = response.json()
            status = data.get("status")
            progress = data.get("progress", 0)
            current_step = data.get("current_step", "")
            
            # Afficher seulement si le statut a changé
            if status != last_status:
                status_icon = {
                    "PENDING": "[WAIT]",
                    "OCR": "[OCR]",
                    "NLP": "[NLP]",
                    "ACV": "[LCA]",
                    "SCORE": "[SCORE]",
                    "DONE": "[DONE]",
                    "ERROR": "[ERROR]"
                }
                icon = status_icon.get(status, "[?]")
                print(f"{icon} Status: {status} | Progress: {progress}% | {current_step[:60]}")
                last_status = status
            
            # Vérifier si terminé
            if status == "DONE":
                print_success("Workflow termine avec succes!")
                return data
            elif status == "ERROR":
                print_error("Workflow echoue")
                error_msg = data.get("error") or current_step
                print_error(f"  Erreur: {error_msg}")
                # En cas d'erreur, récupérer les détails complets via /debug
                try:
                    debug_response = requests.get(
                        f"{API_GATEWAY_URL}/mobile/products/scan/{job_id}/debug",
                        timeout=10
                    )
                    if debug_response.status_code == 200:
                        debug_data = debug_response.json()
                        # Fusionner les données de debug avec les données de status
                        data.update(debug_data)
                except:
                    pass
                return data
            
            time.sleep(2)
            attempt += 1
            
        except Exception as e:
            print_error(f"Erreur lors du polling: {e}")
            return None
    
    print_warning("Timeout: Le job n'a pas termine dans les temps")
    # Essayer de récupérer les résultats partiels même en timeout
    try:
        debug_response = requests.get(
            f"{API_GATEWAY_URL}/mobile/products/scan/{job_id}/debug",
            timeout=10
        )
        if debug_response.status_code == 200:
            return debug_response.json()
    except:
        pass
    return None


def analyze_results(data: Dict[str, Any]):
    """Analyse et affiche les résultats détaillés"""
    print_header("TEST 4: Analyse des resultats")
    
    # Résultats intermédiaires
    parser_result = data.get("parser_result")
    nlp_result = data.get("nlp_result")
    lca_result = data.get("lca_result")
    scoring_result = data.get("scoring_result")
    final_result = data.get("result")
    
    # 1. Parser Result
    print(f"\n{Colors.BOLD}1. PARSER SERVICE (OCR){Colors.RESET}")
    if parser_result:
        ingredients_raw = parser_result.get("ingredients_raw", "")
        product_name = parser_result.get("product_name", "N/A")
        confidence = parser_result.get("metadata", {}).get("confidence", 0.0)
        method = parser_result.get("metadata", {}).get("method", "unknown")
        
        print_success("Texte extrait")
        print_info(f"  Methode: {method}")
        print_info(f"  Confiance OCR: {confidence:.2%}")
        print_info(f"  Nom produit: {product_name}")
        print_info(f"  Ingredients bruts: {len(ingredients_raw)} caracteres")
        if ingredients_raw:
            print_info(f"  Apercu: {ingredients_raw[:200]}...")
    else:
        print_warning("Resultat Parser non disponible")
    
    # 2. NLP Result
    print(f"\n{Colors.BOLD}2. NLP SERVICE (Extraction){Colors.RESET}")
    if nlp_result:
        entities_normalized = nlp_result.get("entities_normalized", [])
        entities = nlp_result.get("entities", [])
        total_ingredients = nlp_result.get("total_ingredients", 0)
        
        print_success("Entites extraites")
        print_info(f"  Entites brutes: {len(entities)}")
        print_info(f"  Entites normalisees: {len(entities_normalized)}")
        print_info(f"  Total ingredients: {total_ingredients}")
        
        # Afficher les premiers ingrédients
        if entities_normalized:
            print_info("\n  Premiers ingredients:")
            ingredients = [e for e in entities_normalized if e.get("label", "").upper() == "INGREDIENT"]
            for i, entity in enumerate(ingredients[:10], 1):
                text = entity.get("text", "")
                normalized = entity.get("normalized_name", "")
                print(f"    {i}. {text} -> {normalized}")
    else:
        print_warning("Resultat NLP non disponible")
    
    # 3. LCA Result
    print(f"\n{Colors.BOLD}3. LCA SERVICE (Impacts){Colors.RESET}")
    if lca_result:
        total_impacts = lca_result.get("total_impacts", {})
        co2 = total_impacts.get("co2_kg", 0)
        water = total_impacts.get("water_m3", 0)
        energy = total_impacts.get("energy_mj", 0)
        
        print_success("Impacts calcules")
        print_info(f"  CO2: {co2:.3f} kg CO2-eq")
        print_info(f"  Eau: {water:.3f} m3")
        print_info(f"  Energie: {energy:.3f} MJ")
    else:
        print_warning("Resultat LCA non disponible")
    
    # 4. Scoring Result
    print(f"\n{Colors.BOLD}4. SCORING SERVICE (Score){Colors.RESET}")
    if scoring_result:
        score_letter = scoring_result.get("score_letter", "N/A")
        score_value = scoring_result.get("score_numeric", 0)
        confidence = scoring_result.get("confidence", 0.0)
        
        print_success("Score calcule")
        print_info(f"  Score: {score_letter} ({score_value:.1f}/100)")
        print_info(f"  Confiance: {confidence:.2%}")
    else:
        print_warning("Resultat Scoring non disponible")
    
    # 5. Final Result
    print(f"\n{Colors.BOLD}5. RESULTAT FINAL{Colors.RESET}")
    if final_result:
        score_letter = final_result.get("score_letter", "N/A")
        score_value = final_result.get("score_value", 0)
        
        # Afficher le score avec couleur
        if score_letter == "A":
            color = Colors.GREEN
        elif score_letter == "B":
            color = Colors.CYAN
        elif score_letter == "C":
            color = Colors.YELLOW
        else:
            color = Colors.RED
        
        print(f"\n{color}{'=' * 80}{Colors.RESET}")
        print(f"{color}{Colors.BOLD}SCORE ECOLOGIQUE: {score_letter} ({score_value:.1f}/100){Colors.RESET}")
        print(f"{color}{'=' * 80}{Colors.RESET}\n")
        
        # Détails
        acv_data = final_result.get("acv_data", {})
        print_info(f"CO2: {acv_data.get('co2_kg', 0):.3f} kg CO2-eq")
        print_info(f"Eau: {acv_data.get('water_liters', 0):.1f} L")
        print_info(f"Energie: {acv_data.get('energy_mj', 0):.3f} MJ")
    else:
        print_warning("Resultat final non disponible")


def test_workflow(image_path: str):
    """Teste le workflow complet"""
    print_header("TEST WORKFLOW COMPLET - ECOLABEL")
    print_info(f"API Gateway: {API_GATEWAY_URL}")
    print_info(f"Image: {image_path}\n")
    
    # Test 1: Health check
    if not test_api_gateway_health():
        print_error("Impossible de continuer: API Gateway non accessible")
        return False
    
    # Test 2: Upload
    job_id = upload_image(image_path)
    if not job_id:
        print_error("Impossible de continuer: Upload echoue")
        return False
    
    # Test 3: Polling
    result = poll_job_status(job_id)
    if not result:
        print_error("Impossible de continuer: Polling echoue")
        return False
    
    # Test 4: Analyse
    analyze_results(result)
    
    # Résumé
    status = result.get("status")
    if status == "DONE":
        print_header("[SUCCESS] WORKFLOW REUSSI")
        return True
    else:
        print_header("[ERROR] WORKFLOW ECHOUE")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_error("Usage: python test_workflow_complete.py <path_to_image>")
        print_info("Example: python test_workflow_complete.py c:\\Users\\doaa\\Downloads\\coca.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = test_workflow(image_path)
    sys.exit(0 if success else 1)
