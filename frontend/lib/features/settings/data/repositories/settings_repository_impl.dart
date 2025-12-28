import '../../domain/entities/app_settings.dart';
import '../../domain/repositories/settings_repository.dart';
import '../datasources/settings_local_ds.dart';
import '../models/app_settings_model.dart';

/// Implémentation du repository de paramètres
class SettingsRepositoryImpl implements SettingsRepository {
  final SettingsLocalDataSource localDataSource;

  SettingsRepositoryImpl(this.localDataSource);

  @override
  Future<AppSettings> getSettings() async {
    final settings = localDataSource.getSettings();
    if (settings != null) {
      return settings;
    }
    // Retourner les paramètres par défaut
    return localDataSource.getDefaultSettings();
  }

  @override
  Future<AppSettings> updateSettings(AppSettings settings) async {
    final model = AppSettingsModel(
      co2Weight: settings.co2Weight,
      waterWeight: settings.waterWeight,
      energyWeight: settings.energyWeight,
      sensitivity: settings.sensitivity,
      displayMode: settings.displayMode,
      language: settings.language,
      notificationsEnabled: settings.notificationsEnabled,
      massUnit: settings.massUnit,
      volumeUnit: settings.volumeUnit,
      updatedAt: DateTime.now(),
    );
    await localDataSource.saveSettings(model);
    return model;
  }

  @override
  Future<void> resetSettings() async {
    await localDataSource.deleteSettings();
  }
}
