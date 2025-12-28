import '../entities/user_profile.dart';

/// Repository pour le profil utilisateur
abstract class ProfileRepository {
  Future<UserProfile> getProfile();
  Future<UserProfile> updateProfile(UserProfile profile);
  Future<void> deleteProfile();
}
