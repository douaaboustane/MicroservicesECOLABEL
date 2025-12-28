import 'package:flutter/material.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/widgets/eco_button.dart';

/// Widget pour les actions utilisateur (CTA)
class ResultActions extends StatelessWidget {
  final VoidCallback? onScanAnother;
  final VoidCallback? onCompare;
  final VoidCallback? onAddToFavorites;
  final VoidCallback? onViewMethodology;
  final VoidCallback? onReportError;

  const ResultActions({
    super.key,
    this.onScanAnother,
    this.onCompare,
    this.onAddToFavorites,
    this.onViewMethodology,
    this.onReportError,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Boutons principaux
        EcoButton(
          text: 'Scanner un autre produit',
          icon: Icons.qr_code_scanner,
          onPressed: onScanAnother ?? () {
            Navigator.pushNamedAndRemoveUntil(
              context,
              AppRoutes.home,
              (route) => false,
            );
          },
        ),
        const SizedBox(height: 32),
        EcoButton(
          text: 'Voir la provenance & méthodologie',
          icon: Icons.info_outline,
          isPrimary: false,
          onPressed: onViewMethodology ?? () {
            Navigator.pushNamed(context, AppRoutes.methodology);
          },
        ),
        const SizedBox(height: 12),
        // Bouton secondaire
        TextButton.icon(
          onPressed: onReportError,
          icon: const Icon(Icons.report_problem_outlined),
          label: const Text('Signaler une erreur'),
          style: TextButton.styleFrom(
            foregroundColor: Colors.grey[600],
          ),
        ),
      ],
    );
  }
}
