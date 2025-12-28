import '../entities/user_profile.dart';
import '../repositories/profile_repository.dart';

/// Use case pour récupérer le profil
class GetProfileUseCase {
  final ProfileRepository repository;

  GetProfileUseCase(this.repository);

  Future<UserProfile> call() async {
    return await repository.getProfile();
  }
}
