import '../entities/app_settings.dart';
import '../repositories/settings_repository.dart';

/// Use case pour mettre à jour les paramètres
class UpdateSettingsUseCase {
  final SettingsRepository repository;

  UpdateSettingsUseCase(this.repository);

  Future<AppSettings> call(AppSettings settings) async {
    return await repository.updateSettings(settings);
  }
}
