import '../../domain/entities/prediction.dart';

class PredictionModel extends Prediction {
  const PredictionModel({
    required super.predictedScore,
    required super.predictedLetter,
    required super.isEcoFriendly,
    required super.confidence,
  });

  factory PredictionModel.fromJson(Map<String, dynamic> json) {
    return PredictionModel(
      predictedScore: (json['predicted_score'] as num).toDouble(),
      predictedLetter: json['predicted_letter'] as String,
      isEcoFriendly: json['is_eco_friendly'] as bool,
      confidence: json['confidence'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'predicted_score': predictedScore,
      'predicted_letter': predictedLetter,
      'is_eco_friendly': isEcoFriendly,
      'confidence': confidence,
    };
  }
}





