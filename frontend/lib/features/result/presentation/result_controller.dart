import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/entities/eco_score.dart';
import '../domain/usecases/get_final_score.dart';
import 'package:ecolabel_ms/features/result/data/mock_data.dart';

/// Controller pour les résultats
class ResultController extends StateNotifier<AsyncValue<EcoScore?>> {
  final GetFinalScore getFinalScore;

  ResultController(this.getFinalScore) : super(const AsyncValue.data(null));

  /// Charge le score final
  Future<void> loadScore(String jobId) async {
    state = const AsyncValue.loading();
    try {
      // Mode test : si jobId commence par "test_", utiliser des données mockées
      if (jobId.startsWith('test_')) {
        // Simuler un délai réseau
        await Future.delayed(const Duration(milliseconds: 500));
        
        // Retourner différents scores selon le jobId
        EcoScore testScore;
        if (jobId == 'test_job_excellent') {
          testScore = MockResultData.excellentScore;
        } else if (jobId == 'test_job_average') {
          testScore = MockResultData.averageScore;
        } else if (jobId == 'test_job_poor') {
          testScore = MockResultData.poorScore;
        } else if (jobId == 'test_job_very_poor') {
          testScore = MockResultData.veryPoorScore;
        } else {
          // Score par défaut (B)
          testScore = MockResultData.createTestScore();
        }
        
        state = AsyncValue.data(testScore);
        return;
      }
      
      // Mode normal : appeler l'API
      final score = await getFinalScore(jobId);
      state = AsyncValue.data(score);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }
}
