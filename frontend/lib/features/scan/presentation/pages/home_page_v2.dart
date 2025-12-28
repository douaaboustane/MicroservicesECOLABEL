import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/config/env.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/gradient_text.dart';
import '../../../history/presentation/history_providers.dart';
import '../../../../injection_container.dart' as di;
import '../../domain/entities/scan_job.dart';
import '../../domain/usecases/create_scan_job.dart';
import '../scan_controller.dart';

/// Page d'accueil redesignée avec hero section et glassmorphism
class HomePageV2 extends ConsumerStatefulWidget {
  const HomePageV2({super.key});

  @override
  ConsumerState<HomePageV2> createState() => _HomePageV2State();
}

class _HomePageV2State extends ConsumerState<HomePageV2>
    with SingleTickerProviderStateMixin {
  late AnimationController _logoController;
  late Animation<double> _logoScaleAnimation;
  final ImagePicker _picker = ImagePicker();

  @override
  void initState() {
    super.initState();
    _logoController = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    )..repeat(reverse: true);

    _logoScaleAnimation = Tween<double>(begin: 1.0, end: 1.05).animate(
      CurvedAnimation(
        parent: _logoController,
        curve: Curves.easeInOut,
      ),
    );
  }

  @override
  void dispose() {
    _logoController.dispose();
    super.dispose();
  }

  /// Sélectionne une image depuis la galerie du téléphone
  Future<void> _pickImageFromGallery() async {
    try {
      HapticFeedback.lightImpact();
      final XFile? image = await _picker.pickImage(
        source: ImageSource.gallery,
        imageQuality: 85, // Qualité optimale pour l'analyse
      );

      if (image != null) {
        final imageFile = File(image.path);
        
        // Vérifier que le fichier existe et est valide
        if (!await imageFile.exists()) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Le fichier sélectionné n\'existe plus'),
                backgroundColor: Colors.orange,
              ),
            );
          }
          return;
        }
        
        // Vérifier la taille du fichier (max 10MB)
        final fileSize = await imageFile.length();
        if (fileSize > 10 * 1024 * 1024) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('L\'image est trop volumineuse (max 10MB)'),
                backgroundColor: Colors.orange,
              ),
            );
          }
          return;
        }
        
        await _processImage(imageFile);
      }
    } on PlatformException catch (e) {
      // Erreur de permission
      if (mounted) {
        String message = 'Erreur lors de l\'accès à la galerie';
        if (e.code == 'photo_access_denied' || e.code == 'permission_denied') {
          message = 'Permission refusée. Veuillez autoriser l\'accès à la galerie dans les paramètres.';
        } else if (e.code == 'photo_picker_error') {
          message = 'Impossible d\'ouvrir la galerie. Veuillez réessayer.';
        }
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(message),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 4),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Erreur lors de la sélection de l\'image: ${e.toString()}'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 3),
          ),
        );
      }
    }
  }

  /// Traite l'image sélectionnée
  Future<void> _processImage(File imageFile) async {
    try {
      final controller = ref.read(scanControllerProvider.notifier);
      
      // Afficher un indicateur de chargement
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Row(
              children: [
                SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                  ),
                ),
                SizedBox(width: 16),
                Text('Envoi de l\'image au serveur...'),
              ],
            ),
            duration: Duration(seconds: 2),
          ),
        );
      }
      
      await controller.scanProduct(imageFile);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Erreur lors du traitement: ${e.toString()}'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 3),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    // Écouter les changements du scanController pour rediriger vers processing ou gérer les erreurs
    // ref.listen doit être dans build, pas dans initState
    ref.listen<AsyncValue<ScanJob?>>(
      scanControllerProvider,
      (previous, next) {
        next.whenOrNull(
          data: (job) {
            if (job != null && mounted) {
              Navigator.pushNamed(
                context,
                AppRoutes.processing,
                arguments: job.jobId,
              );
            }
          },
          error: (error, stack) {
            if (mounted) {
              String errorMessage = 'Erreur lors de l\'envoi de l\'image';
              String? technicalDetails;
              
              // Messages d'erreur plus spécifiques avec détails techniques
              final errorStr = error.toString();
              
              if (errorStr.contains('Timeout') || errorStr.contains('timeout')) {
                errorMessage = 'Timeout de connexion au serveur.';
                technicalDetails = 'Le serveur ne répond pas dans les délais. Vérifiez que le backend est démarré sur le port 8000.';
              } else if (errorStr.contains('Failed host lookup') ||
                         errorStr.contains('Network is unreachable') ||
                         errorStr.contains('SocketException') ||
                         errorStr.contains('Connection refused')) {
                errorMessage = 'Impossible de se connecter au serveur.';
                technicalDetails = 'Vérifiez que le backend est démarré et accessible. URL: ${Env.baseUrl}';
              } else if (errorStr.contains('503') ||
                         errorStr.contains('Service indisponible')) {
                errorMessage = 'Le service est temporairement indisponible.';
                technicalDetails = 'Le backend est peut-être en cours de démarrage. Réessayez dans quelques instants.';
              } else if (errorStr.contains('500')) {
                errorMessage = 'Erreur serveur lors du traitement.';
                technicalDetails = 'Le backend a rencontré une erreur. Vérifiez les logs du serveur.';
              } else if (errorStr.contains('404')) {
                errorMessage = 'Endpoint non trouvé.';
                technicalDetails = 'L\'endpoint /mobile/products/scan n\'existe pas. Vérifiez la configuration du backend.';
              } else if (errorStr.contains('401') || errorStr.contains('Non autorisé')) {
                errorMessage = 'Authentification requise.';
                technicalDetails = 'Vous devez être connecté pour envoyer une image.';
              } else {
                // Afficher plus de détails pour les autres erreurs
                technicalDetails = errorStr.length > 100 
                    ? errorStr.substring(0, 100) + '...'
                    : errorStr;
              }
              
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        errorMessage,
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      if (technicalDetails != null) ...[
                        const SizedBox(height: 4),
                        Text(
                          technicalDetails,
                          style: const TextStyle(fontSize: 12),
                        ),
                      ],
                    ],
                  ),
                  backgroundColor: Colors.red,
                  duration: const Duration(seconds: 6),
                  action: SnackBarAction(
                    label: 'Réessayer',
                    textColor: Colors.white,
                    onPressed: () {
                      // Réinitialiser l'état pour permettre un nouvel essai
                      ref.read(scanControllerProvider.notifier).reset();
                    },
                  ),
                ),
              );
            }
          },
        );
      },
    );

    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            EcoColors.primaryGreen.withValues(alpha: 0.1),
            EcoColors.scientificBlue.withValues(alpha: 0.05),
            EcoColors.naturalBeige,
          ],
          stops: const [0.0, 0.5, 1.0],
        ),
      ),
      child: SafeArea(
        child: CustomScrollView(
          slivers: [
          // Hero section
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              child: _buildHeroSection(),
            ),
          ),

          // Espace supplémentaire
          SliverToBoxAdapter(
            child: SizedBox(height: 32),
          ),

          // Actions principales
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
              child: _buildActionCards(),
            ),
          ),

          // Boutons de test (DEV ONLY)
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: _buildTestButtons(),
            ),
          ),
        ],
        ),
      ),
    );
  }

  Widget _buildHeroSection() {
    return Column(
      children: [
        // Logo animé
        AnimatedBuilder(
          animation: _logoScaleAnimation,
          builder: (context, child) {
            return Transform.scale(
              scale: _logoScaleAnimation.value,
              child: Container(
                width: 130,
                height: 130,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: const LinearGradient(
                    colors: [
                      EcoColors.primaryGreen,
                      EcoColors.lightGreen,
                    ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: EcoColors.primaryGreen.withValues(alpha: 0.4),
                      blurRadius: 30,
                      spreadRadius: 5,
                    ),
                  ],
                ),
                child: const Icon(
                  Icons.eco,
                  size: 64,
                  color: Colors.white,
                ),
              ),
            );
          },
        ),

        const SizedBox(height: 24),

        // Titre avec gradient
        GradientText(
          text: EcoStrings.appName,
          gradient: const LinearGradient(
            colors: [
              EcoColors.primaryGreen,
              EcoColors.scientificBlue,
            ],
          ),
          style: EcoTypography.h1.copyWith(
            fontSize: 36,
            fontWeight: FontWeight.bold,
          ),
          textAlign: TextAlign.center,
        ),

        const SizedBox(height: 12),

        // Tagline avec icônes
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
            _TaglineItem(icon: '', text: 'Scan'),
            const SizedBox(width: 16),
            _TaglineItem(icon: '', text: 'Analyse'),
            const SizedBox(width: 16),
            _TaglineItem(icon: '', text: 'Agissez'),
            ],
          ),
      ],
    );
  }

  Widget _buildActionCards() {
    return Column(
      children: [
        // Card Scanner
        Container(
          margin: const EdgeInsets.only(bottom: 16),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                const Color(0xFFA8D5A8), // Vert clair
                const Color(0xFF8BC48B), // Vert moyen
              ],
            ),
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: EcoColors.primaryGreen.withValues(alpha: 0.2),
                blurRadius: 12,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              onTap: () {
                HapticFeedback.mediumImpact();
                Navigator.pushNamed(context, AppRoutes.scan);
              },
              borderRadius: BorderRadius.circular(20),
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Row(
                  children: [
                    Container(
                      width: 64,
                      height: 64,
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.3),
                        borderRadius: BorderRadius.circular(18),
                      ),
                      child: const Icon(
                        Icons.qr_code_scanner_rounded,
                        color: Colors.white,
                        size: 34,
                      ),
                    ),
                    const SizedBox(width: 18),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Scanner',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Scannez le code-barres ou l\'étiquette',
                            style: TextStyle(
                              color: Colors.white.withValues(alpha: 0.9),
                              fontSize: 13,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const Icon(
                      Icons.arrow_forward_ios_rounded,
                      color: Colors.white,
                      size: 20,
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),

        // Card Importer
        Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                const Color(0xFF9BBFDA), // Bleu clair
                const Color(0xFF7AA5C9), // Bleu moyen
              ],
            ),
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: EcoColors.scientificBlue.withValues(alpha: 0.2),
                blurRadius: 12,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              onTap: _pickImageFromGallery,
              borderRadius: BorderRadius.circular(20),
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Row(
                  children: [
                    Container(
                      width: 64,
                      height: 64,
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.3),
                        borderRadius: BorderRadius.circular(18),
                      ),
                      child: const Icon(
                        Icons.photo_library_rounded,
                        color: Colors.white,
                        size: 34,
                      ),
                    ),
                    const SizedBox(width: 18),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Importer',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Choisissez une photo depuis votre galerie',
                            style: TextStyle(
                              color: Colors.white.withValues(alpha: 0.9),
                              fontSize: 13,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const Icon(
                      Icons.arrow_forward_ios_rounded,
                      color: Colors.white,
                      size: 20,
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildTestButtons() {
    return Column(
      children: [
        Text(
          'Exemple',
          style: TextStyle(
            color: Colors.grey[600],
            fontSize: 14,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.5,
          ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 10,
          runSpacing: 10,
          alignment: WrapAlignment.center,
          children: [
            _TestButton(
              label: 'Score A',
              color: EcoColors.scoreA,
              jobId: 'test_job_excellent',
            ),
            _TestButton(
              label: 'Score B',
              color: EcoColors.scoreB,
              jobId: 'test_job',
            ),
            _TestButton(
              label: 'Score C',
              color: EcoColors.scoreC,
              jobId: 'test_job_average',
            ),
            _TestButton(
              label: 'Score D',
              color: EcoColors.scoreD,
              jobId: 'test_job_poor',
            ),
            _TestButton(
              label: 'Score E',
              color: EcoColors.scoreE,
              jobId: 'test_job_very_poor',
            ),
          ],
        ),
      ],
    );
  }
}


/// Widget pour les éléments du tagline
class _TaglineItem extends StatelessWidget {
  final String icon;
  final String text;

  const _TaglineItem({
    required this.icon,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (icon.isNotEmpty) ...[
          Text(icon, style: const TextStyle(fontSize: 16)),
          const SizedBox(width: 4),
        ],
        Text(
          text,
          style: EcoTypography.bodyMedium.copyWith(
            color: Colors.grey[700],
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }
}

/// Bouton de test pour différents scores
class _TestButton extends StatelessWidget {
  final String label;
  final Color color;
  final String jobId;

  const _TestButton({
    required this.label,
    required this.color,
    required this.jobId,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () {
          HapticFeedback.selectionClick();
          Navigator.pushNamed(
            context,
            AppRoutes.result,
            arguments: jobId,
          );
        },
        borderRadius: BorderRadius.circular(28),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 11),
          decoration: BoxDecoration(
            color: Colors.white.withValues(alpha: 0.75),
            border: Border.all(
              color: color,
              width: 2.5,
            ),
            borderRadius: BorderRadius.circular(28),
            boxShadow: [
              BoxShadow(
                color: color.withValues(alpha: 0.25),
                blurRadius: 8,
                offset: const Offset(0, 3),
                spreadRadius: 0,
              ),
            ],
          ),
          child: Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 14,
              fontWeight: FontWeight.w700,
              letterSpacing: 0.4,
            ),
          ),
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

