import '../entities/app_settings.dart';
import '../repositories/settings_repository.dart';

/// Use case pour récupérer les paramètres
class GetSettingsUseCase {
  final SettingsRepository repository;

  GetSettingsUseCase(this.repository);

  Future<AppSettings> call() async {
    return await repository.getSettings();
  }
}
