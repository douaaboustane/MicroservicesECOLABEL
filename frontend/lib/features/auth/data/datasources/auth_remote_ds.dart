import '../../../../core/network/api_client.dart';
import '../models/user_model.dart';
import '../../domain/entities/auth_request.dart';
import '../../domain/entities/signup_request.dart';

/// Source de données distante pour l'authentification
class AuthRemoteDataSource {
  final ApiClient apiClient;

  AuthRemoteDataSource(this.apiClient);

  /// Connexion
  Future<UserModel> login(AuthRequest request) async {
    final response = await apiClient.post<Map<String, dynamic>>(
      '/mobile/auth/login',
      data: {
        'email': request.email,
        'password': request.password,
      },
    );

    return UserModel.fromJson(response.data!);
  }

  /// Inscription
  Future<UserModel> signup(SignupRequest request) async {
    final response = await apiClient.post<Map<String, dynamic>>(
      '/mobile/auth/signup',
      data: {
        'email': request.email,
        'password': request.password,
        if (request.name != null) 'name': request.name,
        if (request.pays != null) 'pays': request.pays,
      },
    );

    return UserModel.fromJson(response.data!);
  }

  /// Récupérer l'utilisateur actuel depuis le backend
  Future<UserModel> getCurrentUser() async {
    final response = await apiClient.get<Map<String, dynamic>>(
      '/mobile/auth/me',
    );

    return UserModel.fromJson(response.data!);
  }
  
  /// Mettre à jour le profil utilisateur
  Future<UserModel> updateProfile(Map<String, String> updates) async {
    final response = await apiClient.patch<Map<String, dynamic>>(
      '/mobile/auth/me',
      data: updates,
    );

    return UserModel.fromJson(response.data!);
  }
  
  /// Authentification sociale (Google, Apple, Microsoft)
  Future<UserModel> socialAuth({
    required String email,
    String? name,
    required String provider,
    String? providerId,
    String? accessToken,
    String? idToken,
  }) async {
    final response = await apiClient.post<Map<String, dynamic>>(
      '/mobile/auth/social',
      data: {
        'email': email,
        if (name != null) 'name': name,
        'provider': provider,
        if (providerId != null) 'providerId': providerId,
        if (accessToken != null) 'accessToken': accessToken,
        if (idToken != null) 'idToken': idToken,
      },
    );

    return UserModel.fromJson(response.data!);
  }
}
