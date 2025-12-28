import '../repositories/analytics_repository.dart';
import '../entities/recommendation.dart';

class GetRecommendationsUseCase {
  final AnalyticsRepository repository;

  GetRecommendationsUseCase(this.repository);

  Future<List<Recommendation>> call(String jobId, {int topN = 5}) async {
    return await repository.getRecommendations(jobId, topN: topN);
  }
}





