import '../entities/eco_score.dart';
import '../../data/repositories/result_repository_impl.dart';

/// Use case pour récupérer le score final
class GetFinalScore {
  final ResultRepositoryImpl repository;

  GetFinalScore(this.repository);

  Future<EcoScore> call(String jobId) async {
    return await repository.getFinalScore(jobId);
  }
}
