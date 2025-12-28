import '../../../../core/network/api_client.dart';
import '../models/trends_model.dart';
import '../models/ingredient_stat_model.dart';
import '../models/recommendation_model.dart';
import '../models/prediction_model.dart';
import '../models/anomaly_model.dart';

class AnalyticsRemoteDataSource {
  final ApiClient apiClient;

  AnalyticsRemoteDataSource(this.apiClient);

  /// Get trends (evolution of scores over time)
  Future<TrendsModel> getTrends() async {
    final response = await apiClient.get<Map<String, dynamic>>(
      '/analytics/trends',
    );
    return TrendsModel.fromJson(response.data!);
  }

  /// Get top N most frequent ingredients
  Future<List<IngredientStatModel>> getTopIngredients(int topN) async {
    final response = await apiClient.get<Map<String, dynamic>>(
      '/analytics/ingredients/frequent',
      queryParameters: {'top_n': topN},
    );
    return (response.data!['ingredients'] as List)
        .map((json) => IngredientStatModel.fromJson(json as Map<String, dynamic>))
        .toList();
  }

  /// Get ingredients associated with low scores
  Future<List<IngredientStatModel>> getBadIngredients({
    required double threshold,
    required int topN,
  }) async {
    final response = await apiClient.get<Map<String, dynamic>>(
      '/analytics/ingredients/low-score',
      queryParameters: {
        'threshold': threshold,
        'top_n': topN,
      },
    );
    return (response.data!['ingredients'] as List)
        .map((json) => IngredientStatModel.fromJson(json as Map<String, dynamic>))
        .toList();
  }

  /// Get score prediction for a product
  Future<PredictionModel> getPrediction(String jobId) async {
    final response = await apiClient.get<Map<String, dynamic>>(
      '/analytics/predictions/$jobId',
    );
    return PredictionModel.fromJson(response.data!['prediction'] as Map<String, dynamic>);
  }

  /// Get recommendations (similar products with better scores)
  Future<List<RecommendationModel>> getRecommendations(
    String jobId, {
    int topN = 5,
  }) async {
    final response = await apiClient.get<Map<String, dynamic>>(
      '/analytics/recommendations/$jobId',
      queryParameters: {'top_n': topN},
    );
    return (response.data!['recommendations'] as List)
        .map((json) => RecommendationModel.fromJson(json as Map<String, dynamic>))
        .toList();
  }

  /// Get detected anomalies
  Future<List<AnomalyModel>> getAnomalies() async {
    final response = await apiClient.get<Map<String, dynamic>>(
      '/analytics/anomalies',
    );
    return (response.data!['anomalies'] as List)
        .map((json) => AnomalyModel.fromJson(json as Map<String, dynamic>))
        .toList();
  }
}





