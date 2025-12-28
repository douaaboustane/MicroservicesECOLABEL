import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'history_controller.dart';
import '../domain/entities/scan_history_item.dart';

/// Provider pour le controller d'historique
final historyControllerProvider =
    StateNotifierProvider<HistoryController, List<ScanHistoryItem>>((ref) {
  return HistoryController();
});
