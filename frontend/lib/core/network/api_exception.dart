import 'package:dio/dio.dart';

/// Exception personnalisée pour les erreurs API
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final dynamic originalError;

  ApiException({
    required this.message,
    this.statusCode,
    this.originalError,
  });

  factory ApiException.fromDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return ApiException(
          message: 'Timeout de connexion',
          originalError: error,
        );
      case DioExceptionType.badResponse:
        // Essayer d'extraire le message d'erreur du backend
        String? backendMessage;
        if (error.response?.data != null) {
          try {
            final data = error.response!.data;
            if (data is Map<String, dynamic>) {
              backendMessage = data['message'] as String? ?? 
                              data['detail'] as String? ??
                              data['error'] as String?;
            }
          } catch (e) {
            // Ignorer si on ne peut pas parser
          }
        }
        return ApiException(
          message: backendMessage ?? _handleStatusCode(error.response?.statusCode),
          statusCode: error.response?.statusCode,
          originalError: error,
        );
      case DioExceptionType.cancel:
        return ApiException(
          message: 'Requête annulée',
          originalError: error,
        );
      case DioExceptionType.unknown:
      default:
        return ApiException(
          message: 'Erreur de connexion. Vérifiez votre réseau.',
          originalError: error,
        );
    }
  }

  static String _handleStatusCode(int? statusCode) {
    switch (statusCode) {
      case 400:
        return 'Requête invalide';
      case 401:
        return 'Non autorisé';
      case 403:
        return 'Accès refusé';
      case 404:
        return 'Ressource non trouvée';
      case 500:
        return 'Erreur serveur';
      case 502:
        return 'Bad Gateway';
      case 503:
        return 'Service indisponible';
      default:
        return 'Erreur inconnue';
    }
  }

  @override
  String toString() => message;
}
