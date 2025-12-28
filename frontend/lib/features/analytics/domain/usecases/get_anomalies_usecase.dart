import '../repositories/analytics_repository.dart';
import '../entities/anomaly.dart';

class GetAnomaliesUseCase {
  final AnalyticsRepository repository;

  GetAnomaliesUseCase(this.repository);

  Future<List<Anomaly>> call() async {
    return await repository.getAnomalies();
  }
}





