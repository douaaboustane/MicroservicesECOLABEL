import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/widgets/eco_card.dart';
import '../../domain/entities/eco_score.dart';

/// Widget pour les 3 cartes d'indicateurs environnementaux horizontales
class ImpactCardsRow extends StatelessWidget {
  final EcoScore score;

  const ImpactCardsRow({
    super.key,
    required this.score,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: _ImpactCard(
            icon: Icons.cloud,
            color: EcoColors.co2Color,
            value: score.co2,
            unit: EcoStrings.unitCo2,
            label: 'CO₂',
          ),
        ),
        const SizedBox(width: 8), // Réduit de 12 à 8
        Expanded(
          child: _ImpactCard(
            icon: Icons.water_drop,
            color: EcoColors.waterColor,
            value: score.water,
            unit: EcoStrings.unitWater,
            label: 'Eau',
          ),
        ),
        const SizedBox(width: 8), // Réduit de 12 à 8
        Expanded(
          child: _ImpactCard(
            icon: Icons.bolt,
            color: EcoColors.energyColor,
            value: score.energy,
            unit: EcoStrings.unitEnergy,
            label: 'Énergie',
          ),
        ),
      ],
    );
  }
}

class _ImpactCard extends StatelessWidget {
  final IconData icon;
  final Color color;
  final double value;
  final String unit;
  final String label;

  const _ImpactCard({
    required this.icon,
    required this.color,
    required this.value,
    required this.unit,
    required this.label,
  });

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
        ],
      ),
    );
  }
}
