import 'package:google_sign_in/google_sign_in.dart';
import 'package:sign_in_with_apple/sign_in_with_apple.dart';
import 'dart:io';

/// Service pour l'authentification sociale
class SocialAuthService {
  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email', 'profile'],
  );

  /// Connexion avec Google
  Future<SocialAuthResult?> signInWithGoogle() async {
    try {
      final GoogleSignInAccount? account = await _googleSignIn.signIn();
      if (account == null) return null;

      final GoogleSignInAuthentication auth = await account.authentication;

      return SocialAuthResult(
        email: account.email,
        name: account.displayName,
        id: account.id,
        accessToken: auth.accessToken,
        idToken: auth.idToken,
        provider: 'google',
      );
    } catch (e) {
      throw Exception('Erreur lors de la connexion Google: $e');
    }
  }

  /// Connexion avec Apple
  Future<SocialAuthResult?> signInWithApple() async {
    try {
      // Vérifier si Apple Sign In est disponible (iOS/macOS uniquement)
      if (!Platform.isIOS && !Platform.isMacOS) {
        throw Exception('Apple Sign In n\'est disponible que sur iOS/macOS');
      }

      final credential = await SignInWithApple.getAppleIDCredential(
        scopes: [
          AppleIDAuthorizationScopes.email,
          AppleIDAuthorizationScopes.fullName,
        ],
      );

      return SocialAuthResult(
        email: credential.email,
        name: credential.givenName != null && credential.familyName != null
            ? '${credential.givenName} ${credential.familyName}'
            : null,
        id: credential.userIdentifier,
        accessToken: credential.identityToken,
        idToken: credential.identityToken,
        provider: 'apple',
      );
    } catch (e) {
      throw Exception('Erreur lors de la connexion Apple: $e');
    }
  }

  /// Connexion avec Microsoft
  Future<SocialAuthResult?> signInWithMicrosoft() async {
    try {
      // Note: msal_flutter nécessite une configuration Azure AD
      // Pour l'instant, on retourne une erreur indiquant que c'est à implémenter
      throw UnimplementedError(
        'Microsoft Sign In nécessite une configuration Azure AD. '
        'Veuillez configurer msal_flutter dans votre projet.',
      );
    } catch (e) {
      throw Exception('Erreur lors de la connexion Microsoft: $e');
    }
  }

  /// Déconnexion
  Future<void> signOut() async {
    await _googleSignIn.signOut();
  }
}

/// Résultat de l'authentification sociale
class SocialAuthResult {
  final String? email;
  final String? name;
  final String? id;
  final String? accessToken;
  final String? idToken;
  final String provider;

  SocialAuthResult({
    required this.email,
    this.name,
    required this.id,
    this.accessToken,
    this.idToken,
    required this.provider,
  });
}


