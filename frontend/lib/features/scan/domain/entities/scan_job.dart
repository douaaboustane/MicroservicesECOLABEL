import 'package:equatable/equatable.dart';

/// Entité représentant un job de scan
class ScanJob extends Equatable {
  final String jobId;
  final String? imageUrl;
  final DateTime createdAt;
  final String status;

  const ScanJob({
    required this.jobId,
    this.imageUrl,
    required this.createdAt,
    required this.status,
  });

  @override
  List<Object?> get props => [jobId, imageUrl, createdAt, status];
}
