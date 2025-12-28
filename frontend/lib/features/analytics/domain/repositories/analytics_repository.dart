import '../entities/trends.dart';
import '../entities/ingredient_stat.dart';
import '../entities/recommendation.dart';
import '../entities/prediction.dart';
import '../entities/anomaly.dart';

abstract class AnalyticsRepository {
  Future<Trends> getTrends();
  Future<List<IngredientStat>> getTopIngredients(int topN);
  Future<List<IngredientStat>> getBadIngredients({
    required double threshold,
    required int topN,
  });
  Future<Prediction> getPrediction(String jobId);
  Future<List<Recommendation>> getRecommendations(
    String jobId, {
    int topN = 5,
  });
  Future<List<Anomaly>> getAnomalies();
}





