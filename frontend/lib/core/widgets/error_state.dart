import 'package:flutter/material.dart';
import '../constants/colors.dart';
import '../constants/typography.dart';
import 'eco_button.dart';

/// Widget pour les erreurs pédagogiques (pas juste "error 500")
class ErrorState extends StatelessWidget {
  final String title;
  final String message;
  final String? technicalDetails;
  final String actionLabel;
  final VoidCallback onAction;
  final IconData icon;

  const ErrorState({
    super.key,
    required this.title,
    required this.message,
    this.technicalDetails,
    required this.actionLabel,
    required this.onAction,
    this.icon = Icons.error_outline,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                color: EcoColors.error.withValues(alpha: 0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                icon,
                size: 50,
                color: EcoColors.error,
              ),
            ),
            const SizedBox(height: 24),
            Text(
              title,
              style: EcoTypography.h3.copyWith(
                color: EcoColors.error,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            Text(
              message,
              style: EcoTypography.bodyMedium.copyWith(
                color: Colors.grey[700],
              ),
              textAlign: TextAlign.center,
            ),
            if (technicalDetails != null) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  technicalDetails!,
                  style: EcoTypography.bodySmall.copyWith(
                    color: Colors.grey[600],
                    fontFamily: 'monospace',
                  ),
                ),
              ),
            ],
            const SizedBox(height: 32),
            EcoButton(
              text: actionLabel,
              icon: Icons.refresh,
              onPressed: onAction,
            ),
          ],
        ),
      ),
    );
  }
}


