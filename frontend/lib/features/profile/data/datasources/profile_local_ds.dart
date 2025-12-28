import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_profile_model.dart';

/// Source de données locale pour le profil
class ProfileLocalDataSource {
  static const String _profileKey = 'user_profile';

  final SharedPreferences prefs;

  ProfileLocalDataSource(this.prefs);

  /// Sauvegarder le profil
  Future<void> saveProfile(UserProfileModel profile) async {
    await prefs.setString(_profileKey, jsonEncode(profile.toJson()));
  }

  /// Récupérer le profil
  UserProfileModel? getProfile() {
    final profileJson = prefs.getString(_profileKey);
    if (profileJson == null) return null;
    try {
      return UserProfileModel.fromJson(
        jsonDecode(profileJson) as Map<String, dynamic>,
      );
    } catch (e) {
      return null;
    }
  }

  /// Supprimer le profil
  Future<void> deleteProfile() async {
    await prefs.remove(_profileKey);
  }
}
