import 'package:equatable/equatable.dart';

/// Entité représentant un score écologique
class EcoScore extends Equatable {
  final String jobId;
  final String scoreLetter; // A, B, C, D, E
  final int scoreNumeric; // 0-100
  final double co2; // kg CO₂
  final double water; // L
  final double energy; // kWh
  final List<String> ingredients;
  final DateTime calculatedAt;

  const EcoScore({
    required this.jobId,
    required this.scoreLetter,
    required this.scoreNumeric,
    required this.co2,
    required this.water,
    required this.energy,
    required this.ingredients,
    required this.calculatedAt,
  });

  @override
  List<Object?> get props => [
        jobId,
        scoreLetter,
        scoreNumeric,
        co2,
        water,
        energy,
        ingredients,
        calculatedAt,
      ];
}
