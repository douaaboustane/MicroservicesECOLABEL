import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/styles.dart';
import '../../../history/presentation/history_providers.dart';
import '../../../auth/presentation/auth_providers.dart';

class ProfilePageV2 extends ConsumerStatefulWidget {
  const ProfilePageV2({super.key});

  @override
  ConsumerState<ProfilePageV2> createState() => _ProfilePageV2State();
}

class _ProfilePageV2State extends ConsumerState<ProfilePageV2> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _pseudoController = TextEditingController();
  final ImagePicker _picker = ImagePicker();
  // ignore: unused_field
  bool _isEditingName = false;

  @override
  void initState() {
    super.initState();
    _nameController.text = 'Jean Dupont';
    // L'email sera chargé depuis le provider d'authentification
  }

  @override
  void dispose() {
    _nameController.dispose();
    _pseudoController.dispose();
    super.dispose();
  }

  Future<void> _pickAvatar() async {
    final image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null && mounted) {
      // TODO: Logique d'upload réelle ici
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Photo de profil mise à jour')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final historyItems = ref.watch(historyControllerProvider);
    final authState = ref.watch(authControllerProvider);
    final scanCount = historyItems.length;
    final level = (scanCount / 10).floor() + 1;
    
    // Récupérer l'email de l'utilisateur
    final userEmail = authState.when(
      data: (user) => user?.email ?? 'email@example.com',
      loading: () => 'Chargement...',
      error: (_, __) => 'email@example.com',
    );
    
    // Mettre à jour le pseudo avec l'email
    _pseudoController.text = userEmail;
    
    // Mettre à jour le nom si disponible
    final userName = authState.when(
      data: (user) => user?.name,
      loading: () => null,
      error: (_, __) => null,
    );
    if (userName != null && userName.isNotEmpty) {
      _nameController.text = userName;
    }
    
    // Calculs factices pour l'exemple
    final co2Saved = scanCount * 0.5;
    final kmEquivalent = (co2Saved * 4).toStringAsFixed(0);
    
    final scoreDistribution = _getScoreDistribution(historyItems);

    return Container(
      // Fond cohérent avec les autres pages
      decoration: BoxDecoration(
        gradient: EcoStyles.gradientBackground(
          EcoColors.primaryGreen,
          EcoColors.scientificBlue,
        ),
      ),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: CustomScrollView(
          slivers: [
            // 1. Hero Section avec Courbe Organique
            SliverToBoxAdapter(
              child: _buildHeroSection(context, scanCount, level),
            ),

            // 2. Impact Évité
            SliverToBoxAdapter(
              child: _buildImpactSection(context, co2Saved, kmEquivalent),
            ),

            // 3. Répartition des Scores
            SliverToBoxAdapter(
              child: _buildScoreDistributionSection(context, scoreDistribution),
            ),

            // Marge en bas pour le scroll
            const SliverToBoxAdapter(
              child: SizedBox(height: 100),
            ),
          ],
        ),
      ),
    );
  }

  /// Section du haut avec la forme courbée et les infos profil
  Widget _buildHeroSection(BuildContext context, int scanCount, int level) {
    return Stack(
      children: [
        // Fond vert écologique avec dégradé (même vert que les cartes)
        ClipPath(
          clipper: HeaderCurveClipper(),
          child: Container(
            width: double.infinity,
            height: 350,
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  Color(0xFFA8D5A8), // Vert clair (même que Scanner et Stats)
                  Color(0xFF8BC48B), // Vert moyen
                ],
              ),
            ),
          ),
        ),

        // Contenu par-dessus
        SafeArea(
          bottom: false,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Bouton Logout Élégant
              Padding(
                padding: const EdgeInsets.only(left: 16, right: 16, top: 16, bottom: 0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    Material(
                      color: Colors.transparent,
                      child: InkWell(
                        onTap: () async {
                          // Afficher une boîte de dialogue de confirmation
                          final shouldLogout = await showDialog<bool>(
                            context: context,
                            builder: (context) => AlertDialog(
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(20),
                              ),
                              title: const Text(
                                'Déconnexion',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 20,
                                ),
                              ),
                              content: const Text(
                                'Êtes-vous sûr de vouloir vous déconnecter ?',
                                style: TextStyle(fontSize: 15),
                              ),
                              actions: [
                                TextButton(
                                  onPressed: () => Navigator.pop(context, false),
                                  style: TextButton.styleFrom(
                                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                                  ),
                                  child: const Text(
                                    'Annuler',
                                    style: TextStyle(
                                      fontWeight: FontWeight.w600,
                                      fontSize: 15,
                                    ),
                                  ),
                                ),
                                TextButton(
                                  onPressed: () => Navigator.pop(context, true),
                                  style: TextButton.styleFrom(
                                    foregroundColor: Colors.white,
                                    backgroundColor: Colors.red,
                                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(12),
                                    ),
                                  ),
                                  child: const Text(
                                    'Déconnexion',
                                    style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      fontSize: 15,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          );

                          if (shouldLogout == true && context.mounted) {
                            // Déconnexion
                            await ref.read(authControllerProvider.notifier).logout();
                            
                            // Rediriger vers la page de connexion
                            if (context.mounted) {
                              Navigator.of(context).pushNamedAndRemoveUntil(
                                AppRoutes.login,
                                (route) => false,
                              );
                            }
                          }
                        },
                        borderRadius: BorderRadius.circular(20),
                        child: Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.95),
                            borderRadius: BorderRadius.circular(20),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.red.withOpacity(0.15),
                                blurRadius: 12,
                                offset: const Offset(0, 4),
                                spreadRadius: 0,
                              ),
                              BoxShadow(
                                color: Colors.black.withOpacity(0.08),
                                blurRadius: 8,
                                offset: const Offset(0, 2),
                              ),
                            ],
                          ),
                          child: const Icon(
                            Icons.logout_rounded,
                            color: Color(0xFFE53935),
                            size: 22,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              // Avatar sans caméra
              Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.white.withOpacity(0.4), width: 1),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.2),
                      blurRadius: 20,
                      offset: const Offset(0, 10),
                    ),
                  ],
                ),
                child: const CircleAvatar(
                  radius: 50,
                  backgroundColor: Colors.white24,
                  child: Icon(Icons.person, size: 60, color: Colors.white),
                ),
              ),

              const SizedBox(height: 20),
              
              // Nom et Email sur la même ligne avec le même style
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Nom avec fond blanc
                  GestureDetector(
                    onTap: () => _showNameEditDialog(context),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.9),
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(
                          color: Colors.white.withOpacity(0.5),
                          width: 1,
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.1),
                            blurRadius: 10,
                            offset: const Offset(0, 3),
                          ),
                        ],
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            ref.watch(authControllerProvider).when(
                              data: (user) => user?.name ?? 'Utilisateur',
                              loading: () => 'Chargement...',
                              error: (_, __) => 'Utilisateur',
                            ),
                            style: const TextStyle(
                              color: Colors.black87,
                              fontWeight: FontWeight.w600,
                              fontSize: 15,
                              letterSpacing: 0.3,
                            ),
                          ),
                          const SizedBox(width: 8),
                          Icon(
                            Icons.edit_rounded, 
                            color: EcoColors.primaryGreen,
                            size: 16
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(width: 12),
                  
                  // Email avec badge bien visible
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.9),
                      borderRadius: BorderRadius.circular(24),
                      border: Border.all(
                        color: Colors.white.withOpacity(0.5),
                        width: 1,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.1),
                          blurRadius: 10,
                          offset: const Offset(0, 3),
                        ),
                      ],
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.email_outlined, color: EcoColors.primaryGreen, size: 16),
                        const SizedBox(width: 8),
                        Text(
                          _pseudoController.text,
                          style: const TextStyle(
                            color: Colors.black87,
                            fontSize: 15,
                            fontWeight: FontWeight.w600,
                            letterSpacing: 0.3,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 12),

              // Badges d'infos - Style modernisé
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 20),
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(25),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.08),
                      blurRadius: 20,
                      offset: const Offset(0, 8),
                    ),
                  ],
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildModernInfoBadge(
                      Icons.location_on,
                      ref.watch(authControllerProvider).when(
                        data: (user) => user?.pays ?? 'Maroc',
                        loading: () => 'Maroc',
                        error: (_, __) => 'Maroc',
                      ),
                      EcoColors.primaryGreen,
                    ),
                    Container(
                      width: 1.5,
                      height: 22,
                      color: EcoColors.naturalBeige,
                    ),
                    _buildModernInfoBadge(
                      Icons.eco_rounded,
                      '$scanCount Scans',
                      EcoColors.lightGreen,
                    ),
                  ],
                ),
              ),
              
              // Espace pour la courbe - réduit pour mieux voir la forme
              const SizedBox(height: 10),
            ],
          ),
        ),
      ],
    );
  }

  // Widget Capsule pour les infos dans la partie verte (style glassmorphism)
  Widget _buildModernInfoBadge(IconData icon, String text, Color color) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: color, size: 18),
        ),
        const SizedBox(width: 8),
        Text(
          text,
          style: TextStyle(
            color: color,
            fontSize: 14,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.3,
          ),
        ),
      ],
    );
  }

  Widget _buildInfoBadgeGreen(IconData icon, String text) {
    return Expanded(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: Colors.white, size: 18),
          const SizedBox(width: 6),
          Flexible(
            child: Text(
              text,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 12,
                fontWeight: FontWeight.w600,
              ),
              textAlign: TextAlign.center,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }

  // Widget Capsule pour les infos (ancien style pour carte blanche - gardé au cas où)
  Widget _buildInfoBadge(IconData icon, String text, Color textColor) {
    return Expanded(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: EcoColors.primaryGreen, size: 18),
          const SizedBox(width: 6),
          Flexible(
            child: Text(
              text,
              style: TextStyle(
                color: textColor,
                fontSize: 12,
                fontWeight: FontWeight.w600,
              ),
              textAlign: TextAlign.center,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildImpactSection(BuildContext context, double co2Saved, String kmEquivalent) {
    return Container(
      margin: EdgeInsets.symmetric(
        horizontal: EcoStyles.spacingL,
        vertical: EcoStyles.spacingS,
      ),
      padding: EdgeInsets.all(EcoStyles.spacingXXL),
      decoration: EcoStyles.cardWhite,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: EdgeInsets.all(EcoStyles.spacingM),
                decoration: EcoStyles.iconContainer(EcoColors.primaryGreen),
                child: const Icon(
                  Icons.eco_rounded,
                  color: EcoColors.primaryGreen,
                  size: 24,
                ),
              ),
              SizedBox(width: EcoStyles.spacingM),
              Text(
                'Impact Évité',
                style: EcoStyles.bodyText,
              ),
            ],
          ),
          SizedBox(height: EcoStyles.spacingXXL),
          // Texte CO2
          RichText(
            text: TextSpan(
              children: [
                TextSpan(
                  text: '${co2Saved.toStringAsFixed(1)}kg ',
                  style: const TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF2D3436),
                  ),
                ),
                TextSpan(
                  text: 'de CO',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.w600,
                    color: Colors.grey[700],
                  ),
                ),
                WidgetSpan(
                  alignment: PlaceholderAlignment.baseline,
                  baseline: TextBaseline.alphabetic,
                  child: Transform.translate(
                    offset: const Offset(0, 4),
                    child: Text(
                      '₂',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: Colors.grey[700],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(height: EcoStyles.spacingXS),
          Text(
            'économisés grâce à vos choix',
            style: EcoStyles.bodyTextSecondary,
          ),
          SizedBox(height: EcoStyles.spacingXXL),
          // Capsule équivalent
          Container(
            padding: EdgeInsets.all(EcoStyles.spacingL),
            decoration: BoxDecoration(
              color: EcoColors.primaryGreen.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(EcoStyles.radiusLarge),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  Icons.directions_car_rounded,
                  color: EcoColors.primaryGreen,
                  size: 24,
                ),
                SizedBox(width: EcoStyles.spacingM),
                Text(
                  'Équivalent Voyage',
                  style: TextStyle(
                    color: EcoColors.primaryGreen,
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                SizedBox(width: EcoStyles.spacingS),
                Text(
                  '$kmEquivalent km en voiture',
                  style: TextStyle(
                    color: EcoColors.primaryGreen,
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildScoreDistributionSection(BuildContext context, Map<String, Map<String, dynamic>> distribution) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 15, offset: const Offset(0, 5)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                 padding: const EdgeInsets.all(8),
                 decoration: BoxDecoration(
                   color: const Color(0xFFE8F5E9),
                   borderRadius: BorderRadius.circular(10),
                 ),
                 child: const Icon(Icons.bar_chart_rounded, color: Color(0xFF2E7D32), size: 24),
               ),
              const SizedBox(width: 12),
              const Text(
                'Répartition',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF2E7D32)),
              ),
            ],
          ),
          const SizedBox(height: 24),
          ...['A', 'B', 'C', 'D', 'E'].map((score) {
            final data = distribution[score]!;
            final color = _getScoreColor(score);
            final percentage = data['percentage'] as double;
            
            return Padding(
              padding: const EdgeInsets.only(bottom: 20),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Container(
                            width: 24,
                            height: 24,
                            alignment: Alignment.center,
                            decoration: BoxDecoration(
                              color: color.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(score, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
                          ),
                          const SizedBox(width: 10),
                          Text('Score $score', style: const TextStyle(fontWeight: FontWeight.w600, color: Colors.black87)),
                        ],
                      ),
                      Text(
                        '${percentage.toStringAsFixed(0)}%',
                        style: TextStyle(fontWeight: FontWeight.bold, color: color),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(
                      value: percentage / 100,
                      backgroundColor: Colors.grey[100],
                      color: color,
                      minHeight: 10,
                    ),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  // --- Helpers ---

  Map<String, Map<String, dynamic>> _getScoreDistribution(List items) {
    final Map<String, int> counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0};
    for (var item in items) {
      if (counts.containsKey(item.scoreLetter)) {
        counts[item.scoreLetter!] = counts[item.scoreLetter!]! + 1;
      }
    }
    int total = items.isEmpty ? 1 : items.length;
    return counts.map((key, value) => MapEntry(key, {
      'count': value,
      'percentage': (value / total) * 100,
    }));
  }

  Color _getScoreColor(String score) {
    switch (score) {
      case 'A': 
        return const Color(0xFF2E7D32);
      case 'B': 
        return const Color(0xFF81C784);
      case 'C': 
        return const Color(0xFFFFB74D);
      case 'D': 
        return const Color(0xFFFF7043);
      case 'E': 
        return const Color(0xFFD32F2F);
      default: 
        return Colors.grey;
    }
  }

  void _showNameEditDialog(BuildContext context) {
    final tempController = TextEditingController(text: _nameController.text);
    
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Modifier le nom'),
        content: TextField(
          controller: tempController,
          autofocus: true,
          decoration: const InputDecoration(
            hintText: 'Votre nom',
            border: OutlineInputBorder(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context), 
            child: const Text('Annuler')
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF2E7D32)),
            onPressed: () async {
              final newName = tempController.text.trim();
              if (newName.isEmpty) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Le nom ne peut pas être vide')),
                );
                return;
              }
              
              Navigator.pop(context);
              
              // Mettre à jour le profil via le backend
              try {
                await ref.read(authControllerProvider.notifier).updateProfile({'name': newName});
                
                setState(() {
                  _nameController.text = newName;
                });
                
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Nom mis à jour avec succès'),
                      backgroundColor: Color(0xFF2E7D32),
                    ),
                  );
                }
              } catch (e) {
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Erreur: ${e.toString()}'),
                      backgroundColor: Colors.red,
                    ),
                  );
                }
              }
            },
            child: const Text('Enregistrer', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }
}

// --- Le Clipper pour la forme vague/courbe ---
class HeaderCurveClipper extends CustomClipper<Path> {
  @override
  Path getClip(Size size) {
    var path = Path();
    // On commence en bas à gauche, mais un peu remonté pour la courbe
    path.lineTo(0, size.height - 40);

    // Premier point de contrôle (bosse vers le haut) - courbe plus prononcée
    var firstControlPoint = Offset(size.width * 0.25, size.height - 80);
    var firstEndPoint = Offset(size.width * 0.5, size.height - 40);
    
    path.quadraticBezierTo(
      firstControlPoint.dx, firstControlPoint.dy, 
      firstEndPoint.dx, firstEndPoint.dy
    );

    // Deuxième point de contrôle (bosse vers le bas) - courbe plus prononcée
    var secondControlPoint = Offset(size.width * 0.75, size.height);
    var secondEndPoint = Offset(size.width, size.height - 50);

    path.quadraticBezierTo(
      secondControlPoint.dx, secondControlPoint.dy, 
      secondEndPoint.dx, secondEndPoint.dy
    );

    path.lineTo(size.width, 0); // Coin haut droit
    path.close(); // Ferme le chemin en revenant à (0,0)
    return path;
  }

  @override
  bool shouldReclip(CustomClipper<Path> oldClipper) => false;
}