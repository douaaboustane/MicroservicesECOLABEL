import 'package:flutter/material.dart';
import '../constants/colors.dart';

/// Utilitaires pour mapper les scores
class ScoreMapper {
  /// Convertit un score numérique (0-100) en lettre (A-E)
  static String numericToLetter(int score) {
    if (score >= 80) return 'A';
    if (score >= 60) return 'B';
    if (score >= 40) return 'C';
    if (score >= 20) return 'D';
    return 'E';
  }

  /// Retourne la couleur associée à un score numérique
  static Color getScoreColor(int score) {
    return EcoColors.getScoreColor(numericToLetter(score));
  }

  /// Retourne la description d'un score
  static String getScoreDescription(String score) {
    switch (score.toUpperCase()) {
      case 'A':
        return 'Excellent';
      case 'B':
        return 'Très bon';
      case 'C':
        return 'Moyen';
      case 'D':
        return 'Faible';
      case 'E':
        return 'Très faible';
      default:
        return 'Non évalué';
    }
  }
}
