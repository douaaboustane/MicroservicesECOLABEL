import '../../domain/entities/trends.dart';

class TrendsModel extends Trends {
  const TrendsModel({
    required super.trend,
    required super.averageScore,
    required super.totalProducts,
    required super.scoreDistribution,
    super.period1Average,
    super.period2Average,
  });

  factory TrendsModel.fromJson(Map<String, dynamic> json) {
    return TrendsModel(
      trend: json['trend'] as String,
      averageScore: (json['average_score'] as num).toDouble(),
      totalProducts: json['total_products'] as int,
      scoreDistribution: Map<String, int>.from(json['score_distribution'] as Map),
      period1Average: json['period1_average'] != null 
          ? (json['period1_average'] as num).toDouble() 
          : null,
      period2Average: json['period2_average'] != null 
          ? (json['period2_average'] as num).toDouble() 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'trend': trend,
      'average_score': averageScore,
      'total_products': totalProducts,
      'score_distribution': scoreDistribution,
      if (period1Average != null) 'period1_average': period1Average,
      if (period2Average != null) 'period2_average': period2Average,
    };
  }
}





