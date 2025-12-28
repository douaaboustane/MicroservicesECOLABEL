import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/usecases/track_job_status.dart';
import '../data/datasources/job_polling_ds.dart' show JobStatus;

/// Controller pour le suivi du traitement
class ProcessingController extends StateNotifier<AsyncValue<JobStatus>> {
  final TrackJobStatus trackJobStatus;
  Stream<JobStatus>? _statusStream;

  ProcessingController(this.trackJobStatus)
      : super(const AsyncValue.data(JobStatus.pending));

  /// Démarre le suivi du statut
  void startTracking(String jobId) {
    _statusStream = trackJobStatus(jobId);
    _statusStream!.listen(
      (status) {
        state = AsyncValue.data(status);
      },
      onError: (error, stack) {
        state = AsyncValue.error(error, stack);
      },
    );
  }
}
