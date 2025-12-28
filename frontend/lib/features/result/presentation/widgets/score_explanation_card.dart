import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/eco_card.dart';
import '../../../../core/utils/score_mapper.dart';
import '../../domain/entities/eco_score.dart';

/// Widget pour l'explication pédagogique du score (expandable)
class ScoreExplanationCard extends StatefulWidget {
  final EcoScore score;

  const ScoreExplanationCard({
    super.key,
    required this.score,
  });

  @override
  State<ScoreExplanationCard> createState() => _ScoreExplanationCardState();
}

class _ScoreExplanationCardState extends State<ScoreExplanationCard> {
  bool _isExpanded = false;

  String _generateExplanation(EcoScore score) {
    final explanations = <String>[];
    
    if (score.co2 > 2.0) {
      explanations.add('émissions de CO₂ élevées');
    }
    if (score.water > 500) {
      explanations.add('consommation d\'eau importante');
    }
    if (score.energy > 10) {
      explanations.add('énergie de transformation moyenne à élevée');
    }
    
    if (explanations.isEmpty) {
      return 'Ce produit obtient un score ${score.scoreLetter} grâce à un impact environnemental globalement modéré.';
    }
    
    return 'Ce produit obtient un score ${score.scoreLetter} en raison d\'une ${explanations.join(' et d\'une ')}.';
  }

  @override
  Widget build(BuildContext context) {
    final explanation = _generateExplanation(widget.score);
    
    return EcoCard(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          InkWell(
            onTap: () {
              setState(() {
                _isExpanded = !_isExpanded;
              });
            },
            child: Row(
              children: [
                Icon(
                  Icons.info_outline,
                  color: EcoColors.scientificBlue,
                  size: 20,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'Pourquoi ce score ?',
                    style: EcoTypography.h4.copyWith(
                      color: EcoColors.scientificBlue,
                    ),
                  ),
                ),
                Icon(
                  _isExpanded ? Icons.expand_less : Icons.expand_more,
                  color: EcoColors.scientificBlue,
                ),
              ],
            ),
          ),
          if (_isExpanded) ...[
            const SizedBox(height: 12),
            Text(
              explanation,
              style: EcoTypography.bodyMedium.copyWith(
                color: Colors.grey[700],
                height: 1.5,
              ),
            ),
          ],
        ],
      ),
    );
  }
}
