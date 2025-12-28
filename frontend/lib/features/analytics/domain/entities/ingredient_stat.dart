import 'package:equatable/equatable.dart';

class IngredientStat extends Equatable {
  final String ingredient;
  final int frequency;
  final double averageScore;
  final double percentage;
  final int? frequencyInLowScores; // Only for bad ingredients

  const IngredientStat({
    required this.ingredient,
    required this.frequency,
    required this.averageScore,
    required this.percentage,
    this.frequencyInLowScores,
  });

  @override
  List<Object?> get props => [
        ingredient,
        frequency,
        averageScore,
        percentage,
        frequencyInLowScores,
      ];
}





