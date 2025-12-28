import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../injection_container.dart' as di;
import 'settings_controller.dart';
import '../domain/usecases/get_settings_usecase.dart';
import '../domain/usecases/update_settings_usecase.dart';

/// Provider pour le controller de paramètres
final settingsControllerProvider =
    StateNotifierProvider<SettingsController, AsyncValue<dynamic>>((ref) {
  // Vérifier que GetIt est initialisé
  if (!di.getIt.isRegistered<GetSettingsUseCase>()) {
    throw StateError(
      'GetSettingsUseCase is not registered. Make sure setupDependencyInjection() is called before using this provider.',
    );
  }
  return SettingsController(
    getSettingsUseCase: di.getIt<GetSettingsUseCase>(),
    updateSettingsUseCase: di.getIt<UpdateSettingsUseCase>(),
  );
});
