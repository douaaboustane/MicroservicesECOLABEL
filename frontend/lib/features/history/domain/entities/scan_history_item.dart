import 'package:equatable/equatable.dart';

/// Entité représentant un élément d'historique
class ScanHistoryItem extends Equatable {
  final String jobId;
  final String? productName;
  final String? scoreLetter;
  final int? scoreNumeric;
  final DateTime scannedAt;
  final String? imageUrl;

  const ScanHistoryItem({
    required this.jobId,
    this.productName,
    this.scoreLetter,
    this.scoreNumeric,
    required this.scannedAt,
    this.imageUrl,
  });

  @override
  List<Object?> get props => [
        jobId,
        productName,
        scoreLetter,
        scoreNumeric,
        scannedAt,
        imageUrl,
      ];
}
