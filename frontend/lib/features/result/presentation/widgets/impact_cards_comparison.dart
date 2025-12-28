import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/widgets/eco_card.dart';
import '../../domain/entities/eco_score.dart';

/// Widget pour les cartes d'impact avec comparaison vs moyenne
class ImpactCardsComparison extends StatelessWidget {
  final EcoScore score;
  final Map<String, double>? averages; // Moyennes par type de produit

  const ImpactCardsComparison({
    super.key,
    required this.score,
    this.averages,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: _ImpactCardWithComparison(
            icon: Icons.cloud,
            color: EcoColors.co2Color,
            value: score.co2,
            unit: EcoStrings.unitCo2,
            label: 'CO₂',
            average: averages?['co2'],
          ),
        ),
        const SizedBox(width: 8), // Réduit de 12 à 8
        Expanded(
          child: _ImpactCardWithComparison(
            icon: Icons.water_drop,
            color: EcoColors.waterColor,
            value: score.water,
            unit: EcoStrings.unitWater,
            label: 'Eau',
            average: averages?['water'],
          ),
        ),
        const SizedBox(width: 8), // Réduit de 12 à 8
        Expanded(
          child: _ImpactCardWithComparison(
            icon: Icons.bolt,
            color: EcoColors.energyColor,
            value: score.energy,
            unit: EcoStrings.unitEnergy,
            label: 'Énergie',
            average: averages?['energy'],
          ),
        ),
      ],
    );
  }
}

class _ImpactCardWithComparison extends StatelessWidget {
  final IconData icon;
  final Color color;
  final double value;
  final String unit;
  final String label;
  final double? average;

  const _ImpactCardWithComparison({
    required this.icon,
    required this.color,
    required this.value,
    required this.unit,
    required this.label,
    this.average,
  });

  bool get isBetterThanAverage {
    if (average == null) return false;
    return value < average!;
  }

  @override
  Widget build(BuildContext context) {
    return EcoCard(
      padding: const EdgeInsets.all(12), // Réduit de 16 à 12
      child: Column(
        mainAxisSize: MainAxisSize.min, // Évite l'expansion
        children: [
          Icon(icon, color: color, size: 28), // Réduit de 32 à 28
          const SizedBox(height: 8), // Réduit de 12 à 8
          Flexible(
            child: Text(
              value.toStringAsFixed(1),
              style: TextStyle(
                fontSize: 18, // Réduit de 20 à 18
                fontWeight: FontWeight.bold,
                color: color,
              ),
              overflow: TextOverflow.ellipsis,
              maxLines: 1,
            ),
          ),
          Text(
            unit,
            style: TextStyle(
              fontSize: 10, // Réduit de 11 à 10
              color: Colors.grey[600],
            ),
            overflow: TextOverflow.ellipsis,
            maxLines: 1,
          ),
          const SizedBox(height: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 11, // Réduit de 12 à 11
              color: Colors.grey[700],
              fontWeight: FontWeight.w500,
            ),
            overflow: TextOverflow.ellipsis,
            maxLines: 1,
          ),
          // Badge de comparaison si moyenne disponible
          if (average != null) ...[
            const SizedBox(height: 6), // Réduit de 8 à 6
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3), // Réduit
              decoration: BoxDecoration(
                color: isBetterThanAverage
                    ? EcoColors.primaryGreen.withValues(alpha: 0.1)
                    : Colors.grey[200],
                borderRadius: BorderRadius.circular(10), // Réduit de 12 à 10
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    isBetterThanAverage ? Icons.trending_down : Icons.trending_up,
                    size: 10,
                    color: isBetterThanAverage
                        ? EcoColors.primaryGreen
                        : Colors.grey[600],
                  ),
                  const SizedBox(width: 2),
                  Text(
                    isBetterThanAverage ? 'Mieux' : 'Moyen', // "Mieux" au lieu de "Meilleur" (plus court)
                    style: TextStyle(
                      fontSize: 9,
                      color: isBetterThanAverage
                          ? EcoColors.primaryGreen
                          : Colors.grey[600],
                      fontWeight: FontWeight.w600,
                    ),
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
}


