import '../entities/user.dart';
import '../entities/auth_request.dart';
import '../repositories/auth_repository.dart';

/// Use case pour la connexion
class LoginUseCase {
  final AuthRepository repository;

  LoginUseCase(this.repository);

  Future<User> call(AuthRequest request) async {
    return await repository.login(request);
  }
}
