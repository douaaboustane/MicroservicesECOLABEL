import 'package:flutter/material.dart';

/// Palette de couleurs écologique pour EcoLabel-MS
class EcoColors {
  // Couleurs primaires
  static const Color primaryGreen = Color(0xFF2E7D32); // 🌱 Vert primaire
  static const Color lightGreen = Color(0xFF66BB6A); // 🍃 Vert clair (succès / score A)
  static const Color scientificBlue = Color(0xFF1565C0); // 🔬 Bleu scientifique
  static const Color naturalBeige = Color(0xFFF4F1EC); // 🌾 Beige naturel (fond)
  static const Color offWhite = Color(0xFFFAFAFA); // 🤍 Blanc cassé

  // Couleurs des scores
  static const Color scoreA = Color(0xFF2E7D32); // A - Excellent
  static const Color scoreB = Color(0xFF7CB342); // B - Très bon
  static const Color scoreC = Color(0xFFFBC02D); // C - Moyen
  static const Color scoreD = Color(0xFFFB8C00); // D - Faible
  static const Color scoreE = Color(0xFFC62828); // E - Très faible

  // Couleurs d'impact
  static const Color co2Color = Color(0xFF424242); // 🌫️ CO₂
  static const Color waterColor = Color(0xFF0277BD); // 💧 Eau
  static const Color energyColor = Color(0xFFFFA726); // ⚡ Énergie

  // Utilitaires
  static const Color error = Color(0xFFD32F2F);
  static const Color warning = Color(0xFFF57C00);
  static const Color success = lightGreen;
  static const Color info = scientificBlue;

  /// Retourne la couleur associée à un score (A-E)
  static Color getScoreColor(String score) {
    switch (score.toUpperCase()) {
      case 'A':
        return scoreA;
      case 'B':
        return scoreB;
      case 'C':
        return scoreC;
      case 'D':
        return scoreD;
      case 'E':
        return scoreE;
      default:
        return Colors.grey;
    }
  }
}
