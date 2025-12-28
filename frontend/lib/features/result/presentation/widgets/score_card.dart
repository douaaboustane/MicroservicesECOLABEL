import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/utils/score_mapper.dart';
import '../../domain/entities/eco_score.dart';

/// Widget pour afficher le score écologique
class ScoreCard extends StatelessWidget {
  final EcoScore score;

  const ScoreCard({
    super.key,
    required this.score,
  });

  @override
  Widget build(BuildContext context) {
    final scoreColor = EcoColors.getScoreColor(score.scoreLetter);
    final description = ScoreMapper.getScoreDescription(score.scoreLetter);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: scoreColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: scoreColor, width: 3),
      ),
      child: Column(
        children: [
          Text(
            score.scoreLetter,
            style: EcoTypography.scoreLetter.copyWith(color: scoreColor),
          ),
          const SizedBox(height: 8),
          Text(
            '${score.scoreNumeric}/100',
            style: EcoTypography.scoreNumber.copyWith(color: scoreColor),
          ),
          const SizedBox(height: 8),
          Text(
            description,
            style: EcoTypography.h3.copyWith(color: scoreColor),
          ),
        ],
      ),
    );
  }
}
