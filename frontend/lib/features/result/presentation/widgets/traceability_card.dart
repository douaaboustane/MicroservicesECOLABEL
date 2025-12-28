import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/eco_card.dart';
import '../../../../core/utils/date_utils.dart' as app_date_utils;
import '../../domain/entities/eco_score.dart';

/// Widget pour la traçabilité et confiance
class TraceabilityCard extends StatelessWidget {
  final EcoScore score;
  final String? modelVersion;
  final String? dataSource;
  final String? originCountry;

  const TraceabilityCard({
    super.key,
    required this.score,
    this.modelVersion,
    this.dataSource,
    this.originCountry,
  });

  @override
  Widget build(BuildContext context) {
    return EcoCard(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                Icons.science,
                color: EcoColors.scientificBlue,
                size: 20,
              ),
              const SizedBox(width: 8),
              Text(
                'Transparence',
                style: EcoTypography.h4.copyWith(
                  color: EcoColors.scientificBlue,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          _buildInfoRow('Date du calcul', app_date_utils.DateUtils.formatDate(score.calculatedAt)),
          if (modelVersion != null)
            _buildInfoRow('Version du modèle', modelVersion!),
          if (dataSource != null)
            _buildInfoRow('Source des données', dataSource!),
          if (originCountry != null)
            _buildInfoRow('Pays d\'origine', originCountry!),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: EcoTypography.bodySmall.copyWith(
                color: Colors.grey[600],
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: EcoTypography.bodyMedium.copyWith(
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
