import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/widgets/empty_state.dart';
import '../../domain/entities/scan_history_item.dart';
import '../history_providers.dart';
import '../widgets/stats_card.dart';
import '../widgets/search_bar_widget.dart';
import '../widgets/filter_chips_row.dart';
import '../widgets/product_history_card.dart';

/// Page d'historique redesignée
class HistoryPageV2 extends ConsumerStatefulWidget {
  const HistoryPageV2({super.key});

  @override
  ConsumerState<HistoryPageV2> createState() => _HistoryPageV2State();
}

class _HistoryPageV2State extends ConsumerState<HistoryPageV2> {
  String? _selectedScoreFilter;
  String _searchQuery = '';

  List<ScanHistoryItem> _getFilteredItems() {
    final allItems = ref.watch(historyControllerProvider);
    var filtered = allItems;

    // Filtre par score
    if (_selectedScoreFilter != null) {
      filtered = filtered
          .where((item) =>
              item.scoreLetter != null &&
              item.scoreLetter == _selectedScoreFilter)
          .toList();
    }

    // Recherche
    if (_searchQuery.isNotEmpty) {
      final lowerQuery = _searchQuery.toLowerCase();
      filtered = filtered
          .where((item) =>
              (item.productName?.toLowerCase().contains(lowerQuery) ?? false))
          .toList();
    }

    return filtered;
  }

  double _calculateAverageScore() {
    final items = ref.watch(historyControllerProvider);
    if (items.isEmpty) return 0.0;
    final scores = items
        .where((item) => item.scoreNumeric != null)
        .map((item) => item.scoreNumeric!)
        .toList();
    if (scores.isEmpty) return 0.0;
    return scores.reduce((a, b) => a + b) / scores.length;
  }

  String _getAverageScoreLetter() {
    final avg = _calculateAverageScore();
    if (avg >= 80) return 'A';
    if (avg >= 60) return 'B';
    if (avg >= 40) return 'C';
    if (avg >= 20) return 'D';
    return 'E';
  }

  double _calculateCO2Saved() {
    final items = ref.watch(historyControllerProvider);
    return items.length * 0.5; // Estimation
  }

  @override
  Widget build(BuildContext context) {
    final allItems = ref.watch(historyControllerProvider);
    final filteredItems = _getFilteredItems();
    final scanCount = allItems.length;
    final averageScore = _calculateAverageScore();
    final averageScoreLetter = _getAverageScoreLetter();
    final co2Saved = _calculateCO2Saved();

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
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(
          elevation: 0,
          backgroundColor: Colors.transparent,
          title: Text(
            'Historique',
            style: TextStyle(
              color: EcoColors.primaryGreen,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        body: RefreshIndicator(
        onRefresh: () async {
          // TODO: Rafraîchir les données
          await Future.delayed(const Duration(seconds: 1));
        },
        color: EcoColors.primaryGreen,
        child: CustomScrollView(
          slivers: [
            // Stats Card
            if (scanCount > 0)
              SliverToBoxAdapter(
                child: StatsCard(
                  scanCount: scanCount,
                  averageScore: averageScore,
                  averageScoreLetter: averageScoreLetter,
                  co2Saved: co2Saved,
                ),
              ),

            // Search Bar
            SliverToBoxAdapter(
              child: SearchBarWidget(
                onSearchChanged: (query) {
                  setState(() {
                    _searchQuery = query;
                  });
                },
              ),
            ),

            // Filter Chips
            SliverToBoxAdapter(
              child: FilterChipsRow(
                selectedFilter: _selectedScoreFilter,
                onFilterChanged: (filter) {
                  setState(() {
                    _selectedScoreFilter = filter;
                  });
                },
              ),
            ),

            // Product List
            if (filteredItems.isEmpty)
              SliverFillRemaining(
                child: EmptyState(
                  icon: Icons.search_off,
                  title: _searchQuery.isNotEmpty || _selectedScoreFilter != null
                      ? 'Aucun résultat'
                      : 'Aucun produit scanné',
                  message: _searchQuery.isNotEmpty || _selectedScoreFilter != null
                      ? 'Essayez de modifier vos filtres'
                      : 'Scannez votre premier produit pour commencer',
                  actionLabel: 'Scanner maintenant',
                  onAction: () {
                    Navigator.pushNamed(context, AppRoutes.scan);
                  },
                ),
              )
            else
              SliverPadding(
                padding: const EdgeInsets.only(bottom: 100),
                sliver: SliverList(
                  delegate: SliverChildBuilderDelegate(
                    (context, index) {
                      final item = filteredItems[index];
                      return ProductHistoryCard(
                        item: item,
                        onTap: () {
                          Navigator.pushNamed(
                            context,
                            AppRoutes.result,
                            arguments: item.jobId,
                          );
                        },
                      );
                    },
                    childCount: filteredItems.length,
                  ),
                ),
              ),
          ],
        ),
        ),
      ),
    );
  }
}

