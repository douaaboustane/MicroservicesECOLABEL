import '../../domain/entities/app_settings.dart';

/// Modèle de données pour AppSettings
class AppSettingsModel extends AppSettings {
  const AppSettingsModel({
    super.co2Weight,
    super.waterWeight,
    super.energyWeight,
    super.sensitivity,
    super.displayMode,
    super.language,
    super.notificationsEnabled,
    super.massUnit,
    super.volumeUnit,
    required super.updatedAt,
  });

  factory AppSettingsModel.fromJson(Map<String, dynamic> json) {
    return AppSettingsModel(
      co2Weight: (json['co2_weight'] as num?)?.toDouble() ?? 0.4,
      waterWeight: (json['water_weight'] as num?)?.toDouble() ?? 0.3,
      energyWeight: (json['energy_weight'] as num?)?.toDouble() ?? 0.3,
      sensitivity: EnvironmentalSensitivity.values.firstWhere(
        (e) => e.name == json['sensitivity'],
        orElse: () => EnvironmentalSensitivity.medium,
      ),
      displayMode: DisplayMode.values.firstWhere(
        (e) => e.name == json['display_mode'],
        orElse: () => DisplayMode.system,
      ),
      language: json['language'] as String? ?? 'fr',
      notificationsEnabled: json['notifications_enabled'] as bool? ?? true,
      massUnit: json['mass_unit'] as String? ?? 'kg',
      volumeUnit: json['volume_unit'] as String? ?? 'L',
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'] as String)
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'co2_weight': co2Weight,
      'water_weight': waterWeight,
      'energy_weight': energyWeight,
      'sensitivity': sensitivity.name,
      'display_mode': displayMode.name,
      'language': language,
      'notifications_enabled': notificationsEnabled,
      'mass_unit': massUnit,
      'volume_unit': volumeUnit,
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}
