import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/eco_button.dart';
import '../../../../injection_container.dart' as di;
import '../../domain/entities/scan_job.dart';
import '../../domain/usecases/create_scan_job.dart';
import '../scan_controller.dart';
import '../widgets/scan_camera.dart';

/// Page de scan stylisée
class ScanPage extends ConsumerStatefulWidget {
  const ScanPage({super.key});

  @override
  ConsumerState<ScanPage> createState() => _ScanPageState();
}

class _ScanPageState extends ConsumerState<ScanPage> {
  final ImagePicker _picker = ImagePicker();
  bool _useCamera = true;

  Future<void> _pickImage() async {
    final image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      HapticFeedback.lightImpact();
      _processImage(File(image.path));
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

  @override
  Widget build(BuildContext context) {
    final scanState = ref.watch(scanControllerProvider);

    return Scaffold(
      backgroundColor: EcoColors.naturalBeige,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        title: Text(
          EcoStrings.scanTitle,
          style: EcoTypography.h3.copyWith(
            color: EcoColors.primaryGreen,
          ),
        ),
        iconTheme: const IconThemeData(color: EcoColors.primaryGreen),
      ),
      body: Stack(
        children: [
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 300),
            child: _useCamera
                ? ScanCamera(
                    key: const ValueKey('camera'),
                    onImageCaptured: (path) =>
                        _processImage(File(path)),
                  )
                : _GalleryView(
                    onPickImage: _pickImage,
                    onBackToCamera: () =>
                        setState(() => _useCamera = true),
                  ),
          ),

          // Overlay loading
          if (scanState.isLoading)
            Container(
              color: Colors.black.withValues(alpha: 0.35),
              child: const Center(
                child: CircularProgressIndicator(
                  color: EcoColors.primaryGreen,
                ),
              ),
            ),
        ],
      ),

      // FAB switch mode
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: EcoColors.primaryGreen,
        onPressed: () {
          HapticFeedback.selectionClick();
          setState(() => _useCamera = !_useCamera);
        },
        icon: Icon(_useCamera ? Icons.photo_library : Icons.camera_alt),
        label: Text(_useCamera ? 'Galerie' : 'Caméra'),
      ),
    );
  }
}

/// Widget pour la vue galerie
class _GalleryView extends StatelessWidget {
  final VoidCallback onPickImage;
  final VoidCallback onBackToCamera;

  const _GalleryView({
    required this.onPickImage,
    required this.onBackToCamera,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                color: EcoColors.primaryGreen.withValues(alpha: 0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.image_outlined,
                size: 50,
                color: EcoColors.primaryGreen,
              ),
            ),
            const SizedBox(height: 32),
            Text(
              'Importer une image',
              style: EcoTypography.h3.copyWith(
                color: EcoColors.primaryGreen,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Sélectionnez une image depuis votre galerie',
              style: EcoTypography.bodyMedium.copyWith(
                color: Colors.grey[600],
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 48),
            EcoButton(
              text: EcoStrings.uploadButton,
              icon: Icons.upload_file_rounded,
              onPressed: onPickImage,
            ),
            const SizedBox(height: 16),
            TextButton.icon(
              onPressed: onBackToCamera,
              icon: const Icon(Icons.camera_alt),
              label: const Text('Utiliser la caméra'),
            ),
          ],
        ),
      ),
    );
  }
}

// Provider pour le controller
final scanControllerProvider =
    StateNotifierProvider<ScanController, AsyncValue<ScanJob?>>((ref) {
  return ScanController(di.getIt<CreateScanJob>());
});
