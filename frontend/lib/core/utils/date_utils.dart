import 'package:intl/intl.dart';

/// Utilitaires pour les dates
class DateUtils {
  static final DateFormat _dateFormat = DateFormat('dd/MM/yyyy');
  static final DateFormat _dateTimeFormat = DateFormat('dd/MM/yyyy HH:mm');

  /// Formate une date au format français
  static String formatDate(DateTime date) {
    return _dateFormat.format(date);
  }

  /// Formate une date avec l'heure
  static String formatDateTime(DateTime date) {
    return _dateTimeFormat.format(date);
  }

  /// Formate une date relative (il y a X minutes/heures/jours)
  static String formatRelative(DateTime date) {
    final now = DateTime.now();
    final difference = now.difference(date);

    if (difference.inDays > 0) {
      return 'Il y a ${difference.inDays} jour${difference.inDays > 1 ? 's' : ''}';
    } else if (difference.inHours > 0) {
      return 'Il y a ${difference.inHours} heure${difference.inHours > 1 ? 's' : ''}';
    } else if (difference.inMinutes > 0) {
      return 'Il y a ${difference.inMinutes} minute${difference.inMinutes > 1 ? 's' : ''}';
    } else {
      return 'À l\'instant';
    }
  }
}
