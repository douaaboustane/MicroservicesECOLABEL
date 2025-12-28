import '../../domain/entities/anomaly.dart';

class AnomalyModel extends Anomaly {
  const AnomalyModel({
    required super.jobId,
    required super.scoreValue,
    required super.scoreLetter,
    required super.zScore,
    required super.reason,
  });

  factory AnomalyModel.fromJson(Map<String, dynamic> json) {
    return AnomalyModel(
      jobId: json['job_id'] as String,
      scoreValue: (json['score_value'] as num).toDouble(),
      scoreLetter: json['score_letter'] as String,
      zScore: (json['z_score'] as num).toDouble(),
      reason: json['reason'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'job_id': jobId,
      'score_value': scoreValue,
      'score_letter': scoreLetter,
      'z_score': zScore,
      'reason': reason,
    };
  }
}





