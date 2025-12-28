import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../injection_container.dart' as di;
import '../../data/datasources/job_polling_ds.dart' show JobStatus;
import '../../domain/usecases/track_job_status.dart';
import '../processing_controller.dart';
import '../widgets/processing_stepper.dart';
import '../../../../core/widgets/error_state.dart';
import '../../../../core/constants/strings.dart';

/// Page de traitement
class ProcessingPage extends ConsumerStatefulWidget {
  final String jobId;

  const ProcessingPage({
    super.key,
    required this.jobId,
  });

  @override
  ConsumerState<ProcessingPage> createState() => _ProcessingPageState();
}

class _ProcessingPageState extends ConsumerState<ProcessingPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(processingControllerProvider.notifier).startTracking(widget.jobId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(processingControllerProvider);

    return Scaffold(
      backgroundColor: EcoColors.naturalBeige,
      appBar: AppBar(
        title: const Text(EcoStrings.processingTitle),
      ),
      body: state.when(
        data: (status) {
          if (status == JobStatus.done) {
            // Rediriger vers la page de résultat
            WidgetsBinding.instance.addPostFrameCallback((_) {
              Navigator.pushReplacementNamed(
                context,
                AppRoutes.result,
                arguments: widget.jobId,
              );
            });
          }

          return Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const CircularProgressIndicator(),
                const SizedBox(height: 32),
                Text(
                  EcoStrings.processingSubtitle,
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 48),
                ProcessingStepper(currentStatus: status),
              ],
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => ErrorState(
          title: 'Erreur lors du traitement',
          message: _getProcessingErrorMessage(error),
          technicalDetails: error.toString(),
          actionLabel: 'Réessayer',
          icon: Icons.refresh,
          onAction: () {
            ref.read(processingControllerProvider.notifier).startTracking(widget.jobId);
          },
        ),
      ),
    );
  }
  
  String _getProcessingErrorMessage(Object error) {
    final errorStr = error.toString().toLowerCase();
    if (errorStr.contains('timeout')) {
      return 'L\'analyse prend plus de temps que prévu. Le traitement peut encore être en cours.';
    }
    if (errorStr.contains('network') || errorStr.contains('connection')) {
      return 'Problème de connexion. Vérifiez votre internet et réessayez.';
    }
    return 'Une erreur est survenue lors du traitement. Veuillez réessayer.';
  }
}

// Provider pour le controller
final processingControllerProvider =
    StateNotifierProvider<ProcessingController, AsyncValue<JobStatus>>((ref) {
  return ProcessingController(di.getIt<TrackJobStatus>());
});
