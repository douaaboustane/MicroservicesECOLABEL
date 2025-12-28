import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/eco_card.dart';
import '../../domain/entities/eco_score.dart';

/// Widget pour les messages éducatifs selon le score
class ScoreMessageCard extends StatelessWidget {
  final EcoScore score;

  const ScoreMessageCard({
    super.key,
    required this.score,
  });

  String _getMessage() {
    switch (score.scoreLetter) {
      case 'A':
      case 'B':
        return 'Excellent choix ! Ce produit a un impact environnemental faible.';
      case 'C':
        return 'Score moyen. Ce produit peut être amélioré, mais reste acceptable.';
      case 'D':
      case 'E':
        return 'Ce produit a un impact élevé. Voici de meilleures alternatives.';
      default:
        return '';
    }
  }

  Color _getMessageColor() {
    switch (score.scoreLetter) {
      case 'A':
      case 'B':
        return EcoColors.primaryGreen;
      case 'C':
        return EcoColors.scoreC;
      case 'D':
      case 'E':
        return EcoColors.scoreD;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    final message = _getMessage();
    if (message.isEmpty) return const SizedBox.shrink();

    final messageColor = _getMessageColor();
    final isLowScore = ['D', 'E'].contains(score.scoreLetter);

    return EcoCard(
      padding: const EdgeInsets.all(20),
      child: Row(
        children: [
          Icon(
            isLowScore ? Icons.lightbulb_outline : Icons.check_circle_outline,
            color: messageColor,
            size: 24,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              message,
              style: EcoTypography.bodyMedium.copyWith(
                color: messageColor,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
