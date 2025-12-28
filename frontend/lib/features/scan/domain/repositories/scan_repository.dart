import 'dart:io';
import '../entities/scan_job.dart';

/// Repository pour les scans
abstract class ScanRepository {
  Future<ScanJob> createScanJob(File imageFile);
}
