import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lottie/lottie.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/widgets/glassmorphism_card.dart';
import '../../../../injection_container.dart' as di;
import '../../data/datasources/job_polling_ds.dart' show JobStatus;
import '../../domain/usecases/track_job_status.dart';
import '../processing_controller.dart';
import '../widgets/processing_stepper_v2.dart';
import '../../../../core/widgets/error_state.dart';

/// Page de traitement améliorée avec animations Lottie
class ProcessingPageV2 extends ConsumerStatefulWidget {
  final String jobId;

  const ProcessingPageV2({
    super.key,
    required this.jobId,
  });

  @override
  ConsumerState<ProcessingPageV2> createState() => _ProcessingPageV2State();
}

class _ProcessingPageV2State extends ConsumerState<ProcessingPageV2> {
  int _currentTipIndex = 0;
  final List<String> _ecoTips = [
    'Le saviez-vous? Les produits locaux réduisent l\'empreinte carbone de 30%',
    'Astuce: Privilégiez les produits de saison pour un impact environnemental réduit',
    'Info: Un produit avec score A émet 50% moins de CO₂ qu\'un produit avec score E',
    'Conseil: Vérifiez toujours l\'origine et la traçabilité de vos produits',
  ];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(processingControllerProvider.notifier).startTracking(widget.jobId);
    });

    // Rotation des tips toutes les 3 secondes
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) {
        setState(() {
          _currentTipIndex = (_currentTipIndex + 1) % _ecoTips.length;
        });
        _rotateTips();
      }
    });
  }

  void _rotateTips() {
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) {
        setState(() {
          _currentTipIndex = (_currentTipIndex + 1) % _ecoTips.length;
        });
        _rotateTips();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(processingControllerProvider);

    return Scaffold(
      backgroundColor: EcoColors.naturalBeige,
      appBar: AppBar(
        title: Text(
          EcoStrings.processingTitle,
          style: const TextStyle(color: EcoColors.primaryGreen),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: const IconThemeData(color: EcoColors.primaryGreen),
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

          return SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                // Animation centrale
                _buildAnimationSection(status),

                const SizedBox(height: 48),

                // Titre
                Text(
                  EcoStrings.processingSubtitle,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: EcoColors.primaryGreen,
                  ),
                  textAlign: TextAlign.center,
                ),

                const SizedBox(height: 48),

                // Timeline style subway map
                ProcessingStepperV2(currentStatus: status),

                const SizedBox(height: 32),

                // Card avec tips écologiques
                _buildEcoTipCard(),
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

  Widget _buildAnimationSection(JobStatus status) {
    // Animation Lottie ou animation custom selon le statut
    return Container(
      width: 200,
      height: 200,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: LinearGradient(
          colors: [
            EcoColors.primaryGreen.withValues(alpha: 0.1),
            EcoColors.scientificBlue.withValues(alpha: 0.1),
          ],
        ),
      ),
      child: Stack(
        alignment: Alignment.center,
        children: [
          // Animation de feuilles qui tournent (fallback si Lottie non disponible)
          _buildCustomAnimation(status),
        ],
      ),
    );
  }

  Widget _buildCustomAnimation(JobStatus status) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0.0, end: 1.0),
      duration: const Duration(seconds: 2),
      curve: Curves.easeInOut,
      builder: (context, value, child) {
        return Transform.rotate(
          angle: value * 2 * 3.14159,
          child: Icon(
            Icons.eco,
            size: 120,
            color: EcoColors.primaryGreen.withValues(alpha: 0.6),
          ),
        );
      },
      onEnd: () {
        if (mounted) {
          setState(() {});
        }
      },
    );
  }

  Widget _buildEcoTipCard() {
    return AnimatedSwitcher(
      duration: const Duration(milliseconds: 500),
      child: GlassmorphismCard(
        key: ValueKey(_currentTipIndex),
        padding: const EdgeInsets.all(20),
        borderRadius: 20,
        backgroundColor: EcoColors.primaryGreen,
        child: Row(
          children: [
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: EcoColors.lightGreen.withValues(alpha: 0.3),
                shape: BoxShape.circle,
              ),
              child: const Icon(
                Icons.lightbulb_outline,
                color: EcoColors.lightGreen,
                size: 28,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Le saviez-vous?',
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: EcoColors.lightGreen,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    _ecoTips[_currentTipIndex],
                    style: const TextStyle(
                      fontSize: 14,
                      color: Colors.white,
                      height: 1.4,
                    ),
                  ),
                ],
              ),
            ),
          ],
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

