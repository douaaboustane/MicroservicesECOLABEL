import '../entities/user_profile.dart';
import '../repositories/profile_repository.dart';

/// Use case pour mettre à jour le profil
class UpdateProfileUseCase {
  final ProfileRepository repository;

  UpdateProfileUseCase(this.repository);

  Future<UserProfile> call(UserProfile profile) async {
    return await repository.updateProfile(profile);
  }
}
