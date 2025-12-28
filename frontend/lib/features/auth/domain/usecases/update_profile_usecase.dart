import '../entities/user.dart';
import '../repositories/auth_repository.dart';

/// Use case pour mettre à jour le profil utilisateur
class UpdateProfileUseCase {
  final AuthRepository repository;

  UpdateProfileUseCase(this.repository);

  Future<User> call(Map<String, String> updates) async {
    return repository.updateProfile(updates);
  }
}

