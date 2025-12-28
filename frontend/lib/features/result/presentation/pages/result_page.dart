import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/constants/colors.dart';
import '../widgets/star_score_card.dart';
import '../widgets/impact_cards_comparison.dart';
import '../widgets/ingredients_section.dart';
import '../widgets/score_explanation_card.dart';
import '../widgets/score_message_card.dart';
import '../widgets/result_actions.dart';
import '../../../../core/widgets/skeleton_loader.dart';
import '../../../../core/widgets/error_state.dart';
import '../result_providers.dart';
import '../../../history/presentation/history_providers.dart';
import '../../../history/domain/entities/scan_history_item.dart';
import '../../../analytics/presentation/widgets/recommendations_widget.dart';

class ResultPage extends ConsumerStatefulWidget {
  final String jobId;
  const ResultPage({super.key, required this.jobId});

  @override
  ConsumerState<ResultPage> createState() => _ResultPageState();
}

class _ResultPageState extends ConsumerState<ResultPage> {
  bool _hasAddedToHistory = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(resultControllerProvider.notifier).loadScore(widget.jobId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(resultControllerProvider);

    return state.when(
      data: (score) {
        if (score == null) return const ResultPageSkeleton();
        
        // Ajouter le produit à l'historique (une seule fois, sans doublon)
        if (!_hasAddedToHistory) {
          _hasAddedToHistory = true;
          WidgetsBinding.instance.addPostFrameCallback((_) {
            final historyController = ref.read(historyControllerProvider.notifier);
            historyController.addItemIfNotExists(
              ScanHistoryItem(
                jobId: widget.jobId,
                productName: null, // Le nom sera ajouté plus tard si disponible
                scoreLetter: score.scoreLetter,
                scoreNumeric: score.scoreNumeric,
                scannedAt: score.calculatedAt,
                imageUrl: null,
              ),
            );
          });
        }
        
        // Couleur dynamique basée sur le score (A=Vert, E=Rouge)
        final scoreColor = _getScoreColor(score.scoreLetter);

        return Scaffold(
          backgroundColor: EcoColors.naturalBeige,
          body: CustomScrollView(
            physics: const BouncingScrollPhysics(),
            slivers: [
              // 1. Header Premium avec Image et Gradient
              _buildPremiumHeader(context, score, scoreColor),

              // 2. Contenu de la page
              SliverPadding(
                padding: const EdgeInsets.fromLTRB(20, 24, 20, 40),
                sliver: SliverList(
                  delegate: SliverChildListDelegate([
                    // Carte de message éducatif stylisée
                    ScoreMessageCard(score: score),
                    
                    const SizedBox(height: 32),
                    _buildSectionTitle('Impact Environnemental', Icons.analytics_rounded),
                    const SizedBox(height: 16),
                    
                    // Comparaison d'impact avec fond Glassmorphism léger
                    _buildGlassCard(
                      child: ImpactCardsComparison(
                        score: score,
                        averages: {'co2': 2.5, 'water': 500.0, 'energy': 8.0},
                      ),
                    ),
                    
                    const SizedBox(height: 32),
                    _buildSectionTitle('Analyse des Ingrédients', Icons.fact_check),
                    const SizedBox(height: 16),
                    
                    IngredientsSection(
                      ingredients: score.ingredients,
                      highImpactIngredients: const ['Huile de palme', 'Sucre'],
                    ),
                    
                    const SizedBox(height: 32),
                    
                    // Recommandations de produits similaires
                    RecommendationsWidget(jobId: widget.jobId),
                    
                    const SizedBox(height: 24),
                    ScoreExplanationCard(score: score),
                    
                    const SizedBox(height: 40),
                    ResultActions(
                      onViewMethodology: () => Navigator.pushNamed(context, '/methodology'),
                    ),
                  ]),
                ),
              ),
            ],
          ),
        );
      },
      loading: () => const ResultPageSkeleton(),
      error: (error, stack) => _buildErrorState(error),
    );
  }

  /// Header Immersif avec le score en lévitation
  Widget _buildPremiumHeader(BuildContext context, dynamic score, Color scoreColor) {
    return SliverAppBar(
      expandedHeight: 320,
      automaticallyImplyLeading: false,
      backgroundColor: Colors.transparent,
      flexibleSpace: FlexibleSpaceBar(
        background: Stack(
          fit: StackFit.expand,
          children: [
            // Dégradé de fond dynamique
            Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    scoreColor.withOpacity(0.8),
                    scoreColor.withOpacity(0.4),
                    EcoColors.naturalBeige,
                  ],
                ),
              ),
            ),
            // Bouton retour custom
            Positioned(
              top: 50,
              left: 20,
              child: ClipOval(
                child: BackdropFilter(
                  filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                  child: Container(
                    color: Colors.white.withOpacity(0.2),
                    child: IconButton(
                      icon: const Icon(Icons.arrow_back_ios_new, color: Colors.white, size: 20),
                      onPressed: () => Navigator.pop(context),
                    ),
                  ),
                ),
              ),
            ),
            // Le Score Card qui semble flotter
            Center(
              child: Hero(
                tag: 'score_${score.jobId}',
                child: StarScoreCard(score: score),
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Titres de section avec une typographie élégante
  Widget _buildSectionTitle(String title, IconData icon) {
    return Row(
      children: [
        Icon(icon, color: Colors.black87, size: 22),
        const SizedBox(width: 10),
        Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w800,
            letterSpacing: -0.5,
            color: Colors.black87,
          ),
        ),
      ],
    );
  }

  /// Conteneur effet "Verre" pour les sections importantes
  Widget _buildGlassCard({required Widget child}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(28),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 20,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: child,
    );
  }

  Color _getScoreColor(String letter) {
    switch (letter.toUpperCase()) {
      case 'A': return const Color(0xFF2E7D32);
      case 'B': return const Color(0xFF81C784);
      case 'C': return const Color(0xFFFFB74D);
      case 'D': return const Color(0xFFFF7043);
      case 'E': return const Color(0xFFD32F2F);
      default: return Colors.blueGrey;
    }
  }

  Widget _buildErrorState(Object error) {
    // Personnaliser le message selon le type d'erreur
    String title = 'Analyse interrompue';
    String message = 'Nous n\'avons pas pu finaliser l\'analyse du produit.';
    String? technicalDetails;
    
    final errorStr = error.toString();
    
    if (errorStr.contains('encore en cours')) {
      title = 'Analyse en cours';
      message = 'L\'analyse du produit est toujours en cours. Veuillez patienter quelques instants.';
    } else if (errorStr.contains('Aucun résultat disponible')) {
      title = 'Résultat indisponible';
      message = 'L\'analyse n\'a pas pu générer de résultat. Veuillez réessayer avec une autre image.';
      technicalDetails = errorStr;
    } else if (errorStr.contains('timeout') || errorStr.contains('Timeout')) {
      title = 'Délai dépassé';
      message = 'L\'analyse prend plus de temps que prévu. Le traitement peut encore être en cours.';
    } else if (errorStr.contains('network') || errorStr.contains('connexion')) {
      title = 'Problème de connexion';
      message = 'Impossible de se connecter au serveur. Vérifiez votre connexion internet.';
    } else {
      technicalDetails = errorStr;
    }
    
    return Scaffold(
      body: ErrorState(
        title: title,
        message: message,
        technicalDetails: technicalDetails,
        actionLabel: 'Réessayer',
        onAction: () {
          // Recharger le score avec le même jobId
          ref.read(resultControllerProvider.notifier).loadScore(widget.jobId);
        },
      ),
    );
  }
}