import 'package:equatable/equatable.dart';

class Prediction extends Equatable {
  final double predictedScore;
  final String predictedLetter;
  final bool isEcoFriendly;
  final String confidence; // 'low', 'medium', 'high'

  const Prediction({
    required this.predictedScore,
    required this.predictedLetter,
    required this.isEcoFriendly,
    required this.confidence,
  });

  @override
  List<Object?> get props => [
        predictedScore,
        predictedLetter,
        isEcoFriendly,
        confidence,
      ];
}





