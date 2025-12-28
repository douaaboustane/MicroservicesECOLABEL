import 'package:flutter/material.dart';
import '../constants/colors.dart';

/// Widget de fond avec effet de gradient pour toute l'application
class AppBackground extends StatelessWidget {
  final Widget child;
  final bool showPattern;

  const AppBackground({
    super.key,
    required this.child,
    this.showPattern = true,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            EcoColors.naturalBeige,
            EcoColors.offWhite,
            EcoColors.naturalBeige.withValues(alpha: 0.9),
          ],
          stops: const [0.0, 0.5, 1.0],
        ),
      ),
      child: showPattern
          ? Stack(
              children: [
                // Pattern subtil en arrière-plan
                CustomPaint(
                  painter: _BackgroundPatternPainter(),
                  child: Container(),
                ),
                // Contenu
                child,
              ],
            )
          : child,
    );
  }
}

/// Painter pour créer un pattern subtil en arrière-plan
class _BackgroundPatternPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = EcoColors.primaryGreen.withValues(alpha: 0.03)
      ..style = PaintingStyle.fill;

    // Créer un pattern de cercles subtils
    const spacing = 100.0;
    for (double x = 0; x < size.width + spacing; x += spacing) {
      for (double y = 0; y < size.height + spacing; y += spacing) {
        canvas.drawCircle(
          Offset(x, y),
          30,
          paint,
        );
      }
    }

    // Ajouter des lignes subtiles
    final linePaint = Paint()
      ..color = EcoColors.primaryGreen.withValues(alpha: 0.02)
      ..strokeWidth = 1;

    for (double x = 0; x < size.width; x += spacing) {
      canvas.drawLine(
        Offset(x, 0),
        Offset(x, size.height),
        linePaint,
      );
    }

    for (double y = 0; y < size.height; y += spacing) {
      canvas.drawLine(
        Offset(0, y),
        Offset(size.width, y),
        linePaint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

