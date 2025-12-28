import '../../../../core/config/env.dart';
import '../../data/datasources/job_polling_ds.dart';

/// Use case pour suivre le statut d'un job
class TrackJobStatus {
  final JobPollingDataSource dataSource;

  TrackJobStatus(this.dataSource);

  /// Stream du statut du job avec polling automatique
  Stream<JobStatus> call(String jobId) async* {
    final startTime = DateTime.now();

    while (true) {
      // Vérifier le timeout
      if (DateTime.now().difference(startTime) > Env.pollingTimeout) {
        yield JobStatus.error;
        break;
      }

      final status = await dataSource.getJobStatus(jobId);
      yield status;

      // Arrêter le polling si le job est terminé ou en erreur
      if (status == JobStatus.done || status == JobStatus.error) {
        break;
      }

      // Attendre avant le prochain poll
      await Future.delayed(Env.pollingInterval);
    }
  }
}
