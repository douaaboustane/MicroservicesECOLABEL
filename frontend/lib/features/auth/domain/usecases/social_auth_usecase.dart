import '../repositories/auth_repository.dart';
import '../entities/user.dart';

class SocialAuthUseCase {
  final AuthRepository repository;

  SocialAuthUseCase(this.repository);

  Future<User> call({
    required String email,
    String? name,
    required String provider,
    String? providerId,
    String? accessToken,
    String? idToken,
  }) async {
    return await repository.socialAuth(
      email: email,
      name: name,
      provider: provider,
      providerId: providerId,
      accessToken: accessToken,
      idToken: idToken,
    );
  }
}

