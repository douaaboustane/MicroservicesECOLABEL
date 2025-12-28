import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/utils/score_mapper.dart';
import '../../domain/entities/eco_score.dart';

/// Widget pour le score écologique (élément STAR)
class StarScoreCard extends StatefulWidget {
  final EcoScore score;

  const StarScoreCard({
    super.key,
    required this.score,
  });

  @override
  State<StarScoreCard> createState() => _StarScoreCardState();
}

class _StarScoreCardState extends State<StarScoreCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );

    // Animation conditionnelle sera appliquée dans build()
    _scaleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: _controller,
        curve: Curves.elasticOut, // Par défaut, sera ajusté selon score
      ),
    );

    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: _controller,
        curve: Curves.easeIn,
      ),
    );

    _controller.forward();
    HapticFeedback.lightImpact();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final scoreColor = EcoColors.getScoreColor(widget.score.scoreLetter);
    final description = ScoreMapper.getScoreDescription(widget.score.scoreLetter);
    
    // Animation conditionnelle selon le score
    final isPositiveScore = ['A', 'B'].contains(widget.score.scoreLetter);
    final animationCurve = isPositiveScore 
        ? Curves.elasticOut  // Animation positive pour A-B
        : Curves.easeOut;     // Animation douce pour C-D-E

    return FadeTransition(
      opacity: _fadeAnimation,
      child: ScaleTransition(
        scale: _scaleAnimation,
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 32),
          padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 40),
          decoration: BoxDecoration(
            // Gradient subtil derrière le score
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                scoreColor.withValues(alpha: 0.15),
                scoreColor.withValues(alpha: 0.05),
                Colors.transparent,
              ],
            ),
            borderRadius: BorderRadius.circular(40),
            border: Border.all(
              color: scoreColor.withValues(alpha: 0.4),
              width: 3,
            ),
            // Glow effect pour les bons scores
            boxShadow: isPositiveScore
                ? [
                    BoxShadow(
                      color: scoreColor.withValues(alpha: 0.3),
                      blurRadius: 30,
                      spreadRadius: 5,
                    ),
                  ]
                : null,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Lettre du score (réduite pour éviter l'overflow)
              FittedBox(
                fit: BoxFit.scaleDown,
                child: Text(
                  widget.score.scoreLetter,
                  style: TextStyle(
                    fontSize: 130,
                    fontWeight: FontWeight.bold,
                    color: scoreColor,
                    height: 1.0,
                    letterSpacing: -8,
                    shadows: [
                      Shadow(
                        color: scoreColor.withValues(alpha: 0.3),
                        blurRadius: 20,
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 10),
              // Note numérique
              FittedBox(
                fit: BoxFit.scaleDown,
                child: Text(
                  '${widget.score.scoreNumeric} / 100',
                  style: EcoTypography.h1.copyWith(
                    color: scoreColor,
                    fontWeight: FontWeight.bold,
                    fontSize: 26,
                  ),
                ),
              ),
              const SizedBox(height: 6),
              // Description
              Text(
                description,
                style: EcoTypography.h3.copyWith(
                  color: scoreColor,
                  fontWeight: FontWeight.w600,
                  fontSize: 14,
                ),
                textAlign: TextAlign.center,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
