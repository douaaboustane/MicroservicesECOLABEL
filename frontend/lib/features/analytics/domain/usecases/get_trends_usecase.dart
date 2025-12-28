import '../repositories/analytics_repository.dart';
import '../entities/trends.dart';

class GetTrendsUseCase {
  final AnalyticsRepository repository;

  GetTrendsUseCase(this.repository);

  Future<Trends> call() async {
    return await repository.getTrends();
  }
}





