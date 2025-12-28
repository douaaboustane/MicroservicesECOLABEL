import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../injection_container.dart';
import '../domain/entities/trends.dart';
import '../domain/entities/ingredient_stat.dart';
import '../domain/entities/recommendation.dart';
import '../domain/entities/anomaly.dart';
import '../domain/usecases/get_trends_usecase.dart';
import '../domain/usecases/get_top_ingredients_usecase.dart';
import '../domain/usecases/get_bad_ingredients_usecase.dart';
import '../domain/usecases/get_recommendations_usecase.dart';
import '../domain/usecases/get_anomalies_usecase.dart';

// Providers for analytics data

final trendsProvider = FutureProvider<Trends>((ref) async {
  final useCase = getIt<GetTrendsUseCase>();
  return await useCase();
});

final topIngredientsProvider = FutureProvider.family<List<IngredientStat>, int>(
  (ref, topN) async {
    final useCase = getIt<GetTopIngredientsUseCase>();
    return await useCase(topN);
  },
);

final badIngredientsProvider = FutureProvider.family<List<IngredientStat>, Map<String, dynamic>>(
  (ref, params) async {
    final useCase = getIt<GetBadIngredientsUseCase>();
    return await useCase(
      threshold: params['threshold'] as double,
      topN: params['topN'] as int,
    );
  },
);

final recommendationsProvider = FutureProvider.family<List<Recommendation>, Map<String, dynamic>>(
  (ref, params) async {
    final useCase = getIt<GetRecommendationsUseCase>();
    return await useCase(
      params['jobId'] as String,
      topN: params['topN'] as int? ?? 5,
    );
  },
);

final anomaliesProvider = FutureProvider<List<Anomaly>>((ref) async {
  final useCase = getIt<GetAnomaliesUseCase>();
  return await useCase();
});





