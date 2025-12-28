import '../../domain/entities/user.dart';
import '../../domain/entities/auth_request.dart';
import '../../domain/entities/signup_request.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_remote_ds.dart';
import '../datasources/auth_local_ds.dart';
import '../models/user_model.dart';

/// Implémentation du repository d'authentification
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
  });

  @override
  Future<User> login(AuthRequest request) async {
    try {
      final user = await remoteDataSource.login(request);
      await localDataSource.saveUser(user);
      return user;
    } catch (e) {
      // Ne pas utiliser de fallback local - propager l'erreur pour que l'utilisateur soit informé
      rethrow;
    }
  }

  @override
  Future<User> signup(SignupRequest request) async {
    try {
      final user = await remoteDataSource.signup(request);
      await localDataSource.saveUser(user);
      return user;
    } catch (e) {
      // Ne pas utiliser de fallback local - propager l'erreur pour que l'utilisateur soit informé
      rethrow;
    }
  }

  @override
  Future<void> logout() async {
    await localDataSource.clearAuth();
  }

  @override
  Future<User?> getCurrentUser() async {
    // D'abord essayer de récupérer depuis le backend pour vérifier le token
    try {
      final user = await remoteDataSource.getCurrentUser();
      await localDataSource.saveUser(user);
      return user;
    } catch (e) {
      // Si échec, récupérer depuis le stockage local
      return localDataSource.getUser();
    }
  }

  @override
  Future<String?> getToken() async {
    return localDataSource.getToken();
  }
  
  @override
  Future<User> updateProfile(Map<String, String> updates) async {
    try {
      // Récupérer le token actuel avant la mise à jour
      final currentToken = await localDataSource.getToken();
      
      // Mettre à jour le profil via l'API
      final updatedUser = await remoteDataSource.updateProfile(updates);
      
      // Créer un nouveau User avec le token préservé
      final userWithToken = UserModel(
        id: updatedUser.id,
        email: updatedUser.email,
        name: updatedUser.name,
        pays: updatedUser.pays,
        token: currentToken, // Préserver le token existant
      );
      
      // Sauvegarder avec le token
      await localDataSource.saveUser(userWithToken);
      
      return userWithToken;
    } catch (e) {
      rethrow;
    }
  }
  
  @override
  Future<User> socialAuth({
    required String email,
    String? name,
    required String provider,
    String? providerId,
    String? accessToken,
    String? idToken,
  }) async {
    try {
      final user = await remoteDataSource.socialAuth(
        email: email,
        name: name,
        provider: provider,
        providerId: providerId,
        accessToken: accessToken,
        idToken: idToken,
      );
      
      await localDataSource.saveUser(user);
      return user;
    } catch (e) {
      rethrow;
    }
  }
}
