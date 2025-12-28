import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/entities/scan_history_item.dart';

/// Controller pour l'historique
class HistoryController extends StateNotifier<List<ScanHistoryItem>> {
  HistoryController() : super([]);

  void addItem(ScanHistoryItem item) {
    state = [item, ...state];
  }

  /// Ajoute un item uniquement s'il n'existe pas déjà (basé sur jobId)
  void addItemIfNotExists(ScanHistoryItem item) {
    // Vérifier si un item avec le même jobId existe déjà
    final exists = state.any((existing) => existing.jobId == item.jobId);
    
    if (!exists) {
      state = [item, ...state];
    }
  }

  void removeItem(String jobId) {
    state = state.where((item) => item.jobId != jobId).toList();
  }

  void clearHistory() {
    state = [];
  }

  List<ScanHistoryItem> filterByScore(String? score) {
    if (score == null) return state;
    return state
        .where((item) => item.scoreLetter != null && item.scoreLetter == score)
        .toList();
  }

  List<ScanHistoryItem> search(String query) {
    if (query.isEmpty) return state;
    final lowerQuery = query.toLowerCase();
    return state.where((item) {
      return (item.productName?.toLowerCase().contains(lowerQuery) ?? false);
    }).toList();
  }
}
