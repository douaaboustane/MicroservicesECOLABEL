import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/eco_button.dart';

/// Page d'accueil stylisée
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Logo avec glow
              Container(
                width: 130,
                height: 130,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: const LinearGradient(
                    colors: [
                      EcoColors.primaryGreen,
                      EcoColors.lightGreen,
                    ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: EcoColors.primaryGreen.withValues(alpha: 0.35),
                      blurRadius: 24,
                      offset: const Offset(0, 12),
                    ),
                  ],
                ),
                child: const Icon(
                  Icons.eco,
                  size: 64,
                  color: Colors.white,
                ),
              ),

              const SizedBox(height: 36),

              // Nom de l'app
              Text(
                EcoStrings.appName,
                style: EcoTypography.h1.copyWith(
                  color: EcoColors.primaryGreen,
                  letterSpacing: 0.6,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 10),

              // Tagline
              Text(
                'Comprenez l\'impact environnemental de vos produits alimentaires',
                style: EcoTypography.bodyLarge.copyWith(
                  color: Colors.grey.shade600,
                  height: 1.5,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 72),

              // CTA principal
              EcoButton(
                text: EcoStrings.scanButton,
                icon: Icons.qr_code_scanner,
                onPressed: () {
                  HapticFeedback.mediumImpact();
                  Navigator.pushNamed(context, AppRoutes.scan);
                },
              ),

              const SizedBox(height: 18),

              // CTA secondaire
              EcoButton(
                text: EcoStrings.uploadButton,
                icon: Icons.upload_file_rounded,
                isPrimary: false,
                onPressed: () {
                  HapticFeedback.lightImpact();
                  Navigator.pushNamed(context, AppRoutes.scan);
                },
              ),

              const SizedBox(height: 56),

              // Boutons de test (DEV ONLY)
              Column(
                children: [
                  Text(
                    'Mode Test (DEV ONLY)',
                    style: EcoTypography.bodySmall.copyWith(
                      color: Colors.grey[600],
                    ),
                  ),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    alignment: WrapAlignment.center,
                    children: [
                      _TestButton(
                        label: 'Score A',
                        color: EcoColors.scoreA,
                        jobId: 'test_job_excellent',
                      ),
                      _TestButton(
                        label: 'Score B',
                        color: EcoColors.scoreB,
                        jobId: 'test_job',
                      ),
                      _TestButton(
                        label: 'Score C',
                        color: EcoColors.scoreC,
                        jobId: 'test_job_average',
                      ),
                      _TestButton(
                        label: 'Score D',
                        color: EcoColors.scoreD,
                        jobId: 'test_job_poor',
                      ),
                      _TestButton(
                        label: 'Score E',
                        color: EcoColors.scoreE,
                        jobId: 'test_job_very_poor',
                      ),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/// Bouton de test pour différents scores
class _TestButton extends StatelessWidget {
  final String label;
  final Color color;
  final String jobId;

  const _TestButton({
    required this.label,
    required this.color,
    required this.jobId,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {
        Navigator.pushNamed(
          context,
          AppRoutes.result,
          arguments: jobId,
        );
      },
      borderRadius: BorderRadius.circular(20),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.1),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: color, width: 1.5),
        ),
        child: Text(
          label,
          style: EcoTypography.bodySmall.copyWith(
            color: color,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}
