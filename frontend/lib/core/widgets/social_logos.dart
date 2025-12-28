import 'package:flutter/material.dart';

/// Logo Google avec le "G" multicolore
class GoogleLogo extends StatelessWidget {
  final double size;

  const GoogleLogo({super.key, this.size = 24});

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(size, size),
      painter: _GoogleLogoPainter(),
    );
  }
}

class _GoogleLogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width * 0.45;
    final strokeWidth = size.width * 0.18;

    // Fond blanc pour le "G"
    final whitePaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center, radius, whitePaint);

    // Arc bleu (partie supérieure droite du G) - de -45° à 45°
    final bluePaint = Paint()
      ..color = const Color(0xFF4285F4)
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -0.785, // -45 degrés
      1.57, // 90 degrés
      false,
      bluePaint,
    );

    // Arc rouge (partie supérieure gauche du G) - de -135° à -45°
    final redPaint = Paint()
      ..color = const Color(0xFFEA4335)
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -2.356, // -135 degrés
      0.785, // 45 degrés
      false,
      redPaint,
    );

    // Arc jaune (partie inférieure gauche du G) - de 45° à 135°
    final yellowPaint = Paint()
      ..color = const Color(0xFFFBBC05)
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      0.785, // 45 degrés
      0.785, // 45 degrés
      false,
      yellowPaint,
    );

    // Arc vert (partie inférieure droite du G) - de 135° à 180°
    final greenPaint = Paint()
      ..color = const Color(0xFF34A853)
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      2.356, // 135 degrés
      0.785, // 45 degrés
      false,
      greenPaint,
    );

    // Barre horizontale verte du G (la partie qui traverse vers la droite)
    final greenBarPaint = Paint()
      ..color = const Color(0xFF34A853)
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    final barStart = Offset(center.dx + radius * 0.25, center.dy);
    final barEnd = Offset(center.dx + radius * 0.95, center.dy);
    canvas.drawLine(barStart, barEnd, greenBarPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

/// Logo Apple avec sa couleur de marque (noir)
class AppleLogo extends StatelessWidget {
  final double size;

  const AppleLogo({
    super.key,
    this.size = 24,
  });

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(size, size),
      painter: _AppleLogoPainter(),
    );
  }
}

class _AppleLogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.black
      ..style = PaintingStyle.fill;

    // Corps de la pomme - forme plus précise du logo Apple
    final applePath = Path();
    
    // Point de départ (haut centre)
    applePath.moveTo(size.width * 0.5, size.height * 0.05);
    
    // Côté gauche supérieur
    applePath.cubicTo(
      size.width * 0.4, size.height * 0.1,
      size.width * 0.25, size.height * 0.2,
      size.width * 0.22, size.height * 0.35,
    );
    
    // Côté gauche
    applePath.cubicTo(
      size.width * 0.18, size.height * 0.5,
      size.width * 0.2, size.height * 0.65,
      size.width * 0.25, size.height * 0.75,
    );
    
    // Bas gauche
    applePath.cubicTo(
      size.width * 0.3, size.height * 0.85,
      size.width * 0.38, size.height * 0.92,
      size.width * 0.45, size.height * 0.95,
    );
    
    // Bas (creux de la pomme)
    applePath.cubicTo(
      size.width * 0.48, size.height * 0.96,
      size.width * 0.52, size.height * 0.96,
      size.width * 0.55, size.height * 0.95,
    );
    
    // Bas droit
    applePath.cubicTo(
      size.width * 0.62, size.height * 0.92,
      size.width * 0.7, size.height * 0.85,
      size.width * 0.75, size.height * 0.75,
    );
    
    // Côté droit
    applePath.cubicTo(
      size.width * 0.8, size.height * 0.65,
      size.width * 0.82, size.height * 0.5,
      size.width * 0.78, size.height * 0.35,
    );
    
    // Côté droit supérieur
    applePath.cubicTo(
      size.width * 0.75, size.height * 0.2,
      size.width * 0.6, size.height * 0.1,
      size.width * 0.5, size.height * 0.05,
    );
    applePath.close();

    canvas.drawPath(applePath, paint);

    // Morsure (bite) - partie droite
    final bitePath = Path();
    bitePath.moveTo(size.width * 0.68, size.height * 0.25);
    bitePath.cubicTo(
      size.width * 0.7, size.height * 0.28,
      size.width * 0.72, size.height * 0.32,
      size.width * 0.7, size.height * 0.36,
    );
    bitePath.cubicTo(
      size.width * 0.68, size.height * 0.32,
      size.width * 0.66, size.height * 0.28,
      size.width * 0.68, size.height * 0.25,
    );
    bitePath.close();
    
    // Dessiner la morsure en blanc pour créer le creux
    final whitePaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.fill;
    canvas.drawPath(bitePath, whitePaint);

    // Feuille
    final leafPath = Path();
    leafPath.moveTo(size.width * 0.5, size.height * 0.05);
    leafPath.cubicTo(
      size.width * 0.52, size.height * 0.0,
      size.width * 0.58, size.height * 0.02,
      size.width * 0.62, size.height * 0.1,
    );
    leafPath.cubicTo(
      size.width * 0.6, size.height * 0.15,
      size.width * 0.55, size.height * 0.12,
      size.width * 0.5, size.height * 0.05,
    );
    leafPath.close();

    canvas.drawPath(leafPath, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

/// Logo Microsoft avec ses couleurs de marque
class MicrosoftLogo extends StatelessWidget {
  final double size;

  const MicrosoftLogo({super.key, this.size = 24});

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(size, size),
      painter: _MicrosoftLogoPainter(),
    );
  }
}

class _MicrosoftLogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final squareSize = size.width / 2;
    final paint = Paint()..style = PaintingStyle.fill;

    // Carré rouge (en haut à gauche)
    paint.color = const Color(0xFFF25022);
    canvas.drawRect(
      Rect.fromLTWH(0, 0, squareSize, squareSize),
      paint,
    );

    // Carré vert (en haut à droite)
    paint.color = const Color(0xFF7FBA00);
    canvas.drawRect(
      Rect.fromLTWH(squareSize, 0, squareSize, squareSize),
      paint,
    );

    // Carré bleu (en bas à gauche)
    paint.color = const Color(0xFF00A4EF);
    canvas.drawRect(
      Rect.fromLTWH(0, squareSize, squareSize, squareSize),
      paint,
    );

    // Carré jaune (en bas à droite)
    paint.color = const Color(0xFFFFB900);
    canvas.drawRect(
      Rect.fromLTWH(squareSize, squareSize, squareSize, squareSize),
      paint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}


