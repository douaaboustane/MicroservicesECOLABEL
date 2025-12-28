import 'package:equatable/equatable.dart';

class Recommendation extends Equatable {
  final String jobId;
  final double similarity;
  final double scoreValue;
  final String scoreLetter;
  final List<String> commonIngredients;

  const Recommendation({
    required this.jobId,
    required this.similarity,
    required this.scoreValue,
    required this.scoreLetter,
    required this.commonIngredients,
  });

  @override
  List<Object?> get props => [
        jobId,
        similarity,
        scoreValue,
        scoreLetter,
        commonIngredients,
      ];
}





