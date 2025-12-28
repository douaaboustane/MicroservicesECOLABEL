import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../constants/colors.dart';
import '../constants/typography.dart';

/// Widget pour la confirmation implicite après une action réussie
class SuccessConfirmation extends StatelessWidget {
  final String message;
  final IconData icon;
  final Color? color;

  const SuccessConfirmation({
    super.key,
    required this.message,
    this.icon = Icons.check_circle,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    final confirmationColor = color ?? EcoColors.primaryGreen;
    
    // Haptic feedback
    HapticFeedback.lightImpact();
    
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      decoration: BoxDecoration(
        color: confirmationColor.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: confirmationColor.withValues(alpha: 0.3),
          width: 1.5,
        ),
      ),
      child: Row(
        children: [
          Icon(
            icon,
            color: confirmationColor,
            size: 24,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              message,
              style: EcoTypography.bodyMedium.copyWith(
                color: confirmationColor,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
}


