import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/entities/user.dart';
import '../domain/usecases/login_usecase.dart';
import '../domain/usecases/signup_usecase.dart';
import '../domain/usecases/logout_usecase.dart';
import '../domain/usecases/get_current_user_usecase.dart';
import '../domain/usecases/update_profile_usecase.dart';
import '../domain/usecases/social_auth_usecase.dart';
import '../domain/entities/auth_request.dart';
import '../domain/entities/signup_request.dart';

/// Controller pour l'authentification
class AuthController extends StateNotifier<AsyncValue<User?>> {
  final LoginUseCase loginUseCase;
  final SignupUseCase signupUseCase;
  final LogoutUseCase logoutUseCase;
  final GetCurrentUserUseCase getCurrentUserUseCase;
  final UpdateProfileUseCase updateProfileUseCase;
  final SocialAuthUseCase socialAuthUseCase;

  AuthController({
    required this.loginUseCase,
    required this.signupUseCase,
    required this.logoutUseCase,
    required this.getCurrentUserUseCase,
    required this.updateProfileUseCase,
    required this.socialAuthUseCase,
  }) : super(const AsyncValue.loading()) {
    _checkAuth();
  }

  Future<void> _checkAuth() async {
    try {
      final user = await getCurrentUserUseCase();
      state = AsyncValue.data(user);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<bool> login(String email, String password) async {
    state = const AsyncValue.loading();
    try {
      final request = AuthRequest(email: email, password: password);
      final user = await loginUseCase(request);
      state = AsyncValue.data(user);
      return true;
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
      return false;
    }
  }

  Future<bool> signup(String email, String password, {String? name, String? pays}) async {
    state = const AsyncValue.loading();
    try {
      final request = SignupRequest(
        email: email,
        password: password,
        name: name,
        pays: pays,
      );
      final user = await signupUseCase(request);
      state = AsyncValue.data(user);
      return true;
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
      return false;
    }
  }

  Future<void> logout() async {
    try {
      await logoutUseCase();
      state = const AsyncValue.data(null);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  /// Connexion avec un provider social
  Future<bool> signInWithSocial({
    required String email,
    String? name,
    required String provider,
    String? providerId,
    String? accessToken,
    String? idToken,
  }) async {
    state = const AsyncValue.loading();
    try {
      final user = await socialAuthUseCase(
        email: email,
        name: name,
        provider: provider,
        providerId: providerId,
        accessToken: accessToken,
        idToken: idToken,
      );
      state = AsyncValue.data(user);
      return true;
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
      return false;
    }
  }
  
  /// Mettre à jour le profil utilisateur
  Future<bool> updateProfile(Map<String, String> updates) async {
    try {
      final updatedUser = await updateProfileUseCase(updates);
      state = AsyncValue.data(updatedUser);
      return true;
    } catch (e, stack) {
      // NE PAS mettre l'état en erreur pour éviter la déconnexion
      // L'utilisateur reste connecté même si la mise à jour échoue
      print('Erreur updateProfile: $e');
      return false;
    }
  }
}
