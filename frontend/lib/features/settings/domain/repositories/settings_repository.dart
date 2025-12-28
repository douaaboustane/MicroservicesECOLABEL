import '../entities/app_settings.dart';

/// Repository pour les paramètres
abstract class SettingsRepository {
  Future<AppSettings> getSettings();
  Future<AppSettings> updateSettings(AppSettings settings);
  Future<void> resetSettings();
}
