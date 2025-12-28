import 'dart:ui';
import 'package:flutter/material.dart';

/// Widget de cadre de scan animé avec coins et ligne de scan
class AnimatedScanFrame extends StatefulWidget {
  final double size;
  final Color color;
  final double cornerLength;
  final double cornerThickness;
  final double borderRadius;
  final bool showScanLine;
  final Duration scanLineDuration;

  const AnimatedScanFrame({
    super.key,
    required this.size,
    this.color = const Color(0xFF66BB6A),
    this.cornerLength = 30.0,
    this.cornerThickness = 4.0,
    this.borderRadius = 12.0,
    this.showScanLine = true,
    this.scanLineDuration = const Duration(seconds: 2),
  });

  @override
  State<AnimatedScanFrame> createState() => _AnimatedScanFrameState();
}

class _AnimatedScanFrameState extends State<AnimatedScanFrame>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  late AnimationController _scanLineController;
  late Animation<double> _pulseAnimation;
  late Animation<double> _scanLineAnimation;

  @override
  void initState() {
    super.initState();

    // Animation de pulse pour les coins
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 0.6, end: 1.0).animate(
      CurvedAnimation(
        parent: _pulseController,
        curve: Curves.easeInOut,
      ),
    );

    // Animation de la ligne de scan
    _scanLineController = AnimationController(
      duration: widget.scanLineDuration,
      vsync: this,
    )..repeat();

    _scanLineAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: _scanLineController,
        curve: Curves.linear,
      ),
    );
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _scanLineController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.size,
      height: widget.size,
      child: Stack(
        children: [
          // Ligne de scan animée
          if (widget.showScanLine)
            AnimatedBuilder(
              animation: _scanLineAnimation,
              builder: (context, child) {
                final scanLineY = widget.size * _scanLineAnimation.value;
                return Positioned(
                  top: scanLineY - 1,
                  left: 0,
                  right: 0,
                  child: Container(
                    height: 2,
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          Colors.transparent,
                          widget.color.withValues(alpha: 0.5),
                          widget.color.withValues(alpha: 0.5),
                          Colors.transparent,
                        ],
                        stops: const [0.0, 0.3, 0.7, 1.0],
                      ),
                    ),
                  ),
                );
              },
            ),

          // Coins animés
          AnimatedBuilder(
            animation: _pulseAnimation,
            builder: (context, child) {
              final opacity = _pulseAnimation.value;
              return CustomPaint(
                painter: ScanFramePainter(
                  color: widget.color.withValues(alpha: opacity),
                  cornerLength: widget.cornerLength,
                  cornerThickness: widget.cornerThickness,
                  borderRadius: widget.borderRadius,
                ),
                size: Size(widget.size, widget.size),
              );
            },
          ),
        ],
      ),
    );
  }
}

/// Painter pour dessiner les coins du cadre de scan
class ScanFramePainter extends CustomPainter {
  final Color color;
  final double cornerLength;
  final double cornerThickness;
  final double borderRadius;

  ScanFramePainter({
    required this.color,
    required this.cornerLength,
    required this.cornerThickness,
    required this.borderRadius,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = cornerThickness
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    final glowPaint = Paint()
      ..color = color.withValues(alpha: 0.3)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 5);

    // Coin supérieur gauche
    _drawCorner(
      canvas,
      paint,
      glowPaint,
      Offset(0, 0),
      Offset(cornerLength, 0),
      Offset(0, cornerLength),
    );

    // Coin supérieur droit
    _drawCorner(
      canvas,
      paint,
      glowPaint,
      Offset(size.width, 0),
      Offset(size.width - cornerLength, 0),
      Offset(size.width, cornerLength),
    );

    // Coin inférieur gauche
    _drawCorner(
      canvas,
      paint,
      glowPaint,
      Offset(0, size.height),
      Offset(0, size.height - cornerLength),
      Offset(cornerLength, size.height),
    );

    // Coin inférieur droit
    _drawCorner(
      canvas,
      paint,
      glowPaint,
      Offset(size.width, size.height),
      Offset(size.width, size.height - cornerLength),
      Offset(size.width - cornerLength, size.height),
    );
  }

  void _drawCorner(
    Canvas canvas,
    Paint paint,
    Paint glowPaint,
    Offset corner,
    Offset horizontalEnd,
    Offset verticalEnd,
  ) {
    // Glow effect
    canvas.drawLine(corner, horizontalEnd, glowPaint);
    canvas.drawLine(corner, verticalEnd, glowPaint);

    // Main lines
    canvas.drawLine(corner, horizontalEnd, paint);
    canvas.drawLine(corner, verticalEnd, paint);
  }

  @override
  bool shouldRepaint(ScanFramePainter oldDelegate) =>
      oldDelegate.color != color ||
      oldDelegate.cornerLength != cornerLength ||
      oldDelegate.cornerThickness != cornerThickness;
}

