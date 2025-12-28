"""
Script pour tester directement l'OCR Tesseract
"""
import sys
import requests
from pathlib import Path

PARSER_SERVICE_URL = "http://localhost:8001"

def test_ocr(image_path):
    """Teste l'OCR directement avec le Parser Service"""
    print("=" * 80)
    print("TEST OCR DIRECT")
    print("=" * 80)
    print(f"Image: {image_path}")
    print(f"Parser Service: {PARSER_SERVICE_URL}")
    print()
    
    if not Path(image_path).exists():
        print(f"ERREUR: Fichier introuvable: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {
                'file': (
                    image_path.split('\\')[-1] if '\\' in image_path else image_path.split('/')[-1],
                    f,
                    'image/jpeg'
                )
            }
            print("Upload de l'image...")
            response = requests.post(
                f"{PARSER_SERVICE_URL}/product/parse/single",
                files=files,
                timeout=60
            )
        
        if response.status_code != 200:
            print(f"ERREUR: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        result = response.json()
        
        print("\n" + "=" * 80)
        print("RESULTAT")
        print("=" * 80)
        
        text = result.get("ingredients_raw", "")
        confidence = result.get("metadata", {}).get("confidence", 0.0)
        method = result.get("metadata", {}).get("method", "unknown")
        
        print(f"\nMethode: {method}")
        print(f"Confiance OCR: {confidence:.2%}")
        print(f"Texte extrait: {len(text)} caracteres")
        
        if text:
            print(f"\nTexte extrait:")
            print("-" * 80)
            print(text[:500])
            if len(text) > 500:
                print("...")
            print("-" * 80)
            print("\n[OK] Texte extrait avec succes!")
            return True
        else:
            print("\n[ERREUR] Aucun texte extrait!")
            print("\nCauses possibles:")
            print("  1. Image sans texte visible")
            print("  2. Qualite d'image insuffisante")
            print("  3. Texte trop petit ou flou")
            print("  4. Langue non supportee")
            print("  5. Probleme avec Tesseract OCR")
            return False
        
    except Exception as e:
        print(f"ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_ocr_direct.py <path_to_image>")
        print("Example: python test_ocr_direct.py c:\\Users\\doaa\\Downloads\\coca.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = test_ocr(image_path)
    sys.exit(0 if success else 1)


