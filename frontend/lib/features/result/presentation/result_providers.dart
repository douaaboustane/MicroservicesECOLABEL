import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../injection_container.dart' as di;
import 'result_controller.dart';
import '../domain/usecases/get_final_score.dart';
import '../domain/entities/eco_score.dart';

/// Provider pour le controller de résultats
final resultControllerProvider =
    StateNotifierProvider<ResultController, AsyncValue<EcoScore?>>((ref) {
  // Vérifier que GetIt est initialisé
  if (!di.getIt.isRegistered<GetFinalScore>()) {
    throw StateError(
      'GetFinalScore is not registered. Make sure setupDependencyInjection() is called before using this provider.',
    );
  }
  return ResultController(di.getIt<GetFinalScore>());
});

