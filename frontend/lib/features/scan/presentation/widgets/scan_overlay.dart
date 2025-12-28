import 'dart:ui';
import 'package:flutter/material.dart';
import '../../../../core/widgets/animated_scan_frame.dart';
import '../../../../core/widgets/glassmorphism_card.dart';
import '../../../../core/constants/colors.dart';

/// Overlay complet pour la page de scan avec zone de scan carrée
class ScanOverlay extends StatelessWidget {
  final double scanAreaSize;
  final String instruction;
  final ScanState scanState;

  const ScanOverlay({
    super.key,
    required this.scanAreaSize,
    required this.instruction,
    this.scanState = ScanState.idle,
  });

  @override
  Widget build(BuildContext context) {
    final screenSize = MediaQuery.of(context).size;
    final scanAreaOffset = (screenSize.height - scanAreaSize) / 2;

    return Stack(
      children: [
        // Background overlay avec découpe
        Positioned.fill(
          child: CustomPaint(
            painter: ScanOverlayPainter(
              scanAreaSize: scanAreaSize,
              scanAreaOffset: scanAreaOffset,
            ),
          ),
        ),

        // Zone de scan centrée
        Center(
          child: AnimatedScanFrame(
            size: scanAreaSize,
            color: EcoColors.lightGreen,
            cornerLength: 30,
            cornerThickness: 4,
            borderRadius: 12,
            showScanLine: scanState == ScanState.scanning,
          ),
        ),

        // Instructions dynamiques
        Positioned(
          top: scanAreaOffset + scanAreaSize + 40,
          left: 0,
          right: 0,
          child: Center(
            child: GlassmorphismCard(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              borderRadius: 20,
              backgroundColor: Colors.black,
              child: Text(
                instruction,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
        ),
      ],
    );
  }
}

/// Painter pour l'overlay avec découpe carrée
class ScanOverlayPainter extends CustomPainter {
  final double scanAreaSize;
  final double scanAreaOffset;

  ScanOverlayPainter({
    required this.scanAreaSize,
    required this.scanAreaOffset,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.black.withValues(alpha: 0.6)
      ..style = PaintingStyle.fill;

    // Zone supérieure
    canvas.drawRect(
      Rect.fromLTWH(0, 0, size.width, scanAreaOffset),
      paint,
    );

    // Zone inférieure
    canvas.drawRect(
      Rect.fromLTWH(
        0,
        scanAreaOffset + scanAreaSize,
        size.width,
        size.height - (scanAreaOffset + scanAreaSize),
      ),
      paint,
    );

    // Zone gauche
    final leftOffset = (size.width - scanAreaSize) / 2;
    canvas.drawRect(
      Rect.fromLTWH(
        0,
        scanAreaOffset,
        leftOffset,
        scanAreaSize,
      ),
      paint,
    );

    // Zone droite
    canvas.drawRect(
      Rect.fromLTWH(
        leftOffset + scanAreaSize,
        scanAreaOffset,
        size.width - (leftOffset + scanAreaSize),
        scanAreaSize,
      ),
      paint,
    );
  }

  @override
  bool shouldRepaint(ScanOverlayPainter oldDelegate) =>
      oldDelegate.scanAreaSize != scanAreaSize ||
      oldDelegate.scanAreaOffset != scanAreaOffset;
}

/// États du scan pour les instructions dynamiques
enum ScanState {
  idle,
  scanning,
  detecting,
  captured,
}
