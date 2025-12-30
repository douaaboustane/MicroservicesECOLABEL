"""
Script de démonstration pour tester RabbitMQ
Envoie une image à l'API et affiche le résultat
"""
import requests
import sys
import os
from pathlib import Path

def test_scan_api(image_path):
    """Test l'endpoint de scan avec une image"""
    
    if not os.path.exists(image_path):
        print(f"ERREUR: Le fichier {image_path} n'existe pas")
        return None
    
    url = "http://localhost:8000/mobile/products/scan"
    
    print("=" * 80)
    print("DEMONSTRATION RABBITMQ - Envoi de message")
    print("=" * 80)
    print(f"Fichier: {image_path}")
    print(f"URL: {url}")
    print("\nEnvoi en cours...\n")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("=" * 80)
            print("SUCCES - Job cree!")
            print("=" * 80)
            print(f"Job ID: {result.get('job_id')}")
            print(f"Status: {result.get('status')}")
            print(f"Created at: {result.get('created_at')}")
            print("\n" + "=" * 80)
            print("PROCHAINES ETAPES:")
            print("=" * 80)
            print("1. Ouvrez RabbitMQ UI: http://localhost:15672")
            print("2. Allez dans l'onglet 'Queues and Streams'")
            print("3. Cliquez sur la queue 'product_scan'")
            print("4. Observez le message qui apparaît (Ready: 1)")
            print("5. Rafraîchissez pour voir le traitement (Unacked puis consommé)")
            print("\nVerifier le statut du job:")
            print(f"   curl http://localhost:8000/mobile/products/scan/{result.get('job_id')}/status")
            print("=" * 80 + "\n")
            return result.get('job_id')
        else:
            print("=" * 80)
            print(f"ERREUR: Status code {response.status_code}")
            print("=" * 80)
            print(f"Réponse: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("ERREUR: Impossible de se connecter a l'API")
        print("   Verifiez que le service API Gateway est demarre (port 8000)")
        return None
    except Exception as e:
        print(f"ERREUR: {e}")
        return None


if __name__ == "__main__":
    # Essayer plusieurs chemins possibles pour une image
    possible_images = [
        r"C:\Users\doaa\Downloads\test_product.jpg",
        r"C:\Users\doaa\Downloads\1.jpeg",
        r"C:\Users\doaa\Downloads\a.jpeg",
        r"C:\Users\doaa\Downloads\cerelac.png",
        r"C:\Users\doaa\Downloads\coca.png",
        r"C:\Users\doaa\Downloads\fanta.png",
    ]
    
    # Si un argument est fourni, l'utiliser
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Sinon, chercher la première image disponible
        image_path = None
        for path in possible_images:
            if os.path.exists(path):
                image_path = path
                break
        
        if not image_path:
            print("ERREUR: Aucune image trouvee. Utilisation:")
            print(f"   python {sys.argv[0]} <chemin_vers_image>")
            print("\nImages testees:")
            for path in possible_images:
                print(f"   - {path}")
            sys.exit(1)
    
    job_id = test_scan_api(image_path)
    
    if job_id:
        print(f"\nScript termine. Job ID: {job_id}")

