import '../../domain/entities/scan_job.dart';

/// Modèle de données pour ScanJob
class ScanJobModel extends ScanJob {
  const ScanJobModel({
    required super.jobId,
    super.imageUrl,
    required super.createdAt,
    required super.status,
  });

  factory ScanJobModel.fromJson(Map<String, dynamic> json) {
    // Le backend retourne seulement job_id et status
    // Les autres champs sont optionnels ou ont des valeurs par défaut
    final jobId = json['job_id'] as String? ?? 
                  json['jobId'] as String?;
    
    if (jobId == null || jobId.isEmpty) {
      throw FormatException(
        'Invalid response: job_id is missing or empty',
        json,
      );
    }
    
    final imageUrl = json['image_url'] as String? ?? 
                     json['imageUrl'] as String?;
    
    // created_at peut ne pas être présent dans la réponse initiale
    DateTime createdAt;
    if (json['created_at'] != null) {
      createdAt = DateTime.parse(json['created_at'] as String);
    } else if (json['createdAt'] != null) {
      createdAt = DateTime.parse(json['createdAt'] as String);
    } else {
      createdAt = DateTime.now();
    }
    
    final status = json['status'] as String? ?? 'PENDING';
    
    return ScanJobModel(
      jobId: jobId,
      imageUrl: imageUrl,
      createdAt: createdAt,
      status: status,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'job_id': jobId,
      'image_url': imageUrl,
      'created_at': createdAt.toIso8601String(),
      'status': status,
    };
  }
}
