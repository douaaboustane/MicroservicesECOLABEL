import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../injection_container.dart' as di;
import 'profile_controller.dart';
import '../domain/usecases/get_profile_usecase.dart';
import '../domain/usecases/update_profile_usecase.dart';

/// Provider pour le controller de profil
final profileControllerProvider =
    StateNotifierProvider<ProfileController, AsyncValue<dynamic>>((ref) {
  // Vérifier que GetIt est initialisé
  if (!di.getIt.isRegistered<GetProfileUseCase>()) {
    throw StateError(
      'GetProfileUseCase is not registered. Make sure setupDependencyInjection() is called before using this provider.',
    );
  }
  return ProfileController(
    getProfileUseCase: di.getIt<GetProfileUseCase>(),
    updateProfileUseCase: di.getIt<UpdateProfileUseCase>(),
  );
});
