import '../../domain/entities/user_profile.dart';
import '../../domain/repositories/profile_repository.dart';
import '../datasources/profile_local_ds.dart';
import '../models/user_profile_model.dart';

/// Implémentation du repository de profil
class ProfileRepositoryImpl implements ProfileRepository {
  final ProfileLocalDataSource localDataSource;

  ProfileRepositoryImpl(this.localDataSource);

  @override
  Future<UserProfile> getProfile() async {
    final profile = localDataSource.getProfile();
    if (profile != null) {
      return profile;
    }
    // Créer un profil par défaut
    final defaultProfile = UserProfileModel(
      id: 'local_${DateTime.now().millisecondsSinceEpoch}',
      dietType: DietType.standard,
      ecoGoals: const [],
      createdAt: DateTime.now(),
    );
    await localDataSource.saveProfile(defaultProfile);
    return defaultProfile;
  }

  @override
  Future<UserProfile> updateProfile(UserProfile profile) async {
    final model = UserProfileModel(
      id: profile.id,
      name: profile.name,
      avatarUrl: profile.avatarUrl,
      country: profile.country,
      region: profile.region,
      dietType: profile.dietType,
      ecoGoals: profile.ecoGoals,
      createdAt: profile.createdAt,
      updatedAt: DateTime.now(),
    );
    await localDataSource.saveProfile(model);
    return model;
  }

  @override
  Future<void> deleteProfile() async {
    await localDataSource.deleteProfile();
  }
}
