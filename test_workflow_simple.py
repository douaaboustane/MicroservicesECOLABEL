"""
Script de test simple du workflow complet
"""
import requests
import time
import sys
import os

API_GATEWAY_URL = "http://localhost:8000"

def test_workflow(image_path):
    """Teste le workflow complet avec une image"""
    
    print("\n" + "="*80)
    print("TEST WORKFLOW COMPLET - ECOLABEL".center(80))
    print("="*80 + "\n")
    
    # 1. Vérifier que l'image existe
    if not os.path.exists(image_path):
        print(f"[ERROR] Image non trouvée: {image_path}")
        return False
    
    print(f"[INFO] Image: {image_path}")
    print(f"[INFO] API Gateway: {API_GATEWAY_URL}\n")
    
    # 2. Upload de l'image
    print("="*80)
    print("ÉTAPE 1: Upload de l'image".center(80))
    print("="*80 + "\n")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/png')}
            response = requests.post(
                f"{API_GATEWAY_URL}/mobile/products/scan",
                files=files,
                timeout=10
            )
            response.raise_for_status()
            job_data = response.json()
            job_id = job_data['job_id']
            print(f"[OK] Image uploadée avec succès")
            print(f"[INFO] Job ID: {job_id}")
            print(f"[INFO] Status initial: {job_data['status']}\n")
    except Exception as e:
        print(f"[ERROR] Erreur lors de l'upload: {e}")
        return False
    
    # 3. Polling du statut
    print("="*80)
    print("ÉTAPE 2: Polling du statut du job".center(80))
    print("="*80 + "\n")
    
    print(f"[INFO] Job ID: {job_id}")
    print(f"[INFO] Polling toutes les 2 secondes...\n")
    
    max_attempts = 60  # 2 minutes max
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get(
                f"{API_GATEWAY_URL}/mobile/products/scan/{job_id}/status",
                timeout=5
            )
            response.raise_for_status()
            status_data = response.json()
            
            status = status_data['status']
            progress = status_data.get('progress', 0)
            current_step = status_data.get('current_step', '')
            
            # Afficher le statut avec un préfixe selon l'étape
            if status == 'OCR':
                prefix = '[OCR]'
            elif status == 'NLP':
                prefix = '[NLP]'
            elif status == 'ACV':
                prefix = '[LCA]'
            elif status == 'SCORING':
                prefix = '[SCORING]'
            elif status == 'DONE':
                prefix = '[DONE]'
            elif status == 'ERROR':
                prefix = '[ERROR]'
            else:
                prefix = '[INFO]'
            
            print(f"{prefix} Status: {status} | Progress: {progress}% | {current_step}")
            
            if status == 'DONE':
                print(f"\n[OK] Workflow terminé avec succès!\n")
                break
            elif status == 'ERROR':
                error_msg = status_data.get('error_message', 'Erreur inconnue')
                print(f"\n[ERROR] Workflow échoué")
                print(f"[ERROR]   Erreur: {error_msg}\n")
                return False
            
            time.sleep(2)
            attempt += 1
            
        except Exception as e:
            print(f"[ERROR] Erreur lors du polling: {e}")
            return False
    
    if attempt >= max_attempts:
        print(f"\n[ERROR] Timeout: Le job n'a pas terminé dans les temps")
        return False
    
    # 4. Récupérer les résultats
    print("="*80)
    print("ÉTAPE 3: Résultats".center(80))
    print("="*80 + "\n")
    
    try:
        response = requests.get(
            f"{API_GATEWAY_URL}/mobile/products/scan/{job_id}/status",
            timeout=5
        )
        response.raise_for_status()
        result = response.json()
        
        # Afficher les résultats
        if result.get('parser_result'):
            print("[OK] Résultat Parser (OCR) disponible")
            parser = result['parser_result']
            if parser.get('ingredients'):
                print(f"  Ingrédients extraits: {len(parser['ingredients'])}")
                print(f"  Texte extrait: {parser.get('text', '')[:100]}...")
        
        if result.get('nlp_result'):
            print("[OK] Résultat NLP disponible")
            nlp = result['nlp_result']
            print(f"  Entités trouvées: {nlp.get('total_entities', 0)}")
            print(f"  Ingrédients: {nlp.get('total_ingredients', 0)}")
        
        if result.get('lca_result'):
            print("[OK] Résultat LCA disponible")
            lca = result['lca_result']
            impacts = lca.get('total_impacts', {})
            print(f"  CO2: {impacts.get('co2_kg', 0):.2f} kg")
            print(f"  Eau: {impacts.get('water_m3', 0):.2f} m³")
            print(f"  Énergie: {impacts.get('energy_mj', 0):.2f} MJ")
        
        if result.get('scoring_result'):
            print("[OK] Résultat Scoring disponible")
            scoring = result['scoring_result']
            print(f"  Score: {scoring.get('score', 0):.1f}/100")
            print(f"  Grade: {scoring.get('grade', 'N/A')}")
        
        print("\n" + "="*80)
        print("[SUCCESS] WORKFLOW TERMINÉ AVEC SUCCÈS!".center(80))
        print("="*80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Erreur lors de la récupération des résultats: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_workflow_simple.py <chemin_vers_image>")
        print("\nExemple:")
        print("  python test_workflow_simple.py C:\\Users\\doaa\\Downloads\\4.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = test_workflow(image_path)
    sys.exit(0 if success else 1)

