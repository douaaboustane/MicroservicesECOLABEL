import 'dart:io';

/// Configuration de l'environnement
class Env {
  // Base URL de l'API backend
  // Support pour différents environnements :
  // - iOS Simulator / macOS : http://localhost:8000
  // - Android Emulator : http://10.0.2.2:8000
  // - Appareil physique : http://VOTRE_IP:8000
  static String get baseUrl {
    // Vérifier si une URL est fournie via variable d'environnement
    const envUrl = String.fromEnvironment('API_BASE_URL');
    if (envUrl.isNotEmpty) {
      return envUrl;
    }
    
    // Détection automatique de la plateforme
    if (Platform.isAndroid) {
      // Android Emulator utilise 10.0.2.2 pour accéder à localhost de la machine hôte
      return 'http://10.0.2.2:8000';
    } else if (Platform.isIOS) {
      // iOS Simulator et appareil physique
      // Par défaut, utiliser localhost (fonctionne pour simulateur et parfois pour appareil physique)
      // Pour iPhone physique, utiliser la variable d'environnement :
      // flutter run --dart-define=API_BASE_URL=http://192.168.100.129:8000
      return 'http://localhost:8000';
    } else {
      // macOS, Linux, Windows
      return 'http://localhost:8000';
    }
  }

  // Timeout pour les requêtes
  static const Duration requestTimeout = Duration(seconds: 30);

  // Intervalle de polling pour le statut du job
  static const Duration pollingInterval = Duration(seconds: 2);

  // Timeout maximum pour le polling (augmenté pour permettre le traitement OCR long)
  static const Duration pollingTimeout = Duration(minutes: 10);
}
