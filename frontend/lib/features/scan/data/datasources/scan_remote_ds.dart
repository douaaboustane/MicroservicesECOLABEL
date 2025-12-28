import 'dart:io';
import 'package:dio/dio.dart';
import '../../../../core/network/api_client.dart';
import '../models/scan_job_model.dart';

/// Source de données distante pour les scans
class ScanRemoteDataSource {
  final ApiClient apiClient;

  ScanRemoteDataSource(this.apiClient);

  /// Crée un nouveau job de scan
  Future<ScanJobModel> createScanJob(File imageFile) async {
    final formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(
        imageFile.path,
        filename: imageFile.path.split('/').last,
      ),
    });

    final response = await apiClient.postFormData<Map<String, dynamic>>(
      '/mobile/products/scan',
      formData,
    );

    return ScanJobModel.fromJson(response.data!);
  }
}
