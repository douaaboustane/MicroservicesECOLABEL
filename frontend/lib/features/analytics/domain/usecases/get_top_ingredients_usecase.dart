import '../repositories/analytics_repository.dart';
import '../entities/ingredient_stat.dart';

class GetTopIngredientsUseCase {
  final AnalyticsRepository repository;

  GetTopIngredientsUseCase(this.repository);

  Future<List<IngredientStat>> call(int topN) async {
    return await repository.getTopIngredients(topN);
  }
}





