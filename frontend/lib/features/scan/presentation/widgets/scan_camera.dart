import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';

/// Widget pour la caméra de scan
class ScanCamera extends StatefulWidget {
  final Function(String imagePath) onImageCaptured;

  const ScanCamera({
    super.key,
    required this.onImageCaptured,
  });

  @override
  State<ScanCamera> createState() => _ScanCameraState();
}

class _ScanCameraState extends State<ScanCamera> {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  bool _isInitialized = false;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    _cameras = await availableCameras();
    if (_cameras != null && _cameras!.isNotEmpty) {
      _controller = CameraController(
        _cameras![0],
        ResolutionPreset.high,
      );

      await _controller!.initialize();
      if (mounted) {
        setState(() {
          _isInitialized = true;
        });
      }
    }
  }

  Future<void> _takePicture() async {
    if (_controller == null || !_controller!.value.isInitialized) {
      return;
    }

    try {
      final image = await _controller!.takePicture();
      widget.onImageCaptured(image.path);
    } catch (e) {
      // Gérer l'erreur
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!_isInitialized || _controller == null) {
      return const Center(child: CircularProgressIndicator());
    }

    final screenSize = MediaQuery.of(context).size;
    final scanAreaSize = screenSize.width * 0.75; // 75% de la largeur de l'écran
    final scanAreaOffset = (screenSize.width - scanAreaSize) / 2;

    return Stack(
      children: [
        CameraPreview(_controller!),
        // Overlay avec zone de scan
        Positioned.fill(
          child: CustomPaint(
            painter: ScanOverlayPainter(
              scanAreaSize: scanAreaSize,
              scanAreaOffset: scanAreaOffset,
            ),
          ),
        ),
        // Zone de scan visible (carré)
        Center(
          child: Container(
            width: scanAreaSize,
            height: scanAreaSize,
            decoration: BoxDecoration(
              border: Border.all(
                color: EcoColors.primaryGreen,
                width: 3,
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Stack(
              children: [
                // Coins arrondis pour meilleure visibilité
                Positioned(
                  top: 0,
                  left: 0,
                  child: Container(
                    width: 30,
                    height: 30,
                    decoration: BoxDecoration(
                      border: Border(
                        top: BorderSide(color: EcoColors.primaryGreen, width: 4),
                        left: BorderSide(color: EcoColors.primaryGreen, width: 4),
                      ),
                      borderRadius: const BorderRadius.only(
                        topLeft: Radius.circular(12),
                      ),
                    ),
                  ),
                ),
                Positioned(
                  top: 0,
                  right: 0,
                  child: Container(
                    width: 30,
                    height: 30,
                    decoration: BoxDecoration(
                      border: Border(
                        top: BorderSide(color: EcoColors.primaryGreen, width: 4),
                        right: BorderSide(color: EcoColors.primaryGreen, width: 4),
                      ),
                      borderRadius: const BorderRadius.only(
                        topRight: Radius.circular(12),
                      ),
                    ),
                  ),
                ),
                Positioned(
                  bottom: 0,
                  left: 0,
                  child: Container(
                    width: 30,
                    height: 30,
                    decoration: BoxDecoration(
                      border: Border(
                        bottom: BorderSide(color: EcoColors.primaryGreen, width: 4),
                        left: BorderSide(color: EcoColors.primaryGreen, width: 4),
                      ),
                      borderRadius: const BorderRadius.only(
                        bottomLeft: Radius.circular(12),
                      ),
                    ),
                  ),
                ),
                Positioned(
                  bottom: 0,
                  right: 0,
                  child: Container(
                    width: 30,
                    height: 30,
                    decoration: BoxDecoration(
                      border: Border(
                        bottom: BorderSide(color: EcoColors.primaryGreen, width: 4),
                        right: BorderSide(color: EcoColors.primaryGreen, width: 4),
                      ),
                      borderRadius: const BorderRadius.only(
                        bottomRight: Radius.circular(12),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        // Instructions
        Positioned(
          top: scanAreaOffset + scanAreaSize + 20,
          left: 0,
          right: 0,
          child: Center(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.6),
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Text(
                'Positionnez le produit dans le cadre',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
        ),
        // Bouton de capture
        Positioned(
          bottom: 40,
          left: 0,
          right: 0,
          child: Center(
            child: FloatingActionButton(
              onPressed: _takePicture,
              backgroundColor: EcoColors.primaryGreen,
              child: const Icon(Icons.camera_alt, color: Colors.white),
            ),
          ),
        ),
      ],
    );
  }
}

/// Painter pour l'overlay de scan (zone assombrie autour du carré)
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
      ..color = Colors.black.withOpacity(0.5)
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
    canvas.drawRect(
      Rect.fromLTWH(0, scanAreaOffset, scanAreaOffset, scanAreaSize),
      paint,
    );

    // Zone droite
    canvas.drawRect(
      Rect.fromLTWH(
        scanAreaOffset + scanAreaSize,
        scanAreaOffset,
        size.width - (scanAreaOffset + scanAreaSize),
        scanAreaSize,
      ),
      paint,
    );
  }

  @override
  bool shouldRepaint(ScanOverlayPainter oldDelegate) => false;
}
