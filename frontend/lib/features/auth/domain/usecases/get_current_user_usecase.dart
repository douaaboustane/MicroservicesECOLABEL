import '../entities/user.dart';
import '../repositories/auth_repository.dart';

/// Use case pour récupérer l'utilisateur actuel
class GetCurrentUserUseCase {
  final AuthRepository repository;

  GetCurrentUserUseCase(this.repository);

  Future<User?> call() async {
    return await repository.getCurrentUser();
  }
}
