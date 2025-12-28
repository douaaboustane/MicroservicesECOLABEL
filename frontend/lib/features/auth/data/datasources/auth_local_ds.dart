import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_model.dart';

/// Source de données locale pour l'authentification
class AuthLocalDataSource {
  static const String _userKey = 'user';
  static const String _tokenKey = 'token';

  final SharedPreferences prefs;

  AuthLocalDataSource(this.prefs);

  /// Sauvegarder l'utilisateur
  Future<void> saveUser(UserModel user) async {
    await prefs.setString(_userKey, jsonEncode(user.toJson()));
    if (user.token != null) {
      await prefs.setString(_tokenKey, user.token!);
    }
  }

  /// Récupérer l'utilisateur
  UserModel? getUser() {
    final userJson = prefs.getString(_userKey);
    if (userJson == null) return null;
    try {
      return UserModel.fromJson(jsonDecode(userJson) as Map<String, dynamic>);
    } catch (e) {
      return null;
    }
  }

  /// Récupérer le token
  String? getToken() {
    return prefs.getString(_tokenKey);
  }

  /// Supprimer les données d'authentification
  Future<void> clearAuth() async {
    await prefs.remove(_userKey);
    await prefs.remove(_tokenKey);
  }
}
