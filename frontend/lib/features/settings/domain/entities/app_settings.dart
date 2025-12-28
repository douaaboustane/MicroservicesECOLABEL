import 'package:equatable/equatable.dart';

/// Sensibilité environnementale
enum EnvironmentalSensitivity {
  low,
  medium,
  high,
}

/// Mode d'affichage
enum DisplayMode {
  light,
  dark,
  system,
}

/// Paramètres de l'application
class AppSettings extends Equatable {
  // Pondération des critères (0.0 - 1.0, doit totaliser 1.0)
  final double co2Weight;
  final double waterWeight;
  final double energyWeight;

  // Sensibilité environnementale
  final EnvironmentalSensitivity sensitivity;

  // Préférences d'affichage
  final DisplayMode displayMode;
  final String language;
  final bool notificationsEnabled;

  // Unités
  final String massUnit; // 'kg' ou 'g'
  final String volumeUnit; // 'L' ou 'mL'

  final DateTime updatedAt;

  const AppSettings({
    this.co2Weight = 0.4,
    this.waterWeight = 0.3,
    this.energyWeight = 0.3,
    this.sensitivity = EnvironmentalSensitivity.medium,
    this.displayMode = DisplayMode.system,
    this.language = 'fr',
    this.notificationsEnabled = true,
    this.massUnit = 'kg',
    this.volumeUnit = 'L',
    required this.updatedAt,
  });

  AppSettings copyWith({
    double? co2Weight,
    double? waterWeight,
    double? energyWeight,
    EnvironmentalSensitivity? sensitivity,
    DisplayMode? displayMode,
    String? language,
    bool? notificationsEnabled,
    String? massUnit,
    String? volumeUnit,
    DateTime? updatedAt,
  }) {
    return AppSettings(
      co2Weight: co2Weight ?? this.co2Weight,
      waterWeight: waterWeight ?? this.waterWeight,
      energyWeight: energyWeight ?? this.energyWeight,
      sensitivity: sensitivity ?? this.sensitivity,
      displayMode: displayMode ?? this.displayMode,
      language: language ?? this.language,
      notificationsEnabled: notificationsEnabled ?? this.notificationsEnabled,
      massUnit: massUnit ?? this.massUnit,
      volumeUnit: volumeUnit ?? this.volumeUnit,
      updatedAt: updatedAt ?? DateTime.now(),
    );
  }

  /// Valide que les pondérations totalisent 1.0
  bool get isValidWeights {
    final total = co2Weight + waterWeight + energyWeight;
    return (total - 1.0).abs() < 0.01;
  }

  @override
  List<Object?> get props => [
        co2Weight,
        waterWeight,
        energyWeight,
        sensitivity,
        displayMode,
        language,
        notificationsEnabled,
        massUnit,
        volumeUnit,
        updatedAt,
      ];
}
