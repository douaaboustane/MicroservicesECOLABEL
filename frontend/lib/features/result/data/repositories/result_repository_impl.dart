import '../../../../core/network/api_client.dart';
import '../../domain/entities/eco_score.dart';

/// Repository pour les résultats
class ResultRepositoryImpl {
  final ApiClient apiClient;

  ResultRepositoryImpl(this.apiClient);

  /// Récupère le score final d'un job
  /// 
  /// Adapte la réponse backend au format attendu par le frontend
  /// Backend: GET /mobile/products/scan/{job_id}/status
  /// Retourne: {job_id, status, result: {score_letter, score_value, acv_data: {...}}}
  Future<EcoScore> getFinalScore(String jobId) async {
    // Utiliser l'endpoint backend réel
    final response = await apiClient.get<Map<String, dynamic>>(
      '/mobile/products/scan/$jobId/status',
    );

    final data = response.data!;
    
    // Vérifier que le job est terminé
    final status = data['status'] as String?;
    if (status == null) {
      throw Exception('Statut du job non disponible');
    }
    
    if (status != 'DONE') {
      throw Exception('L\'analyse est encore en cours. Statut: $status');
    }
    
    // Extraire le résultat
    final result = data['result'] as Map<String, dynamic>?;
    if (result == null || result.isEmpty) {
      throw Exception('Aucun résultat disponible pour ce job. L\'analyse peut avoir échoué.');
    }
    
    // Extraire les données ACV
    final acvData = result['acv_data'] as Map<String, dynamic>? ?? {};
    
    // Mapper les données backend vers le format frontend
    return EcoScore(
      jobId: jobId,
      scoreLetter: result['score_letter'] as String? ?? 'C',
      scoreNumeric: (result['score_value'] as num?)?.round() ?? 50,
      co2: (acvData['co2_kg'] as num?)?.toDouble() ?? 0.0,
      water: (acvData['water_liters'] as num?)?.toDouble() ?? 0.0,
      // Convertir MJ en kWh (1 MJ = 0.277778 kWh) ou garder en MJ
      // Pour l'instant, on garde la valeur en MJ mais on la divise par 3.6 pour avoir kWh
      energy: ((acvData['energy_mj'] as num?)?.toDouble() ?? 0.0) / 3.6,
      // TODO: Récupérer la liste des ingrédients depuis un autre endpoint
      // Pour l'instant, on retourne une liste vide ou on peut utiliser ingredients_count
      ingredients: _extractIngredients(result, acvData),
      // Utiliser updated_at du job si disponible, sinon maintenant
      calculatedAt: DateTime.now(), // TODO: Utiliser data['updated_at'] si disponible
    );
  }
  
  /// Extrait la liste des ingrédients depuis le résultat
  /// 
  /// Le backend retourne maintenant les ingrédients dans result['ingredients']
  List<String> _extractIngredients(Map<String, dynamic> result, Map<String, dynamic> acvData) {
    // Option 1: Si les ingrédients sont directement dans result (nouveau format)
    if (result.containsKey('ingredients') && result['ingredients'] is List) {
      final ingredients = result['ingredients'] as List;
      return ingredients
          .map((ing) {
            // Si c'est un Map, extraire le nom
            if (ing is Map<String, dynamic>) {
              return ing['name'] as String? ?? ing.toString();
            }
            // Sinon, convertir en String
            return ing.toString();
          })
          .where((name) => name.isNotEmpty)
          .toList()
          .cast<String>();
    }
    
    // Option 2: Si les ingrédients sont dans acv_data (ancien format)
    if (acvData.containsKey('ingredients') && acvData['ingredients'] is List) {
      final ingredients = acvData['ingredients'] as List;
      return ingredients
          .map((ing) {
            if (ing is Map<String, dynamic>) {
              return ing['name'] as String? ?? ing.toString();
            }
            return ing.toString();
          })
          .where((name) => name.isNotEmpty)
          .toList()
          .cast<String>();
    }
    
    // Par défaut, retourner une liste vide (ne plus générer "Ingrédient 1", "Ingrédient 2")
    return [];
  }
}
