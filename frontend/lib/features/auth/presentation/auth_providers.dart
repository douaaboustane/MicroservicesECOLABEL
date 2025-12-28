import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../injection_container.dart' as di;
import 'auth_controller.dart';
import '../domain/usecases/login_usecase.dart';
import '../domain/usecases/signup_usecase.dart';
import '../domain/usecases/logout_usecase.dart';
import '../domain/usecases/get_current_user_usecase.dart';
import '../domain/usecases/update_profile_usecase.dart';
import '../domain/usecases/social_auth_usecase.dart';

/// Provider pour le controller d'authentification
/// Note: setupDependencyInjection() doit être appelé dans main() avant runApp()
final authControllerProvider =
    StateNotifierProvider<AuthController, AsyncValue<dynamic>>((ref) {
  // GetIt doit être initialisé avant d'utiliser ce provider
  // setupDependencyInjection() est appelé dans main() avant runApp()
  return AuthController(
    loginUseCase: di.getIt<LoginUseCase>(),
    signupUseCase: di.getIt<SignupUseCase>(),
    logoutUseCase: di.getIt<LogoutUseCase>(),
    getCurrentUserUseCase: di.getIt<GetCurrentUserUseCase>(),
    updateProfileUseCase: di.getIt<UpdateProfileUseCase>(),
    socialAuthUseCase: di.getIt<SocialAuthUseCase>(),
  );
});

/// Provider pour vérifier si l'utilisateur est authentifié
final isAuthenticatedProvider = Provider<bool>((ref) {
  final authState = ref.watch(authControllerProvider);
  return authState.maybeWhen(
    data: (user) => user != null,
    orElse: () => false,
  );
});
