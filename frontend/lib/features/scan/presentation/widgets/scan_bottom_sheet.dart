import 'dart:ui';
import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';

/// Bottom sheet avec actions de scan (flash, capture, galerie)
class ScanBottomSheet extends StatelessWidget {
  final VoidCallback onCapture;
  final VoidCallback onGallery;
  final VoidCallback? onFlashToggle;
  final bool isFlashOn;
  final bool isCapturing;

  const ScanBottomSheet({
    super.key,
    required this.onCapture,
    required this.onGallery,
    this.onFlashToggle,
    this.isFlashOn = false,
    this.isCapturing = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 100,
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.9),
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(24),
          topRight: Radius.circular(24),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.1),
            blurRadius: 10,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(24),
          topRight: Radius.circular(24),
        ),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                // Flash toggle
                if (onFlashToggle != null)
                  _ActionButton(
                    icon: isFlashOn ? Icons.flash_on : Icons.flash_off,
                    label: 'Flash',
                    onPressed: onFlashToggle!,
                    isActive: isFlashOn,
                  ),

                // Capture button (principal)
                _CaptureButton(
                  onPressed: isCapturing ? null : onCapture,
                  isCapturing: isCapturing,
                ),

                // Gallery button
                _ActionButton(
                  icon: Icons.photo_library,
                  label: 'Galerie',
                  onPressed: onGallery,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// Bouton d'action secondaire
class _ActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onPressed;
  final bool isActive;

  const _ActionButton({
    required this.icon,
    required this.label,
    required this.onPressed,
    this.isActive = false,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: onPressed,
            borderRadius: BorderRadius.circular(30),
            child: Container(
              width: 56,
              height: 56,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isActive
                    ? EcoColors.lightGreen.withValues(alpha: 0.2)
                    : Colors.grey.withValues(alpha: 0.1),
                border: Border.all(
                  color: isActive
                      ? EcoColors.lightGreen
                      : Colors.grey.withValues(alpha: 0.3),
                  width: 2,
                ),
              ),
              child: Icon(
                icon,
                color: isActive ? EcoColors.lightGreen : Colors.grey[700],
                size: 24,
              ),
            ),
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey[600],
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }
}

/// Bouton de capture principal
class _CaptureButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final bool isCapturing;

  const _CaptureButton({
    required this.onPressed,
    this.isCapturing = false,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: onPressed,
            borderRadius: BorderRadius.circular(40),
            child: Container(
              width: 72,
              height: 72,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: EcoColors.primaryGreen,
                border: Border.all(
                  color: Colors.white,
                  width: 4,
                ),
                boxShadow: [
                  BoxShadow(
                    color: EcoColors.primaryGreen.withValues(alpha: 0.4),
                    blurRadius: 20,
                    spreadRadius: 2,
                  ),
                ],
              ),
              child: isCapturing
                  ? const Padding(
                      padding: EdgeInsets.all(20),
                      child: CircularProgressIndicator(
                        strokeWidth: 3,
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    )
                  : const Icon(
                      Icons.camera_alt,
                      color: Colors.white,
                      size: 32,
                    ),
            ),
          ),
        ),
        const SizedBox(height: 4),
        Text(
          'Capturer',
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey[600],
            fontWeight: FontWeight.w600,
          ),
        ),
      ],
    );
  }
}

