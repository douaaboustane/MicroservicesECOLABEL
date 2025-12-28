import 'package:equatable/equatable.dart';

class Anomaly extends Equatable {
  final String jobId;
  final double scoreValue;
  final String scoreLetter;
  final double zScore;
  final String reason;

  const Anomaly({
    required this.jobId,
    required this.scoreValue,
    required this.scoreLetter,
    required this.zScore,
    required this.reason,
  });

  @override
  List<Object?> get props => [
        jobId,
        scoreValue,
        scoreLetter,
        zScore,
        reason,
      ];
}





