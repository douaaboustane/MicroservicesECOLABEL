import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';

/// Widget pour afficher un ingrédient sous forme de chip
class IngredientChip extends StatelessWidget {
  final String ingredient;
  final bool isHighImpact;

  const IngredientChip({
    super.key,
    required this.ingredient,
    this.isHighImpact = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: isHighImpact
            ? EcoColors.warning.withValues(alpha: 0.1)
            : EcoColors.naturalBeige,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: isHighImpact
              ? EcoColors.warning
              : EcoColors.primaryGreen.withValues(alpha: 0.3),
          width: isHighImpact ? 1.5 : 1,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            ingredient,
            style: const TextStyle(
              fontSize: 14,
              color: Colors.black87,
            ),
          ),
          if (isHighImpact) ...[
            const SizedBox(width: 4),
            Icon(
              Icons.warning_amber_rounded,
              size: 16,
              color: EcoColors.warning,
            ),
          ],
        ],
      ),
    );
  }
}
