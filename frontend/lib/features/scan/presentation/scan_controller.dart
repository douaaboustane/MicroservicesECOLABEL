import 'dart:io';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/usecases/create_scan_job.dart';
import '../domain/entities/scan_job.dart';

/// Controller pour la fonctionnalité de scan
class ScanController extends StateNotifier<AsyncValue<ScanJob?>> {
  final CreateScanJob createScanJob;

  ScanController(this.createScanJob) : super(const AsyncValue.data(null));

  /// Crée un nouveau job de scan
  Future<void> scanProduct(File imageFile) async {
    state = const AsyncValue.loading();
    try {
      final job = await createScanJob(imageFile);
      state = AsyncValue.data(job);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  /// Réinitialise l'état
  void reset() {
    state = const AsyncValue.data(null);
  }
}
