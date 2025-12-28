import '../../domain/entities/ingredient_stat.dart';

class IngredientStatModel extends IngredientStat {
  const IngredientStatModel({
    required super.ingredient,
    required super.frequency,
    required super.averageScore,
    required super.percentage,
    super.frequencyInLowScores,
  });

  factory IngredientStatModel.fromJson(Map<String, dynamic> json) {
    return IngredientStatModel(
      ingredient: json['ingredient'] as String,
      frequency: json['frequency'] as int,
      averageScore: (json['average_score'] as num).toDouble(),
      percentage: (json['percentage'] as num).toDouble(),
      frequencyInLowScores: json['frequency_in_low_scores'] as int?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'ingredient': ingredient,
      'frequency': frequency,
      'average_score': averageScore,
      'percentage': percentage,
      if (frequencyInLowScores != null) 
        'frequency_in_low_scores': frequencyInLowScores,
    };
  }
}





