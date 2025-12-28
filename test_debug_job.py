"""
Script pour tester et déboguer un job spécifique
Utilise le endpoint /debug pour voir tous les détails
"""
import requests
import sys
import json

API_GATEWAY_URL = "http://localhost:8000"


def test_job_debug(job_id: str):
    """Récupère tous les détails d'un job"""
    print(f"\n{'=' * 80}")
    print(f"DEBUG JOB: {job_id}")
    print(f"{'=' * 80}\n")
    
    try:
        response = requests.get(
            f"{API_GATEWAY_URL}/mobile/products/scan/{job_id}/debug",
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)
            return
        
        data = response.json()
        
        # Afficher les informations de base
        print(f"📋 Job ID: {data.get('job_id')}")
        print(f"📊 Status: {data.get('status')}")
        print(f"📈 Progress: {data.get('progress')}%")
        print(f"📝 Current Step: {data.get('current_step')}")
        if data.get('error_message'):
            print(f"❌ Error: {data.get('error_message')}")
        print()
        
        # Parser Result
        parser_result = data.get('parser_result')
        if parser_result:
            print(f"{'=' * 80}")
            print("1. PARSER RESULT (OCR)")
            print(f"{'=' * 80}")
            ingredients_raw = parser_result.get('ingredients_raw', '')
            product_name = parser_result.get('product_name', 'N/A')
            metadata = parser_result.get('metadata', {})
            confidence = metadata.get('confidence', 0)
            method = metadata.get('method', 'unknown')
            
            print(f"  Method: {method}")
            print(f"  Confidence: {confidence:.2%}")
            print(f"  Product Name: {product_name}")
            print(f"  Ingredients Raw Length: {len(ingredients_raw)} chars")
            if ingredients_raw:
                print(f"  Preview: {ingredients_raw[:200]}...")
            print()
        else:
            print("⚠️  Parser Result: Non disponible\n")
        
        # NLP Result
        nlp_result = data.get('nlp_result')
        if nlp_result:
            print(f"{'=' * 80}")
            print("2. NLP RESULT (Extraction)")
            print(f"{'=' * 80}")
            entities = nlp_result.get('entities', [])
            entities_normalized = nlp_result.get('entities_normalized', [])
            total_ingredients = nlp_result.get('total_ingredients', 0)
            
            print(f"  Entities: {len(entities)}")
            print(f"  Entities Normalized: {len(entities_normalized)}")
            print(f"  Total Ingredients: {total_ingredients}")
            
            # Afficher les labels trouvés
            labels = {}
            for e in entities_normalized if entities_normalized else entities:
                if isinstance(e, dict):
                    label = e.get('label', 'UNKNOWN')
                    labels[label] = labels.get(label, 0) + 1
            print(f"  Labels: {labels}")
            
            # Afficher les premiers ingrédients
            if entities_normalized:
                print("\n  Premiers ingrédients:")
                ingredients = [e for e in entities_normalized if e.get('label', '').upper() == 'INGREDIENT']
                for i, ing in enumerate(ingredients[:10], 1):
                    text = ing.get('text', '')
                    normalized = ing.get('normalized_name', '')
                    print(f"    {i}. {text} -> {normalized}")
            print()
        else:
            print("⚠️  NLP Result: Non disponible\n")
        
        # LCA Result
        lca_result = data.get('lca_result')
        if lca_result:
            print(f"{'=' * 80}")
            print("3. LCA RESULT (Impacts)")
            print(f"{'=' * 80}")
            total_impacts = lca_result.get('total_impacts', {})
            print(f"  CO2: {total_impacts.get('co2_kg', 0):.3f} kg CO2-eq")
            print(f"  Water: {total_impacts.get('water_m3', 0):.3f} m3")
            print(f"  Energy: {total_impacts.get('energy_mj', 0):.3f} MJ")
            print()
        else:
            print("⚠️  LCA Result: Non disponible\n")
        
        # Scoring Result
        scoring_result = data.get('scoring_result')
        if scoring_result:
            print(f"{'=' * 80}")
            print("4. SCORING RESULT")
            print(f"{'=' * 80}")
            score_letter = scoring_result.get('score_letter', 'N/A')
            score_value = scoring_result.get('score_numeric', 0)
            print(f"  Score: {score_letter} ({score_value:.1f}/100)")
            print()
        else:
            print("⚠️  Scoring Result: Non disponible\n")
        
        # Final Result
        final_result = data.get('result')
        if final_result:
            print(f"{'=' * 80}")
            print("5. FINAL RESULT")
            print(f"{'=' * 80}")
            print(json.dumps(final_result, indent=2, ensure_ascii=False))
            print()
        
        # Si erreur, afficher les détails complets
        if data.get('status') == 'ERROR':
            print(f"{'=' * 80}")
            print("❌ ERREUR DETECTEE")
            print(f"{'=' * 80}")
            print(f"Error Message: {data.get('error_message')}")
            print("\nPour diagnostiquer l'erreur 422 du LCA Service:")
            print("1. Vérifiez que le NLP a trouvé des ingrédients")
            print("2. Vérifiez les logs: docker-compose logs lca-service --tail 50")
            print("3. Vérifiez les logs de l'API Gateway: docker-compose logs api-gateway --tail 100")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_debug_job.py <job_id>")
        print("\nPour obtenir un job_id, testez d'abord:")
        print("  python test_workflow_complete.py <image_path>")
        sys.exit(1)
    
    job_id = sys.argv[1]
    test_job_debug(job_id)
