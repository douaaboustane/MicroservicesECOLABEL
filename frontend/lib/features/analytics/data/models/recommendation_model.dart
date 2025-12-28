import '../../domain/entities/recommendation.dart';

class RecommendationModel extends Recommendation {
  const RecommendationModel({
    required super.jobId,
    required super.similarity,
    required super.scoreValue,
    required super.scoreLetter,
    required super.commonIngredients,
  });

  factory RecommendationModel.fromJson(Map<String, dynamic> json) {
    return RecommendationModel(
      jobId: json['job_id'] as String,
      similarity: (json['similarity'] as num).toDouble(),
      scoreValue: (json['score_value'] as num).toDouble(),
      scoreLetter: json['score_letter'] as String,
      commonIngredients: List<String>.from(json['common_ingredients'] as List),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'job_id': jobId,
      'similarity': similarity,
      'score_value': scoreValue,
      'score_letter': scoreLetter,
      'common_ingredients': commonIngredients,
    };
  }
}





