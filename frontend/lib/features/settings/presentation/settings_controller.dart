import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/entities/app_settings.dart';
import '../domain/usecases/get_settings_usecase.dart';
import '../domain/usecases/update_settings_usecase.dart';

/// Controller pour les paramètres
class SettingsController extends StateNotifier<AsyncValue<AppSettings?>> {
  final GetSettingsUseCase getSettingsUseCase;
  final UpdateSettingsUseCase updateSettingsUseCase;

  SettingsController({
    required this.getSettingsUseCase,
    required this.updateSettingsUseCase,
  }) : super(const AsyncValue.loading()) {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    try {
      final settings = await getSettingsUseCase();
      state = AsyncValue.data(settings);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> updateSettings(AppSettings settings) async {
    state = const AsyncValue.loading();
    try {
      final updated = await updateSettingsUseCase(settings);
      state = AsyncValue.data(updated);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }
}
