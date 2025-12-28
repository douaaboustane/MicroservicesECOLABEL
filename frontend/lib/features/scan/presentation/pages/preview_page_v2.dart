import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/glassmorphism_card.dart';
import '../../../../core/widgets/pulse_button.dart';

/// Page de prévisualisation améliorée avec zoom et qualité
class PreviewPageV2 extends StatefulWidget {
  final File imageFile;

  const PreviewPageV2({
    super.key,
    required this.imageFile,
  });

  @override
  State<PreviewPageV2> createState() => _PreviewPageV2State();
}

class _PreviewPageV2State extends State<PreviewPageV2> {
  final TransformationController _transformationController =
      TransformationController();
  int _qualityStars = 4; // Estimation de la qualité

  @override
  void dispose() {
    _transformationController.dispose();
    super.dispose();
  }

  void _resetZoom() {
    _transformationController.value = Matrix4.identity();
    HapticFeedback.lightImpact();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'Vérifier l\'image',
          style: EcoTypography.h3.copyWith(
            color: Colors.white,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.close, color: Colors.white),
            onPressed: () => Navigator.pop(context),
          ),
        ],
      ),
      body: Stack(
        children: [
          // Image avec zoom/pinch
          Center(
            child: InteractiveViewer(
              transformationController: _transformationController,
              minScale: 0.5,
              maxScale: 4.0,
              child: Image.file(
                widget.imageFile,
                fit: BoxFit.contain,
              ),
            ),
          ),

          // Overlay bottom avec infos
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: _buildBottomOverlay(),
          ),

          // Bouton reset zoom (si zoomé)
          Positioned(
            top: 100,
            right: 16,
            child: ValueListenableBuilder<Matrix4>(
              valueListenable: _transformationController,
              builder: (context, matrix, child) {
                final isZoomed = matrix.getMaxScaleOnAxis() > 1.0;
                if (!isZoomed) return const SizedBox.shrink();

                return FloatingActionButton.small(
                  onPressed: _resetZoom,
                  backgroundColor: Colors.black.withValues(alpha: 0.6),
                  child: const Icon(Icons.zoom_out_map, color: Colors.white),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBottomOverlay() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            Colors.transparent,
            Colors.black.withValues(alpha: 0.8),
          ],
        ),
      ),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Qualité de l'image
              GlassmorphismCard(
                padding: const EdgeInsets.all(16),
                borderRadius: 16,
                backgroundColor: Colors.white,
                child: Row(
                  children: [
                    const Icon(
                      Icons.image,
                      color: EcoColors.primaryGreen,
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Qualité de l\'image',
                            style: EcoTypography.bodyMedium.copyWith(
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Row(
                            children: List.generate(
                              5,
                              (index) => Icon(
                                index < _qualityStars
                                    ? Icons.star
                                    : Icons.star_border,
                                color: EcoColors.lightGreen,
                                size: 20,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: EcoColors.lightGreen.withValues(alpha: 0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.check_circle,
                            color: EcoColors.lightGreen,
                            size: 16,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            'Image nette',
                            style: EcoTypography.bodySmall.copyWith(
                              color: EcoColors.lightGreen,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Actions
              Row(
                children: [
                  // Bouton reprendre
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () {
                        HapticFeedback.lightImpact();
                        Navigator.pop(context);
                      },
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        side: const BorderSide(
                          color: Colors.white,
                          width: 2,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: const [
                          Icon(Icons.refresh, color: Colors.white),
                          SizedBox(width: 8),
                          Text(
                            'Reprendre',
                            style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  // Bouton analyser (CTA)
                  Expanded(
                    flex: 2,
                    child: PulseButton(
                      backgroundColor: EcoColors.primaryGreen,
                      glowColor: EcoColors.lightGreen,
                      borderRadius: 16,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      enableHaptic: true,
                      onPressed: () {
                        HapticFeedback.mediumImpact();
                        Navigator.pop(context, widget.imageFile);
                      },
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: const [
                          Icon(Icons.analytics, color: Colors.white),
                          SizedBox(width: 8),
                          Text(
                            'Analyser',
                            style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

