import 'package:equatable/equatable.dart';

class Trends extends Equatable {
  final String trend; // 'improving', 'declining', 'stable'
  final double averageScore;
  final int totalProducts;
  final Map<String, int> scoreDistribution; // A:20, B:45, C:50, D:25, E:10
  final double? period1Average;
  final double? period2Average;

  const Trends({
    required this.trend,
    required this.averageScore,
    required this.totalProducts,
    required this.scoreDistribution,
    this.period1Average,
    this.period2Average,
  });

  @override
  List<Object?> get props => [
        trend,
        averageScore,
        totalProducts,
        scoreDistribution,
        period1Average,
        period2Average,
      ];
}





