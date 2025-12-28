import '../../domain/entities/trends.dart';
import '../../domain/entities/ingredient_stat.dart';
import '../../domain/entities/recommendation.dart';
import '../../domain/entities/prediction.dart';
import '../../domain/entities/anomaly.dart';
import '../../domain/repositories/analytics_repository.dart';
import '../datasources/analytics_remote_ds.dart';

class AnalyticsRepositoryImpl implements AnalyticsRepository {
  final AnalyticsRemoteDataSource remoteDataSource;

  AnalyticsRepositoryImpl(this.remoteDataSource);

  @override
  Future<Trends> getTrends() async {
    try {
      return await remoteDataSource.getTrends();
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<List<IngredientStat>> getTopIngredients(int topN) async {
    try {
      return await remoteDataSource.getTopIngredients(topN);
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<List<IngredientStat>> getBadIngredients({
    required double threshold,
    required int topN,
  }) async {
    try {
      return await remoteDataSource.getBadIngredients(
        threshold: threshold,
        topN: topN,
      );
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<Prediction> getPrediction(String jobId) async {
    try {
      return await remoteDataSource.getPrediction(jobId);
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<List<Recommendation>> getRecommendations(
    String jobId, {
    int topN = 5,
  }) async {
    try {
      return await remoteDataSource.getRecommendations(jobId, topN: topN);
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<List<Anomaly>> getAnomalies() async {
    try {
      return await remoteDataSource.getAnomalies();
    } catch (e) {
      rethrow;
    }
  }
}





