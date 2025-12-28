import '../entities/user.dart';
import '../entities/auth_request.dart';
import '../entities/signup_request.dart';

/// Repository pour l'authentification
abstract class AuthRepository {
  Future<User> login(AuthRequest request);
  Future<User> signup(SignupRequest request);
  Future<void> logout();
  Future<User?> getCurrentUser();
  Future<String?> getToken();
  Future<User> updateProfile(Map<String, String> updates);
  
  Future<User> socialAuth({
    required String email,
    String? name,
    required String provider,
    String? providerId,
    String? accessToken,
    String? idToken,
  });
}
