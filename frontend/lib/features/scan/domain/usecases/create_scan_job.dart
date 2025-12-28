import 'dart:io';
import '../entities/scan_job.dart';
import '../repositories/scan_repository.dart';

/// Use case pour créer un job de scan
class CreateScanJob {
  final ScanRepository repository;

  CreateScanJob(this.repository);

  Future<ScanJob> call(File imageFile) async {
    return await repository.createScanJob(imageFile);
  }
}
