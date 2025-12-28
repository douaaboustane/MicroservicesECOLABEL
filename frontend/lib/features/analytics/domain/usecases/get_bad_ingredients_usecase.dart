import '../repositories/analytics_repository.dart';
import '../entities/ingredient_stat.dart';

class GetBadIngredientsUseCase {
  final AnalyticsRepository repository;

  GetBadIngredientsUseCase(this.repository);

  Future<List<IngredientStat>> call({
    required double threshold,
    required int topN,
  }) async {
    return await repository.getBadIngredients(
      threshold: threshold,
      topN: topN,
    );
  }
}





