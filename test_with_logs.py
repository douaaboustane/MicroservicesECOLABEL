"""
Script de test avec capture des logs détaillés pour diagnostiquer l'erreur 422
"""
import requests
import time
import sys
import subprocess
import threading
from typing import Optional, Dict, Any

API_GATEWAY_URL = "http://localhost:8000"
TIMEOUT = 30
MAX_POLL_ATTEMPTS = 60


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    print(f"\n{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")


def print_success(text: str):
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")


def print_error(text: str):
    print(f"{Colors.RED}[ERROR] {text}{Colors.RESET}")


def print_info(text: str):
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")


def monitor_logs(service: str, job_id: str, stop_event: threading.Event):
    """Monitor les logs d'un service en temps réel"""
    try:
        process = subprocess.Popen(
            ["docker-compose", "logs", "-f", "--tail", "0", service],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        keywords = [
            "FINAL PAYLOAD",
            "LCA Request payload",
            "ERROR LCA",
            "422",
            "VALIDATION",
            "INCOMING",
            "NLP Result",
            "Labels trouvés",
            "Ingredient prepared"
        ]
        
        for line in process.stdout:
            if stop_event.is_set():
                break
            
            line_lower = line.lower()
            if any(keyword.lower() in line_lower for keyword in keywords):
                print(f"{Colors.YELLOW}[LOG {service}] {line.strip()}{Colors.RESET}")
            
            if job_id in line:
                print(f"{Colors.CYAN}[LOG {service}] {line.strip()}{Colors.RESET}")
        
        process.terminate()
    except Exception as e:
        print_error(f"Erreur monitoring logs: {e}")


def upload_image(image_path: str) -> Optional[str]:
    """Upload une image et retourne le job_id"""
    print_header("UPLOAD DE L'IMAGE")
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
            print_success(f"Image uploadée avec succès")
            print_info(f"Job ID: {job_id}")
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


def poll_job_status(job_id: str, stop_event: threading.Event) -> Optional[Dict[str, Any]]:
    """Pole le statut du job jusqu'à completion ou erreur"""
    print_header("POLLING DU STATUT")
    print_info(f"Job ID: {job_id}")
    print_info("Polling toutes les 2 secondes...\n")
    
    attempt = 0
    last_status = None
    
    while attempt < MAX_POLL_ATTEMPTS and not stop_event.is_set():
        try:
            response = requests.get(
                f"{API_GATEWAY_URL}/mobile/products/scan/{job_id}/status",
                timeout=10
            )
            
            if response.status_code != 200:
                print_error(f"Erreur récupération statut: {response.status_code}")
                return None
            
            data = response.json()
            status = data.get("status")
            progress = data.get("progress", 0)
            current_step = data.get("current_step", "")
            
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
            
            if status == "DONE":
                print_success("Workflow terminé avec succès!")
                stop_event.set()
                return data
            elif status == "ERROR":
                print_error("Workflow échoué")
                error_msg = data.get("error") or current_step
                print_error(f"Erreur: {error_msg}")
                stop_event.set()
                return data
            
            time.sleep(2)
            attempt += 1
            
        except Exception as e:
            print_error(f"Erreur lors du polling: {e}")
            return None
    
    stop_event.set()
    return None


def analyze_job_details(job_id: str):
    """Analyse les détails d'un job pour diagnostiquer l'erreur"""
    print_header("ANALYSE DES DÉTAILS DU JOB")
    
    try:
        # Essayer le endpoint /debug
        response = requests.get(
            f"{API_GATEWAY_URL}/mobile/products/scan/{job_id}/debug",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Afficher les résultats intermédiaires
            print_info("Résultats intermédiaires:")
            
            parser_result = data.get("parser_result")
            if parser_result:
                print(f"\n{Colors.BOLD}1. PARSER RESULT{Colors.RESET}")
                ingredients_raw = parser_result.get("ingredients_raw", "")
                print(f"  Ingredients bruts: {len(ingredients_raw)} caractères")
                if ingredients_raw:
                    print(f"  Aperçu: {ingredients_raw[:200]}...")
            
            nlp_result = data.get("nlp_result")
            if nlp_result:
                print(f"\n{Colors.BOLD}2. NLP RESULT{Colors.RESET}")
                entities_normalized = nlp_result.get("entities_normalized", [])
                print(f"  Entités normalisées: {len(entities_normalized)}")
                
                # Afficher les ingrédients préparés pour LCA
                ingredients = [e for e in entities_normalized if e.get("label", "").upper() == "INGREDIENT"]
                print(f"  Ingrédients trouvés: {len(ingredients)}")
                for i, ing in enumerate(ingredients[:10], 1):
                    print(f"    {i}. {ing.get('text')} -> {ing.get('normalized_name')}")
            
            lca_result = data.get("lca_result")
            if lca_result:
                print(f"\n{Colors.BOLD}3. LCA RESULT{Colors.RESET}")
                print(f"  {lca_result}")
            
            error_message = data.get("error_message")
            if error_message:
                print(f"\n{Colors.RED}ERROR MESSAGE: {error_message}{Colors.RESET}")
        else:
            print_error(f"Endpoint /debug non accessible: {response.status_code}")
            
            # Essayer le endpoint /status
            response = requests.get(
                f"{API_GATEWAY_URL}/mobile/products/scan/{job_id}/status",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print_info("Données du job (via /status):")
                print(f"  Status: {data.get('status')}")
                print(f"  Progress: {data.get('progress')}%")
                print(f"  Current Step: {data.get('current_step')}")
                if data.get('error'):
                    print(f"  Error: {data.get('error')}")
                
                # Afficher les résultats intermédiaires si disponibles
                if data.get('parser_result'):
                    print(f"\n  Parser Result disponible: {len(str(data.get('parser_result')))} caractères")
                if data.get('nlp_result'):
                    print(f"  NLP Result disponible: {len(str(data.get('nlp_result')))} caractères")
                    
    except Exception as e:
        print_error(f"Erreur analyse job: {e}")


def test_workflow_with_logs(image_path: str):
    """Teste le workflow avec monitoring des logs"""
    print_header("TEST WORKFLOW AVEC LOGS DÉTAILLÉS")
    print_info(f"API Gateway: {API_GATEWAY_URL}")
    print_info(f"Image: {image_path}\n")
    
    # Upload
    job_id = upload_image(image_path)
    if not job_id:
        print_error("Impossible de continuer: Upload échoué")
        return
    
    # Démarrer le monitoring des logs
    stop_event = threading.Event()
    
    log_threads = []
    for service in ["api-gateway", "api-gateway-worker", "lca-service"]:
        thread = threading.Thread(
            target=monitor_logs,
            args=(service, job_id, stop_event),
            daemon=True
        )
        thread.start()
        log_threads.append(thread)
    
    print_info("Monitoring des logs démarré...")
    time.sleep(2)  # Laisser le temps aux threads de démarrer
    
    # Polling
    result = poll_job_status(job_id, stop_event)
    
    # Arrêter le monitoring
    stop_event.set()
    time.sleep(1)
    
    # Analyser les détails
    analyze_job_details(job_id)
    
    # Résumé
    if result and result.get("status") == "DONE":
        print_header("[SUCCESS] WORKFLOW RÉUSSI")
    else:
        print_header("[ERROR] WORKFLOW ÉCHOUÉ")
        print_info("Consultez les logs ci-dessus pour voir le payload exact envoyé au LCA Service")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_error("Usage: python test_with_logs.py <path_to_image>")
        print_info("Example: python test_with_logs.py c:\\Users\\doaa\\Downloads\\image.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    test_workflow_with_logs(image_path)

