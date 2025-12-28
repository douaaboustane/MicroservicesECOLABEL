import '../domain/entities/eco_score.dart';

/// Données mockées pour les tests
class MockResultData {
  /// Crée un score de test avec différentes valeurs selon le type
  static EcoScore createTestScore({
    String scoreLetter = 'B',
    int scoreNumeric = 75,
    double? co2,
    double? water,
    double? energy,
    List<String>? ingredients,
  }) {
    return EcoScore(
      jobId: 'test_job_${DateTime.now().millisecondsSinceEpoch}',
      scoreLetter: scoreLetter,
      scoreNumeric: scoreNumeric,
      co2: co2 ?? 1.2,
      water: water ?? 350.0,
      energy: energy ?? 5.8,
      ingredients: ingredients ?? [
        'Farine de blé',
        'Sucre',
        'Huile de palme',
        'Lait écrémé',
        'Cacao',
        'Additif E322',
        'Sel',
      ],
      calculatedAt: DateTime.now(),
    );
  }

  /// Score excellent (A)
  static EcoScore get excellentScore => createTestScore(
        scoreLetter: 'A',
        scoreNumeric: 92,
        co2: 0.5,
        water: 120.0,
        energy: 2.1,
        ingredients: [
          'Farine complète',
          'Eau',
          'Levure',
          'Sel',
        ],
      );

  /// Score moyen (C)
  static EcoScore get averageScore => createTestScore(
        scoreLetter: 'C',
        scoreNumeric: 55,
        co2: 2.5,
        water: 600.0,
        energy: 8.5,
      );

  /// Score faible (D)
  static EcoScore get poorScore => createTestScore(
        scoreLetter: 'D',
        scoreNumeric: 35,
        co2: 4.8,
        water: 1200.0,
        energy: 15.2,
      );

  /// Score très faible (E)
  static EcoScore get veryPoorScore => createTestScore(
        scoreLetter: 'E',
        scoreNumeric: 18,
        co2: 8.2,
        water: 2500.0,
        energy: 25.0,
      );
}
