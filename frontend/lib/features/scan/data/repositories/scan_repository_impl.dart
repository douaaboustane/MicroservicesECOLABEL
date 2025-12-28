import 'dart:io';
import '../../domain/entities/scan_job.dart';
import '../../domain/repositories/scan_repository.dart';
import '../datasources/scan_remote_ds.dart';
import '../models/scan_job_model.dart';

/// Implémentation du repository de scan
class ScanRepositoryImpl implements ScanRepository {
  final ScanRemoteDataSource remoteDataSource;

  ScanRepositoryImpl(this.remoteDataSource);

  @override
  Future<ScanJob> createScanJob(File imageFile) async {
    final model = await remoteDataSource.createScanJob(imageFile);
    return model;
  }
}
