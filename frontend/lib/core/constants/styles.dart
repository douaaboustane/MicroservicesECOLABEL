import 'package:flutter/material.dart';

/// Constantes de style pour assurer la cohérence visuelle dans toute l'application
class EcoStyles {
  EcoStyles._();

  // ═══════════════════════════════════════════════════════════════════════
  // BORDER RADIUS - Coins arrondis cohérents
  // ═══════════════════════════════════════════════════════════════════════
  
  /// Petits éléments (badges, chips)
  static const double radiusSmall = 12.0;
  
  /// Éléments moyens (boutons, petites cartes)
  static const double radiusMedium = 16.0;
  
  /// Grandes cartes et containers
  static const double radiusLarge = 20.0;
  
  /// Éléments très grands (cartes principales)
  static const double radiusXLarge = 24.0;
  
  /// Cercles complets
  static const double radiusCircular = 999.0;

  // ═══════════════════════════════════════════════════════════════════════
  // SHADOWS - Ombres standardisées
  // ═══════════════════════════════════════════════════════════════════════
  
  /// Ombre légère pour les éléments subtils
  static List<BoxShadow> shadowLight = [
    BoxShadow(
      color: Colors.black.withValues(alpha: 0.04),
      blurRadius: 8,
      offset: const Offset(0, 2),
    ),
  ];
  
  /// Ombre moyenne pour les cartes
  static List<BoxShadow> shadowMedium = [
    BoxShadow(
      color: Colors.black.withValues(alpha: 0.06),
      blurRadius: 12,
      offset: const Offset(0, 4),
    ),
  ];
  
  /// Ombre forte pour les éléments en relief
  static List<BoxShadow> shadowStrong = [
    BoxShadow(
      color: Colors.black.withValues(alpha: 0.10),
      blurRadius: 16,
      offset: const Offset(0, 6),
    ),
  ];
  
  /// Ombre colorée pour les badges de score
  static BoxShadow shadowColored(Color color) {
    return BoxShadow(
      color: color.withValues(alpha: 0.35),
      blurRadius: 12,
      offset: const Offset(0, 4),
    );
  }

  // ═══════════════════════════════════════════════════════════════════════
  // GRADIENTS - Dégradés harmonieux
  // ═══════════════════════════════════════════════════════════════════════
  
  /// Dégradé vert principal (Scanner, éléments verts)
  static const LinearGradient gradientGreen = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFFA8D5A8), // Vert clair
      Color(0xFF8BC48B), // Vert moyen
    ],
  );
  
  /// Dégradé bleu (Importer, éléments bleus)
  static const LinearGradient gradientBlue = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFF9BBFDA), // Bleu clair
      Color(0xFF7AA5C9), // Bleu moyen
    ],
  );
  
  /// Dégradé sage pour statistiques
  static const LinearGradient gradientSage = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFFA8B5A0), // Sage doux
      Color(0xFFBEC9B6), // Vert-gris clair
    ],
  );
  
  /// Dégradé de fond de page
  static LinearGradient gradientBackground(Color primaryColor, Color secondaryColor) {
    return LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [
        primaryColor.withValues(alpha: 0.1),
        secondaryColor.withValues(alpha: 0.05),
        const Color(0xFFF8F5F2), // Natural beige
      ],
      stops: const [0.0, 0.5, 1.0],
    );
  }

  // ═══════════════════════════════════════════════════════════════════════
  // SPACING - Espacements cohérents
  // ═══════════════════════════════════════════════════════════════════════
  
  static const double spacingXS = 4.0;
  static const double spacingS = 8.0;
  static const double spacingM = 12.0;
  static const double spacingL = 16.0;
  static const double spacingXL = 20.0;
  static const double spacingXXL = 24.0;
  static const double spacingXXXL = 32.0;

  // ═══════════════════════════════════════════════════════════════════════
  // CARD DECORATION - Style de carte standard
  // ═══════════════════════════════════════════════════════════════════════
  
  /// Décoration pour les cartes blanches standard
  static BoxDecoration cardWhite = BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(radiusLarge),
    boxShadow: shadowMedium,
  );
  
  /// Décoration pour les cartes avec dégradé
  static BoxDecoration cardGradient(LinearGradient gradient) {
    return BoxDecoration(
      gradient: gradient,
      borderRadius: BorderRadius.circular(radiusLarge),
      boxShadow: shadowMedium,
    );
  }
  
  /// Décoration pour les petits containers (icônes)
  static BoxDecoration iconContainer(Color color, {double opacity = 0.3}) {
    return BoxDecoration(
      color: color.withValues(alpha: opacity),
      borderRadius: BorderRadius.circular(radiusMedium + 2),
    );
  }

  // ═══════════════════════════════════════════════════════════════════════
  // TEXT STYLES - Styles de texte cohérents
  // ═══════════════════════════════════════════════════════════════════════
  
  /// Titre de carte (blanc sur fond coloré)
  static const TextStyle cardTitle = TextStyle(
    color: Colors.white,
    fontSize: 20,
    fontWeight: FontWeight.bold,
  );
  
  /// Sous-titre de carte (blanc avec opacité)
  static TextStyle cardSubtitle = TextStyle(
    color: Colors.white.withValues(alpha: 0.9),
    fontSize: 13,
    fontWeight: FontWeight.w500,
  );
  
  /// Texte du corps sur fond blanc
  static const TextStyle bodyText = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.bold,
    color: Color(0xFF2D3436),
    height: 1.2,
  );
  
  /// Texte secondaire
  static TextStyle bodyTextSecondary = TextStyle(
    fontSize: 13,
    fontWeight: FontWeight.w600,
    color: Colors.grey[600],
  );
}

