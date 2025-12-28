import '../entities/user.dart';
import '../entities/signup_request.dart';
import '../repositories/auth_repository.dart';

/// Use case pour l'inscription
class SignupUseCase {
  final AuthRepository repository;

  SignupUseCase(this.repository);

  Future<User> call(SignupRequest request) async {
    return await repository.signup(request);
  }
}
