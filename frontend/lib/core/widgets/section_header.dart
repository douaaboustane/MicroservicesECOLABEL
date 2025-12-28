import 'package:flutter/material.dart';
import '../constants/colors.dart';
import '../constants/typography.dart';

/// Widget pour les en-têtes de section avec icône et action optionnelle
class SectionHeader extends StatelessWidget {
  final String title;
  final IconData icon;
  final VoidCallback? onActionTap;
  final String? actionLabel;

  const SectionHeader({
    super.key,
    required this.title,
    required this.icon,
    this.onActionTap,
    this.actionLabel,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(
        children: [
          Icon(
            icon,
            color: EcoColors.primaryGreen,
            size: 24,
          ),
          const SizedBox(width: 12),
          Text(
            title,
            style: EcoTypography.h3.copyWith(
              color: EcoColors.primaryGreen,
            ),
          ),
          const Spacer(),
          if (onActionTap != null && actionLabel != null)
            TextButton(
              onPressed: onActionTap,
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    actionLabel!,
                    style: EcoTypography.bodyMedium.copyWith(
                      color: EcoColors.primaryGreen,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(width: 4),
                  Icon(
                    Icons.arrow_forward_ios,
                    size: 14,
                    color: EcoColors.primaryGreen,
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}

