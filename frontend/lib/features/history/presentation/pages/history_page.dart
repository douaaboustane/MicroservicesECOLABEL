import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/config/routes.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/eco_card.dart';
import '../../../../core/widgets/empty_state.dart';
import '../../../../core/utils/date_utils.dart' as app_date_utils;
import 'package:ecolabel_ms/features/history/domain/entities/scan_history_item.dart';
import 'package:ecolabel_ms/features/history/presentation/history_providers.dart';

/// Page d'historique améliorée
class HistoryPage extends ConsumerStatefulWidget {
  const HistoryPage({super.key});

  @override
  ConsumerState<HistoryPage> createState() => _HistoryPageState();
}

class _HistoryPageState extends ConsumerState<HistoryPage> {
  final _searchController = TextEditingController();
  String? _selectedScoreFilter;

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

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
    final query = _searchController.text.trim();
    if (query.isNotEmpty) {
      final lowerQuery = query.toLowerCase();
      filtered = filtered
          .where((item) =>
              (item.productName?.toLowerCase().contains(lowerQuery) ?? false))
          .toList();
    }

    return filtered;
  }

  double _getAverageScore() {
    final items = ref.watch(historyControllerProvider);
    final scores = items
        .where((item) => item.scoreNumeric != null)
        .map((item) => item.scoreNumeric!)
        .toList();
    if (scores.isEmpty) return 0.0;
    return scores.reduce((a, b) => a + b) / scores.length;
  }

  @override
  Widget build(BuildContext context) {
    final items = _getFilteredItems();
    final allItems = ref.watch(historyControllerProvider);
    final averageScore = _getAverageScore();

    return Column(
      children: [
          // Statistiques
          if (allItems.isNotEmpty)
            Container(
              padding: const EdgeInsets.all(16),
              margin: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: EcoColors.primaryGreen.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Column(
                    children: [
                      Text(
                        '${allItems.length}',
                        style: EcoTypography.h2.copyWith(
                          color: EcoColors.primaryGreen,
                        ),
                      ),
                      Text(
                        'Scans',
                        style: EcoTypography.bodySmall,
                      ),
                    ],
                  ),
                  Column(
                    children: [
                      Text(
                        averageScore.toStringAsFixed(0),
                        style: EcoTypography.h2.copyWith(
                          color: EcoColors.primaryGreen,
                        ),
                      ),
                      Text(
                        'Score moyen',
                        style: EcoTypography.bodySmall,
                      ),
                    ],
                  ),
                ],
              ),
            ),

          // Barre de recherche
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Rechercher un produit...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          _searchController.clear();
                          setState(() {});
                        },
                      )
                    : null,
              ),
              onChanged: (_) => setState(() {}),
            ),
          ),

          // Filtres par score
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildFilterChip('Tous', null),
                  const SizedBox(width: 8),
                  ...['A', 'B', 'C', 'D', 'E'].map(
                    (score) => Padding(
                      padding: const EdgeInsets.only(right: 8),
                      child: _buildFilterChip(score, score),
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Liste des items
          Expanded(
            child: items.isEmpty
                ? allItems.isEmpty
                    ? EmptyState(
                        icon: Icons.history,
                        title: EcoStrings.historyEmpty,
                        message: EcoStrings.historyEmptyDesc,
                        actionLabel: 'Scanner un produit',
                        onAction: () {
                          Navigator.pushNamed(context, AppRoutes.scan);
                        },
                      )
                    : EmptyState(
                        icon: Icons.search_off,
                        title: 'Aucun résultat trouvé',
                        message: 'Essayez de modifier vos filtres ou votre recherche.',
                      )
                : ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: items.length,
                    itemBuilder: (context, index) {
                      final item = items[index];
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 12),
                        child: EcoCard(
                          onTap: () {
                            // TODO: Naviguer vers le résultat
                          },
                          child: Row(
                            children: [
                              if (item.imageUrl != null)
                                ClipRRect(
                                  borderRadius: BorderRadius.circular(8),
                                  child: Image.network(
                                    item.imageUrl!,
                                    width: 60,
                                    height: 60,
                                    fit: BoxFit.cover,
                                  ),
                                )
                              else
                                Container(
                                  width: 60,
                                  height: 60,
                                  decoration: BoxDecoration(
                                    color: Colors.grey[200],
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: const Icon(Icons.image,
                                      color: Colors.grey),
                                ),
                              const SizedBox(width: 16),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      item.productName ?? 'Produit scanné',
                                      style: const TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.w600,
                                      ),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      app_date_utils.DateUtils.formatRelative(
                                          item.scannedAt),
                                      style: TextStyle(
                                        fontSize: 12,
                                        color: Colors.grey[600],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              if (item.scoreLetter != null)
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 16,
                                    vertical: 8,
                                  ),
                                  decoration: BoxDecoration(
                                    color: EcoColors.getScoreColor(
                                            item.scoreLetter!)
                                        .withValues(alpha: 0.1),
                                    borderRadius: BorderRadius.circular(20),
                                    border: Border.all(
                                      color: EcoColors.getScoreColor(
                                          item.scoreLetter!),
                                      width: 2,
                                    ),
                                  ),
                                  child: Text(
                                    item.scoreLetter!,
                                    style: TextStyle(
                                      fontSize: 20,
                                      fontWeight: FontWeight.bold,
                                      color: EcoColors.getScoreColor(
                                          item.scoreLetter!),
                                    ),
                                  ),
                                ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
        ),
      ],
    );
  }

  Widget _buildFilterChip(String label, String? value) {
    final isSelected = _selectedScoreFilter == value;
    return FilterChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (selected) {
        setState(() {
          _selectedScoreFilter = selected ? value : null;
        });
      },
      selectedColor: EcoColors.primaryGreen.withValues(alpha: 0.2),
      checkmarkColor: EcoColors.primaryGreen,
    );
  }
}
