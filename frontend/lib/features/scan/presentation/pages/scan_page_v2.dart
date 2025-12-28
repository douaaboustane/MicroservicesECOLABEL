import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/constants/typography.dart';
import '../../../../injection_container.dart' as di;
import '../../domain/entities/scan_job.dart';
import '../../domain/usecases/create_scan_job.dart';
import '../scan_controller.dart';
import '../widgets/scan_overlay.dart';
import '../widgets/scan_bottom_sheet.dart';

// Provider pour le controller
final scanControllerProvider =
    StateNotifierProvider<ScanController, AsyncValue<ScanJob?>>((ref) {
  return ScanController(di.getIt<CreateScanJob>());
});

/// Page de scan v2 avec zone de scan carrée immersive
class ScanPageV2 extends ConsumerStatefulWidget {
  const ScanPageV2({super.key});

  @override
  ConsumerState<ScanPageV2> createState() => _ScanPageV2State();
}

class _ScanPageV2State extends ConsumerState<ScanPageV2> {
  final ImagePicker _picker = ImagePicker();
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  bool _isInitialized = false;
  bool _isFlashOn = false;
  bool _isCapturing = false;
  ScanState _scanState = ScanState.idle;
  ScanMode _scanMode = ScanMode.label;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    try {
      _cameras = await availableCameras();
      if (_cameras == null || _cameras!.isEmpty) {
        if (mounted) {
          setState(() {
            _errorMessage = 'Aucune caméra disponible';
          });
        }
        return;
      }

      _controller = CameraController(
        _cameras![0],
        ResolutionPreset.high,
      );

      await _controller!.initialize();
      if (mounted) {
        setState(() {
          _isInitialized = true;
          _errorMessage = null;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = 'Erreur lors de l\'initialisation de la caméra: ${e.toString()}';
          _isInitialized = false;
        });
      }
    }
  }

  Future<void> _takePicture() async {
    if (_controller == null || !_controller!.value.isInitialized || _isCapturing) {
      return;
    }

    setState(() {
      _isCapturing = true;
      _scanState = ScanState.captured;
    });

    try {
      HapticFeedback.mediumImpact();
      final image = await _controller!.takePicture();
      await _processImage(File(image.path));
    } catch (e) {
      setState(() {
        _isCapturing = false;
        _scanState = ScanState.idle;
      });
    }
  }

  Future<void> _pickFromGallery() async {
    final image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      HapticFeedback.lightImpact();
      await _processImage(File(image.path));
    }
  }

  Future<void> _processImage(File imageFile) async {
    final controller = ref.read(scanControllerProvider.notifier);
    await controller.scanProduct(imageFile);

    ref.listen<AsyncValue<ScanJob?>>(
      scanControllerProvider,
      (_, state) {
        state.whenOrNull(
          data: (job) {
            if (job != null && mounted) {
              Navigator.pushNamed(
                context,
                AppRoutes.processing,
                arguments: job.jobId,
              );
            }
          },
        );
      },
    );
  }

  Future<void> _toggleFlash() async {
    if (_controller == null || !_controller!.value.isInitialized) return;

    try {
      final newFlashMode = _isFlashOn
          ? FlashMode.off
          : FlashMode.torch;
      await _controller!.setFlashMode(newFlashMode);
      setState(() {
        _isFlashOn = !_isFlashOn;
      });
      HapticFeedback.selectionClick();
    } catch (e) {
      // Gérer l'erreur
    }
  }

  String _getInstruction() {
    switch (_scanState) {
      case ScanState.idle:
        return '📸 Centrez l\'étiquette dans le cadre';
      case ScanState.scanning:
        return '🔍 Détection en cours...';
      case ScanState.detecting:
        return '✨ Parfait! Maintenez stable...';
      case ScanState.captured:
        return '✅ Image capturée!';
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final scanState = ref.watch(scanControllerProvider);
    final screenSize = MediaQuery.of(context).size;
    final scanAreaSize = screenSize.width * 0.75; // 75% de la largeur

    return Scaffold(
      backgroundColor: Colors.black,
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          EcoStrings.scanTitle,
          style: EcoTypography.h3.copyWith(
            color: Colors.white,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.help_outline, color: Colors.white),
            onPressed: () {
              // TODO: Afficher aide
            },
          ),
        ],
      ),
      body: Stack(
        children: [
          // Camera preview
          if (_isInitialized && _controller != null && _controller!.value.isInitialized)
            SizedBox.expand(
              child: CameraPreview(_controller!),
            )
          else if (_errorMessage != null)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.camera_alt_outlined,
                      size: 64,
                      color: Colors.white54,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      _errorMessage!,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 24),
                    ElevatedButton.icon(
                      onPressed: _initializeCamera,
                      icon: const Icon(Icons.refresh),
                      label: const Text('Réessayer'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: EcoColors.primaryGreen,
                        foregroundColor: Colors.white,
                      ),
                    ),
                  ],
                ),
              ),
            )
          else
            const Center(
              child: CircularProgressIndicator(
                color: EcoColors.primaryGreen,
              ),
            ),

          // Overlay avec zone de scan
          if (_isInitialized)
            ScanOverlay(
              scanAreaSize: scanAreaSize,
              instruction: _getInstruction(),
              scanState: _scanState,
            ),

          // Mode selector (si nécessaire)
          if (_isInitialized)
            Positioned(
              top: 100,
              left: 0,
              right: 0,
              child: Center(
                child: _buildModeSelector(),
              ),
            ),

          // Bottom sheet avec actions
          if (_isInitialized)
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: ScanBottomSheet(
                onCapture: _takePicture,
                onGallery: _pickFromGallery,
                onFlashToggle: _toggleFlash,
                isFlashOn: _isFlashOn,
                isCapturing: _isCapturing,
              ),
            ),

          // Overlay loading
          if (scanState.isLoading)
            Container(
              color: Colors.black.withValues(alpha: 0.7),
              child: const Center(
                child: CircularProgressIndicator(
                  color: EcoColors.primaryGreen,
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildModeSelector() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.black.withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          _ModeButton(
            label: 'Code-barres',
            isSelected: _scanMode == ScanMode.barcode,
            onTap: () {
              setState(() {
                _scanMode = ScanMode.barcode;
              });
            },
          ),
          const SizedBox(width: 8),
          _ModeButton(
            label: 'Étiquette',
            isSelected: _scanMode == ScanMode.label,
            onTap: () {
              setState(() {
                _scanMode = ScanMode.label;
              });
            },
          ),
        ],
      ),
    );
  }
}

/// Bouton de sélection de mode
class _ModeButton extends StatelessWidget {
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  const _ModeButton({
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected
              ? EcoColors.lightGreen
              : Colors.transparent,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Text(
          label,
          style: TextStyle(
            color: isSelected ? Colors.white : Colors.white70,
            fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
            fontSize: 14,
          ),
        ),
      ),
    );
  }
}

/// Modes de scan
enum ScanMode {
  barcode,
  label,
}

