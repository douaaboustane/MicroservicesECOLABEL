import '../repositories/auth_repository.dart';

/// Use case pour la déconnexion
class LogoutUseCase {
  final AuthRepository repository;

  LogoutUseCase(this.repository);

  Future<void> call() async {
    await repository.logout();
  }
}
