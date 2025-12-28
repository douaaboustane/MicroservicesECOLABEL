import '../../../../core/network/api_client.dart';

/// Statuts possibles d'un job
enum JobStatus {
  pending,
  ocr,
  nlp,
  acv,
  score,
  done,
  error,
}

/// Source de données pour le polling des jobs
class JobPollingDataSource {
  final ApiClient apiClient;

  JobPollingDataSource(this.apiClient);

  /// Récupère le statut d'un job
  /// 
  /// Utilise l'endpoint backend réel: GET /mobile/products/scan/{job_id}/status
  Future<JobStatus> getJobStatus(String jobId) async {
    final response = await apiClient.get<Map<String, dynamic>>(
      '/mobile/products/scan/$jobId/status',
    );

    final status = response.data!['status'] as String;
    return _mapStatus(status);
  }

  JobStatus _mapStatus(String status) {
    switch (status.toUpperCase()) {
      case 'PENDING':
        return JobStatus.pending;
      case 'PROCESSING':
        // Le backend utilise "PROCESSING" comme statut générique
        // On peut essayer de déterminer l'étape depuis le résultat si disponible
        // Pour l'instant, on retourne OCR comme étape par défaut
        return JobStatus.ocr;
      case 'OCR':
      case 'OCR_PROCESSING':
        return JobStatus.ocr;
      case 'NLP':
      case 'NLP_PROCESSING':
        return JobStatus.nlp;
      case 'ACV':
      case 'ACV_PROCESSING':
        return JobStatus.acv;
      case 'SCORE':
      case 'SCORE_PROCESSING':
        return JobStatus.score;
      case 'DONE':
      case 'COMPLETED':
        return JobStatus.done;
      case 'ERROR':
      case 'FAILED':
        return JobStatus.error;
      default:
        return JobStatus.pending;
    }
  }
}
