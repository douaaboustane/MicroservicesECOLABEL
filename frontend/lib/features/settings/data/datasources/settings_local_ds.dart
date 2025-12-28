import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/app_settings_model.dart';

/// Source de données locale pour les paramètres
class SettingsLocalDataSource {
  static const String _settingsKey = 'app_settings';

  final SharedPreferences prefs;

  SettingsLocalDataSource(this.prefs);

  /// Sauvegarder les paramètres
  Future<void> saveSettings(AppSettingsModel settings) async {
    await prefs.setString(_settingsKey, jsonEncode(settings.toJson()));
  }

  /// Récupérer les paramètres
  AppSettingsModel? getSettings() {
    final settingsJson = prefs.getString(_settingsKey);
    if (settingsJson == null) return null;
    try {
      return AppSettingsModel.fromJson(
        jsonDecode(settingsJson) as Map<String, dynamic>,
      );
    } catch (e) {
      return null;
    }
  }

  /// Récupérer les paramètres par défaut
  AppSettingsModel getDefaultSettings() {
    return AppSettingsModel(updatedAt: DateTime.now());
  }

  /// Supprimer les paramètres
  Future<void> deleteSettings() async {
    await prefs.remove(_settingsKey);
  }
}
